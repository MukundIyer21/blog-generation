from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    """Initialize and return the ChatGroq LLM instance."""
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-70b-versatile",
        temperature=0.7
    )
    return llm