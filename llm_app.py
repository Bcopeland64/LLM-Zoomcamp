import streamlit as st
import requests
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration
import time

# Download the minsearch.py script if not already present
if not os.path.exists("minsearch.py"):
    url = "https://raw.githubusercontent.com/alexeygrigorev/minsearch/main/minsearch.py"
    response = requests.get(url)
    with open("minsearch.py", "w") as file:
        file.write(response.text)

import minsearch

# Load the documents
docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']
    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

# Initialize the index
index = minsearch.Index(
    text_fields=["question", "text", "section"],
    keyword_fields=["course"]
)

index.fit(documents)

# Function to perform search
def search(query):
    boost = {'question': 3.0, 'section': 0.5}
    results = index.search(
        query=query,
        filter_dict={'course': 'data-engineering-zoomcamp'},
        boost_dict=boost,
        num_results=5
    )
    return results

# Function to build prompt
def build_prompt(query, search_results):
    prompt_template = """
    You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
    Use only the facts from the CONTEXT when answering the QUESTION.

    QUESTION: {question}

    CONTEXT: 
    {context}
    """.strip()

    context = ""
    for doc in search_results:
        context += f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

# Function to generate answer using LLM
def llm(prompt, generate_params=None):
    if generate_params is None:
        generate_params = {}

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(
        input_ids, 
        max_length=generate_params.get("max_length", 100),
        num_beams=generate_params.get("num_beams", 5),
        temperature=generate_params.get("temperature", 1.0),
        top_k=generate_params.get("top_k", 50),
    )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

# Function to perform RAG
def rag(query):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer

# Load the tokenizer and model
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")

# Streamlit interface
st.title("LLM Query Interface")

query = st.text_input("Enter your query:")
if st.button("Ask"):
    with st.spinner("Generating response..."):
        response = rag(query)
        st.write(response)
