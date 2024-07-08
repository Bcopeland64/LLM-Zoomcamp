import os
import subprocess
import groq

# Set the Groq API key
groq.api_key = os.getenv("MY_API_KEY")

# Check if the ollama container exists and is running
try:
    result = subprocess.run("sudo docker inspect --format='{{.State.Running}}' ollama", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    if result.stdout.strip() == "false":
        subprocess.run("sudo docker start ollama", shell=True, check=True)
except subprocess.CalledProcessError:
    print("Starting the ollama container...")
    subprocess.run("sudo docker run -d --name ollama ollama/ollama", shell=True, check=True)

# Q1. Running Ollama with Docker
subprocess.run("sudo docker exec -it ollama ollama -v", shell=True, check=True)

# Q2. Downloading an LLM
subprocess.run("sudo docker exec -it ollama ollama pull gemma:2b", shell=True, check=True)

try:
    result = subprocess.run("sudo docker exec -it ollama cat /root/.ollama/models/manifests/registry.ollama.ai/library/gemma.json", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    content = result.stdout
    print(content)
except subprocess.CalledProcessError as e:
    print(f"Error executing docker exec command: {e}")

# Q3. Running the LLM
try:
    result = subprocess.run("sudo docker exec -it ollama bash -c 'ollama run -p \"10 * 10\"'", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = result.stdout
    print(output)
except subprocess.CalledProcessError as e:
    print(f"Error executing ollama run command: {e}")

# Q4. Downloading the weights
subprocess.run("sudo docker exec -it ollama ollama pull gemma:2b", shell=True, check=True)

result = subprocess.run("sudo docker exec -it ollama du -h /root/.ollama/models", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
size = result.stdout.strip().split()[0]
print(f"Size of /root/.ollama/models: {size}")

# Q5. Adding the weights
with open("Dockerfile", "w") as f:
    f.write("FROM ollama/ollama\n")
    f.write("COPY ./ollama_files /root/.ollama\n")

# Q6. Serving it
subprocess.run("sudo docker build -t ollama-gemma2b .", shell=True, check=True)

# Change the port to avoid conflict
try:
    subprocess.run("sudo docker run -it --rm -p 11435:11434 ollama-gemma2b", shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error executing docker run command: {e}")

# Make sure you're using the correct method from the `groq` module
prompt = "What's the formula for energy?"
try:
    response = groq.completions.create(
        model="ollama-gemma2b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )

    num_tokens = len(response.choices[0].message.content.split())
    print(f"Number of completion tokens: {num_tokens}")
except AttributeError as e:
    print(f"Error in groq module usage: {e}")
