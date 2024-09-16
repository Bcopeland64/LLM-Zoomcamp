from src.rag.rag_pipeline import RAGPipeline
from src.utils.db import Database
import random
from typing import List, Dict
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
import numpy as np

def get_test_queries(db_path: str, n: int = 50) -> List[Dict[str, str]]:
    with Database(db_path) as db:
        all_docs = db.fetchall("SELECT content FROM documents")
    
    test_queries = []
    for _ in range(n):
        doc = random.choice(all_docs)
        sentences = doc['content'].split('.')
        if len(sentences) > 1:
            question_sentence = random.choice(sentences).strip()
            remaining_sentences = [s.strip() for s in sentences if s != question_sentence]
            answer = random.choice(remaining_sentences)
            
            test_queries.append({
                'question': question_sentence,
                'reference_answer': answer
            })
    
    return test_queries

def evaluate_rag(db_path: str, api_key: str, test_queries: List[Dict[str, str]]):
    rag = RAGPipeline(db_path, api_key)
    rouge = Rouge()
    
    bleu_scores = []
    rouge_scores = []
    
    for query in test_queries:
        generated_answer = rag.query(query['question'])
        
        # Calculate BLEU score
        reference = [query['reference_answer'].split()]
        candidate = generated_answer.split()
        bleu = sentence_bleu(reference, candidate)
        bleu_scores.append(bleu)
        
        # Calculate ROUGE score
        rouge_score = rouge.get_scores(generated_answer, query['reference_answer'])[0]
        rouge_scores.append(rouge_score['rouge-l']['f'])
    
    avg_bleu = np.mean(bleu_scores)
    avg_rouge = np.mean(rouge_scores)
    
    print(f"Average BLEU score: {avg_bleu:.4f}")
    print(f"Average ROUGE-L score: {avg_rouge:.4f}")

if __name__ == "__main__":
    db_path = 'path/to/your/database.sqlite'
    api_key = 'your_openai_api_key'
    test_queries = get_test_queries(db_path)
    evaluate_rag(db_path, api_key, test_queries)
