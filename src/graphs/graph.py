from langgraph.graph import StateGraph, END
from states.states import BlogState
from nodes.nodes import (
    extract_video_id,
    fetch_transcript,
    generate_title_node,
    generate_summary_node,
    generate_blog_node,
    check_error,
    translate_to_french_node
)

def create_blog_graph():
    
    workflow = StateGraph(BlogState)
    workflow.add_node("fetch_transcript", fetch_transcript)
    workflow.add_node("generate_title", generate_title_node)
    workflow.add_node("generate_summary", generate_summary_node)
    workflow.add_node("generate_blog", generate_blog_node)
    
    workflow.set_entry_point("extract_video_id")
    
    
    workflow.add_conditional_edges(
        "fetch_transcript",
        check_error,
        {
            "continue": "generate_title",
            "error": END
        }
    )
    
    workflow.add_conditional_edges(
        "generate_title",
        check_error,
        {
            "continue": "generate_summary",
            "error": END
        }
    )
    
    workflow.add_conditional_edges(
        "generate_summary",
        check_error,
        {
            "continue": "generate_blog",
            "error": END
        }
    )
    
    workflow.add_conditional_edges(
        "generate_blog",
        check_error,
        {
            "continue": END,
            "error": END
        }
    )
    
    app = workflow.compile()
    
    return app
def create_translation_graph():
    
    workflow = StateGraph(BlogState)
    
    workflow.add_node("translate_to_french", translate_to_french_node)
    
    workflow.set_entry_point("translate_to_french")
    
    workflow.add_conditional_edges(
        "translate_to_french",
        check_error,
        {
            "continue": END,
            "error": END
        }
    )
    
    app = workflow.compile()
    
    return app