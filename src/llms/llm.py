from langchain_groq import ChatGroq
import os

class LLMManager:
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")        
        self.llm = ChatGroq(
            api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=4000
        )
    
    def generate_response(self, prompt) :
        response = self.llm.invoke(prompt)
        return response.content

    
    def generate_title(self, transcript: str) -> str:
        prompt = f"""Based on the following video transcript, generate a blog post title. 
Only return the title, nothing else.

Transcript:
{transcript}..."""
        
        return self.generate_response(prompt)
    
    def generate_summary(self, transcript):
        prompt = f"""Create a brief paragraph summary of the following video transcript.

Transcript:
{transcript[:3000]}..."""
        
        return self.generate_response(prompt)
    
    def generate_blog(self, transcript, title, summary):
        prompt = f"""Convert the following video transcript into a well-structured, engaging blog post.

Title: {title}
Summary: {summary}

Transcript:
{transcript}

Generate the complete blog post:"""
        
        return self.generate_response(prompt)