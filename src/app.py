import streamlit as st
import os
from graphs import create_blog_graph, create_translation_graph
from states import BlogState

st.set_page_config(
    page_title="YouTube to Blog",
    layout="centered"
)

st.title("YouTube to Blog")
st.caption("Convert a YouTube video into a blog post")

if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY not set")
    st.stop()

youtube_url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

if "result" not in st.session_state:
    st.session_state.result = None

if st.button("Generate Blog"):

    if not youtube_url:
        st.warning("Please enter a YouTube URL")
        st.stop()

    initial_state: BlogState = {
        "youtube_url": youtube_url,
        "video_id": None,
        "transcript": None,
        "title": None,
        "summary": None,
        "blog_content": None,
        "french_title": None,
        "french_summary": None,
        "french_blog_content": None,
        "error": None,
        "status": "initialized"
    }

    with st.spinner("Generating blog..."):
        app = create_blog_graph()
        for output in app.stream(initial_state):
            result = list(output.values())[0]

    if result.get("error"):
        st.error(result["error"])
        st.stop()

    st.session_state.result = result
    st.success("Blog generated")

if st.session_state.result:
    result = st.session_state.result
    
    st.header(result["title"])
    st.markdown(result["blog_content"])
    
    st.divider()
    
    if st.button("Translate to French"):
        with st.spinner("Translating to French..."):
            translation_app = create_translation_graph()
            translated_result = None
            
            for output in translation_app.stream(result):
                translated_result = list(output.values())[0]
            
            if translated_result.get("error"):
                st.error(translated_result["error"])
            else:
                st.session_state.result = translated_result
                st.success("Translation complete")
                st.rerun()
    
    if result.get("french_title"):
        st.divider()
        st.header("French Version")
        
        st.subheader(result["french_title"])
        st.markdown(result["french_blog_content"])