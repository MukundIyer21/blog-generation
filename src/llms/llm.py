from langchain_groq import ChatGroq
import os

class LLMManager:
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.llm = ChatGroq(
            api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=4000
        )
    
    def generate_response(self, prompt: str) -> str:
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
    
    def generate_title(self, transcript: str) -> str:
        prompt = f"""Based on the following video transcript, generate a catchy and engaging blog post title. 
Only return the title, nothing else.

Transcript:
{transcript[:2000]}..."""
        
        return self.generate_response(prompt)
    
    def generate_summary(self, transcript: str) -> str:
        prompt = f"""Create a brief 2-3 sentence summary of the following video transcript.

Transcript:
{transcript[:3000]}..."""
        
        return self.generate_response(prompt)
    
    def generate_blog(self, transcript: str, title: str, summary: str) -> str:
        prompt = f"""Convert the following video transcript into a well-structured, engaging blog post.

Title: {title}
Summary: {summary}

Requirements:
- Write in a conversational yet professional tone
- Use proper headings and subheadings
- Include an introduction and conclusion
- Break content into digestible paragraphs
- Maintain the key points and insights from the video
- Make it engaging and readable

Transcript:
{transcript}

Generate the complete blog post:"""
        
        return self.generate_response(prompt)