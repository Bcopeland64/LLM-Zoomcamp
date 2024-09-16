# NFL Rules Chatbot

I am constantly asked by students and friends from overseas about why American Football is so different than international football (what we call soccer), so I decided to make a chatbot that can help explain the game and the rules for people new to the sport. This project uses a RAG chatbot along with a streamlit frontend and uses Dash to monitor the metrics of the chatbot.

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
   git clone [https://github.com/yourusername/nfl-rules-chatbot.git](https://github.com/Bcopeland64/LLM-Zoomcamp/edit/main/Final_Project_Upload/)
   cd Final_Project_Upload
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

## Screenshots
![Screen_1](https://github.com/user-attachments/assets/a5c8f063-1868-4013-8f8e-8bf5199147e1)  ![Screen_2](https://github.com/user-attachments/assets/cb4e329d-5de9-4a5f-92c0-cb0e3dc56960)



