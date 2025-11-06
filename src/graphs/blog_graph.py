from langgraph.graph import StateGraph,START,END
from src.states.blog_state import BlogState
from src.nodes.blog_node import generate_blog_node

def create_blog_graph():
    """
    Create a LangGraph graph that generates a blog.
    """
    graph = StateGraph(BlogState)
    graph.add_node("generate_blog", generate_blog_node)

    graph.set_entry_point("generate_blog")
    graph.add_edge("generate_blog", END)


    return graph.compile()
