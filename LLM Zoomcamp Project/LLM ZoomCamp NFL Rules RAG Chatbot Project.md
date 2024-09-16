# NFL Rules RAG Chatbot

As I live overseas, many poeple ask me about this peculiar game of American Football, not to be confused with international football (that we Americans call Soccer). So, I thought I would create a RAG chatbot that can help anyone new to the game of football how to play, score, and learn the rules. I used the official NFL (National Football League) rulebook from 2023. Hopefully, this can help everyone around the world learn about this wonderful game that we Americans love so much!

### Prerequisites

Before beginning, ensure you have the following installed:
- Docker and Docker Compose
- Python 3.9 or higher (for local development)
- An OpenAI API key (required for the language model)

### Setting Things Up

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/yourusername/nfl-rules-rag-chatbot.git](https://github.com/Bcopeland64/LLM-Zoomcamp/tree/main/LLM%20Zoomcamp%20Project
   cd LLM-Zoomcamp Project
   ```

2. The project uses getpass to securely input your OpenAI/Groq API key at runtime. You don't need to set up any environment variables for the API key.

3. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

   This command will start three services:
   - The main chatbot application (available at http://localhost:8000)
   - The SQLite database
   - The monitoring dashboard (available at http://localhost:8050)

4. When the application starts, you'll be prompted to enter your OpenAI API key securely.

### Feeding the Bot NFL Rules Knowledge

To populate the chatbot with NFL rules data:

1. Place the NFL rules pdf data files (in JSON format) in the project directory.

2. Run the ingestion process:
   ```
   docker-compose run app python -m src.ingestion.ingest
   ```

   This will process your data and store it in the database.

### Chatting with the Bot

Once everything is up and running:

1. Open your web browser and go to http://localhost:8000/docs
2. You'll see a Swagger UI where you can interact with the chatbot
3. Try out the `/query` endpoint to ask questions about NFL rules!

### Monitoring Performance with the Dashboard

To view and interact with the monitoring dashboard:

1. Ensure that all Docker services are running (`docker-compose up`)
2. Open your web browser and navigate to http://localhost:8050
3. You'll see the dashboard with various charts and metrics, including:
   - User feedback over time
   - Query volume
   - Response times
   - Top queries
   - Error rates

The dashboard updates in real-time, allowing you to monitor the chatbot's performance as it's being used.

If you need to run the dashboard separately or restart it:

```
docker-compose run dashboard python src/monitoring/dashboard.py
```

This command will start the dashboard service independently of the main application.

### Running Tests

To ensure everything is working correctly:

```
docker-compose run app python -m unittest discover tests
```

This will run all the unit tests in the `tests/` directory.

### Evaluating Performance

To assess how well the chatbot is performing, run these evaluation scripts:

```
docker-compose run app python -m src.evaluation.retrieval_eval
docker-compose run app python -m src.evaluation.rag_eval
```

These will provide metrics on how well the retrieval and RAG systems are performing.

## API Key Security

This project uses the `getpass` module to securely handle the OpenAI API key. Instead of storing the key in environment variables or configuration files, the application will prompt you to enter the key when it starts up. This approach enhances security by ensuring the API key is not stored in plain text anywhere in the project.

## Troubleshooting

If you encounter any issues:
1. Ensure you're entering the correct OpenAI API key when prompted
2. Check the Docker logs for any error messages
3. Verify your data is in the correct format and location
4. If the dashboard isn't loading, ensure the dashboard service is running and check its logs
5. If problems persist, try restarting the services
