from typing import List, Dict
from src.retrieval.hybrid_search import HybridSearch
import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential

class RAGPipeline:
    def __init__(self, db_path: str, api_key: str):
        self.retriever = HybridSearch(db_path)
        openai.api_key = api_key

    def query(self, user_input: str) -> str:
        # Retrieve relevant documents
        docs = self.retriever.search(user_input, k=3)
        
        # Construct prompt
        prompt = self._construct_prompt(user_input, docs)
        
        # Generate response
        response = self._generate_response(prompt)
        
        return response

    def _construct_prompt(self, query: str, docs: List[Dict[str, str]]) -> str:
        context = "\n".join([doc['content'] for doc in docs])
        return f"""Given the following context:

{context}

Please answer the following question:
{query}

If the answer cannot be found in the given context, please say "I don't have enough information to answer that question." and suggest where the user might find the information.
"""

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
    def _generate_response(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the given context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
