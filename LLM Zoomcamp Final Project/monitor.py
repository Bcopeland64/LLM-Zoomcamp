from beyondllm import source, retrieve, generator, llms, embeddings
import os
from openinference.instrumentation.openai import OpenAIInstrumentor
from phoenix.otel import register

# Assuming Groq API key environment variable is set
os.environ['GROQ_API_KEY'] = 'gr-****'

# Initialize OpenTelemetry tracer provider
tracer_provider = register()

# Instrument the OpenAI (or Groq in your case) SDK with OpenInference
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

# Instead of Observer, manually track observability with OpenTelemetry
# (This is your custom wrapper to manage the observability process)

# Using Groq LLM and embeddings model instead of OpenAI
llm = llms.ChatGroqModel()  # Groq-based model for LLM
embed_model = embeddings.GroqEmbeddings()  # Groq embeddings model

# Fit the data source using your local file path
data = source.fit("/home/brandon/Documents/brandon/LLM Zoomcamp/Project_v4/Hobbit, The - J. R. R. Tolkien.txt", 
                  dtype="text", chunk_size=512, chunk_overlap=50)

# Create a retriever with the Groq embedding model
retriever = retrieve.auto_retriever(data, embed_model, type="normal", top_k=4)

# Generate a response using the updated pipeline
pipeline = generator.Generate(question="Who is Gandalf?", retriever=retriever, llm=llm)

# Manually trigger observability here if needed
# (e.g., track requests, usage, etc., using tracer)
