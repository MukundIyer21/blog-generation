from youtube_transcript_api import YouTubeTranscriptApi
import re
from states import BlogState
from llm import LLMManager

llm_manager = LLMManager()

def extract_video_id(state: BlogState) -> BlogState:
    try:
        url = state["youtube_url"]
        
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'^([0-9A-Za-z_-]{11})$'
        ]
        
        video_id = None
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                break
        
        if not video_id:
            state["error"] = "Invalid YouTube URL"
            state["status"] = "error"
        else:
            state["video_id"] = video_id
            state["status"] = "video_id_extracted"
        
        return state
    except Exception as e:
        state["error"] = f"Error extracting video ID: {str(e)}"
        state["status"] = "error"
        return state

def fetch_transcript(state: BlogState) -> BlogState:
    try:
        video_id = state["video_id"]
        
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        full_transcript = " ".join([item["text"] for item in transcript_list])
        
        state["transcript"] = full_transcript
        state["status"] = "transcript_fetched"
        
        return state
    except Exception as e:
        state["error"] = f"Error fetching transcript: {str(e)}. The video may not have captions available."
        state["status"] = "error"
        return state

def generate_title_node(state: BlogState) -> BlogState:
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

def generate_summary_node(state: BlogState) -> BlogState:
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

def generate_blog_node(state: BlogState) -> BlogState:
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

def check_error(state: BlogState) -> str:
    if state.get("error"):
        return "error"
    return "continue"