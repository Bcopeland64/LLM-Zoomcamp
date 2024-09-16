from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Dict, List
import getpass
from groq import Groq, APIError
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NFL Rules Chatbot API",
    description="An API for querying NFL rules using AI",
    version="1.0.0",
)

# In-memory storage
feedback_data = []
query_history = []

# Global variables for vectorizer and embeddings
vectorizer = None
embeddings = None
sentences = None

class Query(BaseModel):
    text: str

class Feedback(BaseModel):
    query: str
    response: str
    rating: int

# Get Groq API key
groq_api_key = getpass.getpass("Enter your Groq API key: ")
client = Groq(api_key=groq_api_key)

# Load and process NFL rulebook
def load_nfl_rulebook(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Embed NFL rulebook
def embed_rulebook(text):
    global vectorizer, embeddings, sentences
    sentences = [sent.strip() for sent in text.split('.') if sent.strip()]
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(sentences)
        logger.info("Using SentenceTransformer for embeddings")
    except Exception as e:
        logger.warning(f"Failed to use SentenceTransformer: {e}. Falling back to TfidfVectorizer.")
        vectorizer = TfidfVectorizer()
        embeddings = vectorizer.fit_transform(sentences)
    return sentences, embeddings

# Simple cosine similarity search
def cosine_similarity_search(query_embedding, embeddings, k=5):
    if isinstance(embeddings, np.ndarray) and isinstance(query_embedding, np.ndarray):
        similarities = np.dot(embeddings, query_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding))
    else:
        similarities = cosine_similarity(embeddings, query_embedding.reshape(1, -1)).flatten()
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    return top_k_indices

# Initialize embeddings and index
pdf_path = '/home/brandon/Documents/brandon/LLM Zoomcamp/LLM Zoomcamp Project 2/2023-rulebook_final.pdf'
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"NFL rulebook PDF not found at {pdf_path}")

logger.info("Loading and processing NFL rulebook...")
nfl_rulebook_text = load_nfl_rulebook(pdf_path)
logger.info("Embedding rulebook sentences...")
sentences, embeddings = embed_rulebook(nfl_rulebook_text)
logger.info("Initialization complete.")

@app.get("/")
async def root():
    """
    Root endpoint that provides basic information about the API.
    """
    return {
        "message": "Welcome to the NFL Rules Chatbot API",
        "endpoints": {
            "/query": "POST - Send a question about NFL rules",
            "/feedback": "POST - Provide feedback on a response",
            "/stats": "GET - Retrieve usage statistics"
        }
    }

@app.post("/query")
async def query(query: Query) -> Dict[str, str]:
    """
    Send a question about NFL rules and get an AI-generated response.
    """
    try:
        # Embed the query
        if vectorizer:
            query_embedding = vectorizer.transform([query.text])
        else:
            query_embedding = embed_rulebook(query.text)[1][0]
        
        # Search for relevant sentences
        top_k_indices = cosine_similarity_search(query_embedding, embeddings)
        relevant_sentences = [sentences[i] for i in top_k_indices]
        
        # Prepare context for Groq
        context = " ".join(relevant_sentences)
        
        # Query Groq
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an NFL rules expert assistant. Use the following context from the NFL rulebook to answer the question: " + context},
                    {"role": "user", "content": query.text}
                ],
                model="mixtral-8x7b-32768",
                temperature=0.5,
                max_tokens=1000,
                top_p=1,
            )
            
            answer = chat_completion.choices[0].message.content
            query_history.append({"query": query.text, "response": answer})
            return {"response": answer}
        except APIError as e:
            logger.error(f"Groq API error: {e}")
            raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.post("/feedback")
async def feedback(fb: Feedback) -> Dict[str, str]:
    """
    Provide feedback on a response from the chatbot.
    """
    feedback_data.append(fb.dict())
    return {"status": "Feedback recorded successfully"}

@app.get("/stats")
async def get_stats() -> Dict[str, int]:
    """
    Retrieve usage statistics for the chatbot.
    """
    return {
        "total_queries": len(query_history),
        "total_feedback": len(feedback_data),
        "average_rating": sum(fb['rating'] for fb in feedback_data) / len(feedback_data) if feedback_data else 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)