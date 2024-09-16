import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(page_title="NFL Rules Chatbot", page_icon="🏈", layout="wide")

# Custom CSS for modern look with black background
st.markdown("""
<style>
    body {
        color: #FFFFFF;
        background-color: #000000;
    }
    .stTextInput > div > div > input {
        color: #FFFFFF;
        background-color: #333333;
    }
    .stButton>button {
        color: #FFFFFF;
        background-color: #0e76a8;
        border-radius: 20px;
    }
    .stTextArea > div > div > textarea {
        color: #FFFFFF;
        background-color: #333333;
    }
    .output-box {
        background-color: #1c1c1c;
        border: 1px solid #333333;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
    }
    .error-box {
        background-color: #3c1414;
        border: 1px solid #5c2626;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏈 NFL Rules Chatbot")

# Input section
user_question = st.text_input("Ask a question about NFL rules:", key="user_input")

# Output box
output_box = st.empty()

# Error box
error_box = st.empty()

# Button to submit question
if st.button("Get Answer"):
    if user_question:
        try:
            # Send request to backend
            response = requests.post("http://localhost:8000/query", 
                                     json={"text": user_question})
            
            if response.status_code == 200:
                answer = response.json()["response"]
                
                # Display answer in output box
                output_box.markdown(f"""
                <div class="output-box">
                    <h3>Answer:</h3>
                    <p>{answer}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Clear any previous errors
                error_box.empty()
                
                # Feedback section
                st.markdown("### Was this answer helpful?")
                col1, col2, col3 = st.columns([1,1,3])
                with col1:
                    if st.button("👍 Yes"):
                        feedback_response = requests.post("http://localhost:8000/feedback",
                                                          json={"query": user_question,
                                                                "response": answer,
                                                                "rating": 1})
                        if feedback_response.status_code == 200:
                            st.success("Thank you for your feedback!")
                with col2:
                    if st.button("👎 No"):
                        feedback_response = requests.post("http://localhost:8000/feedback",
                                                          json={"query": user_question,
                                                                "response": answer,
                                                                "rating": 0})
                        if feedback_response.status_code == 200:
                            st.success("Thank you for your feedback!")
            else:
                # Display error in error box
                error_details = response.json().get('detail', 'No detailed error message available')
                error_box.markdown(f"""
                <div class="error-box">
                    <h3>Error:</h3>
                    <p>Sorry, there was an error processing your request. Please try again.</p>
                    <p>Status code: {response.status_code}</p>
                    <p>Error details: {error_details}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Clear any previous output
                output_box.empty()
        except requests.exceptions.RequestException as e:
            # Display connection error in error box
            error_box.markdown(f"""
            <div class="error-box">
                <h3>Connection Error:</h3>
                <p>Unable to connect to the server. Please check if the backend is running.</p>
                <p>Error details: {str(e)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Clear any previous output
            output_box.empty()
    else:
        st.warning("Please enter a question.")

# Display some stats
st.sidebar.title("Chatbot Stats")
try:
    stats_response = requests.get("http://localhost:8000/stats")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        st.sidebar.metric("Total Queries", stats['total_queries'])
        st.sidebar.metric("Total Feedback", stats['total_feedback'])
        st.sidebar.metric("Average Rating", f"{stats['average_rating']:.2f}")
    else:
        st.sidebar.warning("Unable to fetch stats at the moment.")
except requests.exceptions.RequestException:
    st.sidebar.warning("Unable to connect to the server to fetch stats.")