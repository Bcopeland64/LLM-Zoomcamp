# hobbit_qa.py

import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from prometheus_client import start_http_server, Counter, Histogram
import time

# Load environment variables (make sure you have a .env file with your GROQ_API_KEY)
load_dotenv()

# Check if the API token is set
if "GROQ_API_KEY" not in os.environ:
    raise EnvironmentError("Please set the GROQ_API_KEY environment variable")

# Prometheus metrics
QUERY_COUNTER = Counter('hobbit_qa_queries_total', 'Total number of queries processed')
QUERY_LATENCY = Histogram('hobbit_qa_query_latency_seconds', 'Latency of query processing in seconds')

def load_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return text_splitter.split_text(text)

def create_vectorstore(splits):
    embeddings = HuggingFaceEmbeddings()
    return Chroma.from_texts(texts=splits, embedding=embeddings)

def setup_qa_chain(vectorstore):
    llm = ChatGroq(
        temperature=0.1,
        model_name="mixtral-8x7b-32768",
        max_tokens=512,
    )
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

def process_query(qa_chain, query):
    try:
        with QUERY_LATENCY.time():
            result = qa_chain({"query": query})
        return result["result"], result["source_documents"]
    except Exception as e:
        print(f"An error occurred while processing the query: {e}")
        return None, None

def main():
    # Start up the server to expose the metrics.
    start_http_server(8000)

    print("Loading and processing The Hobbit text...")
    hobbit_text = load_document('Hobbit, The - J. R. R. Tolkien.txt')
    splits = split_text(hobbit_text)
    vectorstore = create_vectorstore(splits)
    qa_chain = setup_qa_chain(vectorstore)

    print("\nWelcome to The Hobbit Q&A! Ask me anything about the book.")
    print("Please note that this system's knowledge is limited to the content of The Hobbit.")
    print("Type 'quit' to exit.")

    while True:
        user_query = input("\nYour question: ")
        if user_query.lower() == 'quit':
            break
        
        QUERY_COUNTER.inc()  # Increment the query counter
        answer, sources = process_query(qa_chain, user_query)
        if answer:
            print(f"\nAnswer: {answer}")
            print("\nSources:")
            for i, doc in enumerate(sources[:2], 1):
                print(f"Source {i}: {doc.page_content[:200]}...")
        else:
            print("Sorry, I couldn't process that query. Please try again.")

    print("Thank you for using The Hobbit Q&A. Goodbye!")

if __name__ == "__main__":
    main()