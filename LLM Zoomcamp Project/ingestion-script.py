import os
import json
from typing import List, Dict
import numpy as np
from src.utils.db import Database
from sentence_transformers import SentenceTransformer

def load_documents(data_dir: str) -> List[Dict[str, str]]:
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            with open(os.path.join(data_dir, filename), 'r') as f:
                data = json.load(f)
                documents.extend(data)
    return documents

def compute_embedding(model: SentenceTransformer, text: str) -> np.ndarray:
    return model.encode(text)

def ingest_documents(db_path: str, data_dir: str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    documents = load_documents(data_dir)
    
    with Database(db_path) as db:
        for doc in documents:
            content = doc['content']
            embedding = compute_embedding(model, content)
            
            db.execute(
                "INSERT INTO documents (content, embedding) VALUES (?, ?)",
                (content, embedding.tobytes())
            )

if __name__ == "__main__":
    db_path = 'path/to/your/database.sqlite'
    data_dir = 'path/to/your/data/directory'
    ingest_documents(db_path, data_dir)
