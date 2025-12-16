from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()


class LLMManager:
    
    def __init__(self):     
        self.llm = ChatGroq(
            model="llama3-70b-8192",
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
        {transcript}..."""
        
        return self.generate_response(prompt)
    
    def generate_blog(self, transcript, title, summary):
        prompt = f"""Convert the following video transcript into a well-structured, engaging blog post.

        Title: {title}
        Summary: {summary}

        Transcript:
        {transcript}

        Generate the complete blog post:"""
        
        return self.generate_response(prompt)
    def translate_to_french(self, title, summary, blog_content):
        prompt = f"""Translate the following blog post into French. Maintain the same structure, tone, and formatting.

        Title: {title}
        Blog Content: {blog_content}

        Provide the translation in the following format:
        TITLE: [translated title]
        BLOG: [translated blog content]"""
                
        response = self.generate_response(prompt)
        
        parts = response.split("TITLE:", 1)
        if len(parts) < 2:
            raise Exception("Failed to parse translation response")
        
        rest = parts[1]
        title_part = rest.split("BLOG:", 1)
        french_title = title_part[0].strip()
        french_blog = title_part[1].strip()
        
        return {
            "french_title": french_title,
            "french_summary": None,
            "french_blog_content": french_blog
        }