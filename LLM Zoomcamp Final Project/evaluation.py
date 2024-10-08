import os
from dotenv import load_dotenv
from beyondllm.retrieve import auto_retriever
from beyondllm.source import fit
from langchain_groq import ChatGroq  # Use Groq model instead of OpenAI
from hobbit_qa import load_document, split_text, create_vectorstore, setup_qa_chain, process_query

# Load environment variables
load_dotenv()

# Check if the GROQ API token is set
if "GROQ_API_KEY" not in os.environ:
    raise EnvironmentError("Please set the GROQ_API_KEY environment variable")

# Load and process the Hobbit text
hobbit_text = load_document('Hobbit, The - J. R. R. Tolkien.txt')
splits = split_text(hobbit_text)
vectorstore = create_vectorstore(splits)
qa_chain = setup_qa_chain(vectorstore)

# Create a BeyondLLM-compatible data object
data = [{"text": split} for split in splits]  # Prepare data in a compatible format

# Create a BeyondLLM-compatible retriever
retriever = auto_retriever(data=data, type="normal", top_k=5)

# Set up the LLM for generating QA pairs using Groq model
llm = ChatGroq(
    model="mixtral-8x7b-32768",  # Replace with your specific Groq model name if needed
    api_key=os.environ["GROQ_API_KEY"],  # Use Groq API key here
    model_kwargs={"max_tokens": 512, "temperature": 0.1}
)

# Evaluate the retriever
retriever_results = retriever.evaluate(llm)
print("Retriever Evaluation Results:")
print(f"Hit Rate: {retriever_results['hit_rate']}")
print(f"MRR: {retriever_results['mrr']}")

# Custom evaluation function for the Hobbit QA system
def evaluate_hobbit_qa(qa_pairs, qa_chain):
    correct = 0
    total = len(qa_pairs)
    for question, expected_answer in qa_pairs:
        answer, _ = process_query(qa_chain, question)
        if answer and expected_answer.lower() in answer.lower():
            correct += 1
    accuracy = correct / total if total > 0 else 0
    return accuracy

# Generate QA pairs using the Groq model
qa_pairs = []
num_questions = 10  # You can adjust this number

for _ in range(num_questions):
    prompt = f"Generate a question and its short answer about the book 'The Hobbit' by J.R.R. Tolkien. Format: Q: [Question] A: [Answer]"
    response = llm(prompt)
    
    if response.startswith("Q:") and "A:" in response:
        question, answer = response.split("A:")
        question = question.replace("Q:", "").strip()
        answer = answer.strip()
        qa_pairs.append((question, answer))

# Evaluate the Hobbit QA system
hobbit_qa_accuracy = evaluate_hobbit_qa(qa_pairs, qa_chain)
print("\nHobbit QA System Evaluation:")
print(f"Accuracy: {hobbit_qa_accuracy:.2f}")

# Print out the QA pairs and the system's answers for manual inspection
print("\nDetailed QA Pairs and System Answers:")
for i, (question, expected_answer) in enumerate(qa_pairs, 1):
    system_answer, _ = process_query(qa_chain, question)
    print(f"\nQ{i}: {question}")
    print(f"Expected A: {expected_answer}")
    print(f"System A: {system_answer}")