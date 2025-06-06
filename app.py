import os
import streamlit as st
import together
from dotenv import load_dotenv
import together

# Load env variables locally
load_dotenv()

# Function to check if the message is programming-related
def is_programming_query(query):
    programming_keywords = ['python', 'javascript', 'html', 'css', 'machine learning', 'deep learning',
                            'ai', 'algorithm', 'data structures', 'react', 'flask', 'django', 'c++', 'c#']
    return any(keyword.lower() in query.lower() for keyword in programming_keywords)

# Streamlit UI setup
st.set_page_config(page_title="Programming Bot", page_icon=":robot:", layout="centered")

# Header
st.markdown("""
    <h1 style='text-align: center; color: #0e76a8; font-size: 40px; font-family: Arial, sans-serif;'>
    Welcome to Programming Bot
    </h1>
    <p style='text-align: center; color: #555;'>Ask any programming-related questions and get answers!</p>
""", unsafe_allow_html=True)

# User input for query
user_query = st.text_input("Enter your programming question:", "", key="query", placeholder="e.g. How to create a Python function?")

# Submit button
submit_button = st.button("Get Answer", key="submit", help="Click to get the answer to your programming question")

if user_query and submit_button:
    if is_programming_query(user_query):
        # Locally from .env, in deployed app from Streamlit secrets
        api_key = os.getenv("TOGETHER_API_KEY") or st.secrets.get("TOGETHER_API_KEY")

        if not api_key:
            st.error("API Key is not loaded! Please check your .env file or Streamlit secrets.")
        else:
            client = together.Client(api_key=api_key)  # Agar class ka naam Client hai
            # client = together.Together(api_key=api_key)

            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[{
                    "role": "user",
                    "content": user_query
                }]
            )
            st.success(response.choices[0].message.content)
    else:
        st.warning("I am only a programming bot. Please ask programming-related questions.")

# Footer CSS + Markdown
footer = """
    <style>
        footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f0f2f6;
            color: #333333;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            border-top: 1px solid #e6e6e6;
            box-shadow: 0px -2px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #0078d4;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            cursor: pointer;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #005a9e;
        }
    </style>
    <footer>
        Developed by Abdul Rehman
    </footer>
"""
st.markdown(footer, unsafe_allow_html=True)
