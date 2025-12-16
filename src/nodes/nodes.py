from langchain_community.document_loaders import YoutubeLoader
import re
from states import BlogState
from llms.llm import LLMManager

llm_manager = LLMManager()


def fetch_transcript(state) :
    try:
        url = state["youtube_url"]
        
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
        docs = loader.load()
        
        full_transcript = " ".join([doc.page_content for doc in docs])
        
        state["transcript"] = full_transcript
        state["status"] = "transcript_fetched"
        
        return state
    except Exception as e:
        state["error"] = f"Error fetching transcript: {str(e)}. The video may not have captions available."
        state["status"] = "error"
        return state
def generate_title_node(state):
    try:
        transcript = state["transcript"]
        title = llm_manager.generate_title(transcript)
        
        state["title"] = title.strip()
        state["status"] = "title_generated"
        
        return state
    except Exception as e:
        state["error"] = f"Error generating title: {str(e)}"
        state["status"] = "error"
        return state

def generate_summary_node(state):
    try:
        transcript = state["transcript"]
        summary = llm_manager.generate_summary(transcript)
        
        state["summary"] = summary.strip()
        state["status"] = "summary_generated"
        
        return state
    except Exception as e:
        state["error"] = f"Error generating summary: {str(e)}"
        state["status"] = "error"
        return state

def generate_blog_node(state):
    try:
        transcript = state["transcript"]
        title = state["title"]
        summary = state["summary"]
        
        blog_content = llm_manager.generate_blog(transcript, title, summary)
        
        state["blog_content"] = blog_content.strip()
        state["status"] = "completed"
        
        return state
    except Exception as e:
        state["error"] = f"Error generating blog: {str(e)}"
        state["status"] = "error"
        return state

def check_error(state):
    if state.get("error"):
        return "error"
    return "continue"

def translate_to_french_node(state):
    try:
        title = state["title"]
        blog_content = state["blog_content"]
        
        translations = llm_manager.translate_to_french(title, blog_content)
        
        state["french_title"] = translations["french_title"]
        state["french_blog_content"] = translations["french_blog_content"]
        state["status"] = "translated"
        
        return state
    except Exception as e:
        state["error"] = f"Error translating to French: {str(e)}"
        state["status"] = "error"
        return state