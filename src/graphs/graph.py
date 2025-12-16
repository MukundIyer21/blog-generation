from langgraph.graph import StateGraph, END
from src.states.states import BlogState
from src.nodes.nodes import (
    title_creation_node,
    content_generator_node,
    route_node,
    hindi_translation_node,
    french_translation_node,
    route_selector
)

def create_blog_graph():
    workflow = StateGraph(BlogState)
    
    workflow.add_node("title_creation", title_creation_node)
    workflow.add_node("content_generator", content_generator_node)
    workflow.add_node("route", route_node)
    workflow.add_node("hindi_translation", hindi_translation_node)
    workflow.add_node("french_translation", french_translation_node)
    workflow.set_entry_point("title_creation")
    
    workflow.add_edge("title_creation", "content_generator")
    workflow.add_edge("content_generator", "route")
   
    workflow.add_conditional_edges(
        "route",
        route_selector,
        {
            "english":END,
            "hindi":"hindi_translation",
            "french":"french_translation"
        }
    )

    workflow.add_edge("hindi_translation", END)
    workflow.add_edge("french_translation", END)
    
    return workflow.compile()