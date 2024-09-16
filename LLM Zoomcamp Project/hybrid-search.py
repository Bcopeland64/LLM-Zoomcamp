import numpy as np
from typing import List, Dict
from src.utils.db import Database
from sentence_transformers import SentenceTransformer

class HybridSearch:
    def __init__(self, db_path: str, model_name: str = 'all-MiniLM-L6-v2'):
        self.db_path = db_path
        self.model = SentenceTransformer(model_name)

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.model.encode(query)
        
        with Database(self.db_path) as db:
            # Semantic search
            semantic_results = db.fetchall('''
                SELECT id, content, embedding
                FROM documents
                ORDER BY cosine_similarity(embedding, ?) DESC
                LIMIT ?
            ''', (query_embedding.tobytes(), k))

            # Text search
            text_results = db.fetchall('''
                SELECT id, content
                FROM documents
                WHERE content MATCH ?
                LIMIT ?
            ''', (query, k))

        # Combine and rank results
        combined_results = self._combine_results(semantic_results, text_results)
        return combined_results[:k]

    def _combine_results(self, semantic_results: List[Dict], text_results: List[Dict]) -> List[Dict]:
        combined = {}
        for i, result in enumerate(semantic_results):
            combined[result['id']] = {'score': 1 / (i + 1), 'content': result['content']}
        
        for i, result in enumerate(text_results):
            if result['id'] in combined:
                combined[result['id']]['score'] += 1 / (i + 1)
            else:
                combined[result['id']] = {'score': 1 / (i + 1), 'content': result['content']}
        
        return sorted(combined.values(), key=lambda x: x['score'], reverse=True)

def cosine_similarity(a: bytes, b: bytes) -> float:
    a_vec = np.frombuffer(a, dtype=np.float32)
    b_vec = np.frombuffer(b, dtype=np.float32)
    return np.dot(a_vec, b_vec) / (np.linalg.norm(a_vec) * np.linalg.norm(b_vec))
