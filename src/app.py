import streamlit as st
import os
from graphs import create_blog_graph
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
        "error": None,
        "status": "initialized"
    }

    with st.spinner("Generating blog..."):
        app = create_blog_graph()
        result = None

        for output in app.stream(initial_state):
            result = list(output.values())[0]

    if result.get("error"):
        st.error(result["error"])
        st.stop()

    st.success("Blog generated")

    st.header(result["title"])

    st.subheader("Summary")
    st.write(result["summary"])

    st.subheader("Blog")
    st.markdown(result["blog_content"])
