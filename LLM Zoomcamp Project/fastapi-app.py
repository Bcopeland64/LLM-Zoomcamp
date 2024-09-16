from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from src.rag.rag_pipeline import RAGPipeline
from src.utils.db import Database, init_db
import getpass
import os
from typing import Dict

app = FastAPI()

class Query(BaseModel):
    text: str

class Feedback(BaseModel):
    query: str
    response: str
    rating: int

# Global variable to store the API key
api_key = None

def get_api_key():
    global api_key
    if api_key is None:
        api_key = getpass.getpass("Enter your OpenAI API key: ")
    return api_key

def get_db_path():
    return os.getenv('DB_PATH', 'nfl_rules_chatbot.sqlite')

def get_rag_pipeline():
    db_path = get_db_path()
    api_key = get_api_key()
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not provided")
    return RAGPipeline(db_path, api_key)

@app.on_event("startup")
async def startup_event():
    db_path = get_db_path()
    init_db(db_path)  # This function should create the necessary tables if they don't exist

@app.post("/query")
def query(query: Query, rag: RAGPipeline = Depends(get_rag_pipeline)) -> Dict[str, str]:
    try:
        response = rag.query(query.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
def feedback(fb: Feedback) -> Dict[str, str]:
    db_path = get_db_path()
    try:
        with Database(db_path) as db:
            db.execute(
                "INSERT INTO user_feedback (query, response, rating) VALUES (?, ?, ?)",
                (fb.query, fb.response, fb.rating)
            )
        return {"status": "Feedback recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)