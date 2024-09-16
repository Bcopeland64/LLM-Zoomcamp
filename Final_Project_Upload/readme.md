# NFL Rules Chatbot

This project implements a chatbot that answers questions about NFL rules using OpenAI's GPT model. It includes a FastAPI backend, a Dash monitoring dashboard, and a Streamlit frontend for user interaction.

## Features

- Answer questions about NFL rules using AI
- Secure API key input using getpass
- User-friendly Streamlit interface
- Real-time monitoring dashboard
- Feedback collection system
- In-memory storage for queries and feedback

## Prerequisites

- Python 3.7+
- OpenAI/Groq API key (used with getpass)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/nfl-rules-chatbot.git
   cd nfl-rules-chatbot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Backend

1. Start the main application:
   ```
   python main.py
   ```
   
   You will be prompted to enter your OpenAI API key securely when the application starts. The key is not stored and will need to be entered each time you start the application.

2. The backend API will be available at `http://localhost:8000`

### Running the Monitoring Dashboard

1. In a separate terminal, start the Dash monitoring dashboard:
   ```
   python dashboard.py
   ```

2. Access the dashboard at `http://localhost:8050`

### Running the Frontend

1. In another terminal, start the Streamlit frontend:
   ```
   streamlit run streamlit_app.py
   ```

2. Access the frontend in your web browser at `http://localhost:8501`

## API Endpoints

- `POST /query`: Send a question about NFL rules
  - Request body: `{"text": "Your question here"}`
  - Response: `{"response": "Answer to your question"}`

- `POST /feedback`: Submit feedback on a response
  - Request body: `{"query": "Original question", "response": "Bot's answer", "rating": 1}`
  - Response: `{"status": "Feedback recorded successfully"}`

- `GET /stats`: Retrieve usage statistics
  - Response: `{"total_queries": int, "total_feedback": int, "average_rating": float}`

## Project Structure

- `main.py`: FastAPI backend application (uses getpass for API key input)
- `dashboard.py`: Dash monitoring dashboard
- `streamlit_app.py`: Streamlit frontend application
- `requirements.txt`: List of Python dependencies

## Customization

- To modify the chatbot's behavior, edit the system message in `main.py`
- To change the dashboard layout or add more charts, edit `dashboard.py`
- To update the frontend design or add features, modify `streamlit_app.py`

## Security Note

This application uses `getpass` to securely input the OpenAI API key. The key is not stored anywhere in the application and is only held in memory while the application is running. You will need to input the key each time you start the application. This approach enhances security but may be less convenient for frequent restarts.

## Limitations

- This chatbot uses in-memory storage, so data is not persistent between restarts
- The current implementation doesn't include a full Retrieval-Augmented Generation (RAG) system
- The API key needs to be entered each time the application is started

## Running the Frontend

After starting the main application, run the Streamlit frontend:

```
streamlit run streamlit_app.py
```

Access the frontend in your web browser at `http://localhost:8501`
