from src.retrieval.hybrid_search import HybridSearch
from src.utils.db import Database
import random
from typing import List, Dict
from sklearn.metrics import ndcg_score
import numpy as np

def get_random_queries(db_path: str, n: int = 100) -> List[str]:
    with Database(db_path) as db:
        all_docs = db.fetchall("SELECT content FROM documents")
    
    queries = []
    for _ in range(n):
        doc = random.choice(all_docs)
        words = doc['content'].split()
        query_length = random.randint(3, 6)
        query = " ".join(random.sample(words, min(query_length, len(words))))
        queries.append(query)
    
    return queries

def evaluate_retrieval(db_path: str, queries: List[str], k: int = 10):
    searcher = HybridSearch(db_path)
    
    ndcg_scores = []
    for query in queries:
        results = searcher.search(query, k)
        
        # Assuming relevance is inversely proportional to the rank
        relevance = [1 / (i + 1) for i in range(len(results))]
        ideal = sorted(relevance, reverse=True)
        
        ndcg = ndcg_score([relevance], [ideal])
        ndcg_scores.append(ndcg)
    
    avg_ndcg = np.mean(ndcg_scores)
    print(f"Average NDCG@{k}: {avg_ndcg:.4f}")

if __name__ == "__main__":
    db_path = 'path/to/your/database.sqlite'
    queries = get_random_queries(db_path)
    evaluate_retrieval(db_path, queries)
