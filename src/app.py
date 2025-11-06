import streamlit as st
from src.graphs.blog_graph import create_blog_graph
from src.states.blog_state import BlogState

st.set_page_config(page_title="AI Blog Generator", layout="centered")

st.title("AI Blog Generator using LangGraph + ChatGroq")


topic = st.text_input("Enter a blog topic:", placeholder="e.g., The Future of Quantum Computing")


if st.button("Generate Blog"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        st.info("Generating blog..")
        graph = create_blog_graph()
        initial_state = BlogState(topic=topic)
        title_placeholder = st.empty()
        content_placeholder = st.empty()

        title = ""
        content = ""

        for update in graph.stream(initial_state):
            state = update.get("generate_blog")
            if state and state.blog:
                title = state.blog.title
                content = state.blog.content
                title_placeholder.markdown(f"### 📝 {title}")
                content_placeholder.write(content)

        st.success("Blog generation complete!")
