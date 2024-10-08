import streamlit as st
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.embeddings.base import Embeddings
from sklearn.feature_extraction.text import TfidfVectorizer

# Load environment variables
load_dotenv()

# Check if the API token is set
if "GROQ_API_KEY" not in os.environ:
    st.error("Please set the GROQ_API_KEY environment variable")
    st.stop()

class SKLearnEmbeddings(Embeddings):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def embed_documents(self, texts):
        return self.vectorizer.fit_transform(texts).toarray().tolist()

    def embed_query(self, text):
        return self.vectorizer.transform([text]).toarray()[0].tolist()

@st.cache_resource
def load_qa_system():
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
        embeddings = SKLearnEmbeddings()
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

    hobbit_text = load_document('Hobbit, The - J. R. R. Tolkien.txt')
    splits = split_text(hobbit_text)
    vectorstore = create_vectorstore(splits)
    qa_chain = setup_qa_chain(vectorstore)
    return qa_chain

def process_query(qa_chain, query):
    try:
        result = qa_chain({"query": query})
        return result["result"], result["source_documents"]
    except Exception as e:
        st.error(f"An error occurred while processing the query: {e}")
        return None, None

st.title("The Hobbit Q&A System")

st.write("Welcome to The Hobbit Q&A! Ask anything about the book.")
st.write("Please note that this system's knowledge is limited to the content of The Hobbit.")

# Initialize session state
if 'qa_chain' not in st.session_state:
    with st.spinner("Loading Q&A system..."):
        st.session_state.qa_chain = load_qa_system()

# Input box for the question
user_question = st.text_input("Enter your question:")

# Button to ask the question
if st.button("Ask"):
    if user_question:
        with st.spinner("Searching for an answer..."):
            answer, sources = process_query(st.session_state.qa_chain, user_question)
        
        if answer:
            st.subheader("Answer:")
            st.write(answer)
            
            st.subheader("Sources:")
            for i, doc in enumerate(sources[:2], 1):
                st.text_area(f"Source {i}", doc.page_content[:200], height=100)
        else:
            st.warning("Sorry, I couldn't process that query. Please try again.")
    else:
        st.warning("Please enter a question.")

st.markdown("---")
st.write("Thank you for using The Hobbit Q&A!")