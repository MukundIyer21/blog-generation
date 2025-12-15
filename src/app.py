import streamlit as st
from graphs import create_blog_graph
from states import BlogState
import os

st.set_page_config(
    page_title="YouTube to Blog Generator",
    layout="wide"
)


st.title("YouTube to Blog Generator")
st.markdown("Convert any YouTube video into a well-structured blog post using AI")

with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1. Enter a YouTube video URL
    2. Click Generate Blog
    3. Wait for the AI to process
    4. Download or copy your blog
    
    **Requirements:**
    - Video must have captions/transcript
    - Set GROQ_API_KEY environment variable
    """)
    
    st.header("About")
    st.markdown("""
    This app uses:
    - LangGraph for workflow orchestration
    - Groq API with Llama for content generation
    - YouTube Transcript API for video data
    """)

if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY environment variable not set")
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    youtube_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        help="Enter the full YouTube video URL"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_button = st.button("Generate Blog", type="primary")

if generate_button and youtube_url:
    
    initial_state: BlogState = {
        "youtube_url": youtube_url,
        "video_id": None,
        "transcript": None,
        "title": None,
        "summary": None,
        "blog_content": None,
        "error": None,
        "status": "initialized"
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("Initializing workflow...")
        progress_bar.progress(10)
        
        app = create_blog_graph()
        
        status_text.text("Extracting video ID...")
        progress_bar.progress(20)
        
        result = None
        for i, output in enumerate(app.stream(initial_state)):
            node_name = list(output.keys())[0]
            node_output = output[node_name]
            
            if node_output["status"] == "video_id_extracted":
                status_text.text("Fetching transcript...")
                progress_bar.progress(30)
            elif node_output["status"] == "transcript_fetched":
                status_text.text("Generating title...")
                progress_bar.progress(50)
            elif node_output["status"] == "title_generated":
                status_text.text("Creating summary...")
                progress_bar.progress(65)
            elif node_output["status"] == "summary_generated":
                status_text.text("Generating full blog post...")
                progress_bar.progress(80)
            elif node_output["status"] == "completed":
                status_text.text("Blog generated successfully")
                progress_bar.progress(100)
            elif node_output["status"] == "error":
                break
            
            result = node_output
        
        progress_bar.empty()
        status_text.empty()
        
        if result and result.get("error"):
            st.markdown(f'<div class="error-box">Error: {result["error"]}</div>', unsafe_allow_html=True)
        
        elif result and result.get("blog_content"):
            st.markdown('<div class="success-box">Blog post generated successfully</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.header(result["title"])
            
            with st.expander("Summary", expanded=True):
                st.write(result["summary"])
            
            st.markdown("---")
            st.subheader("Full Blog Post")
            st.markdown(result["blog_content"])
            
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                st.download_button(
                    label="Download as TXT",
                    data=f"# {result['title']}\n\n{result['summary']}\n\n---\n\n{result['blog_content']}",
                    file_name="blog_post.txt",
                    mime="text/plain"
                )
            
            with col2:
                st.download_button(
                    label="Download as MD",
                    data=f"# {result['title']}\n\n{result['summary']}\n\n---\n\n{result['blog_content']}",
                    file_name="blog_post.md",
                    mime="text/markdown"
                )
        
    except Exception as e:
        st.markdown(f'<div class="error-box">Unexpected error: {str(e)}</div>', unsafe_allow_html=True)

elif generate_button:
    st.warning("Please enter a YouTube URL")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>Built with LangGraph, Groq & Streamlit</div>",
    unsafe_allow_html=True
)