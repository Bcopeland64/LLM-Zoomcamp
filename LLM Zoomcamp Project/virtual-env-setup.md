# Setting Up a Virtual Environment for NFL Rules RAG Chatbot

## Prerequisites
- Python 3.9 or higher installed on your system
- `pip` (Python package installer) is up to date

## Steps

1. Open a terminal or command prompt

2. Navigate to your project directory:
   ```
   cd path/to/nfl-rules-rag-chatbot
   ```

3. Create a virtual environment:
   - On macOS and Linux:
     ```
     python3 -m venv venv
     ```
   - On Windows:
     ```
     python -m venv venv
     ```

4. Activate the virtual environment:
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```

5. Your prompt should change to indicate that the virtual environment is active. It might look something like:
   ```
   (venv) username@hostname:~/path/to/nfl-rules-rag-chatbot$
   ```

6. Install the project dependencies:
   ```
   pip install -r requirements.txt
   ```

7. You're now ready to run the project within this virtual environment!

## Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment:
```
deactivate
```

## Notes

- Remember to activate the virtual environment every time you work on the project.
- If you add or update dependencies, make sure to update the `requirements.txt` file:
  ```
  pip freeze > requirements.txt
  ```

- To delete the virtual environment, simply delete the `venv` directory.
