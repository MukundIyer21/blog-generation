from langchain_core.messages import HumanMessage
from src.llms.groq_llm import get_llm
from src.states.blog_state import Blog, BlogState

def generate_blog_node(state: BlogState) -> BlogState:
    """
    Node that generates a blog given a topic.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(Blog)

    prompt = f"Write a detailed blog about the topic '{state.topic}'. Include a creative title and engaging content."
    response = structured_llm.invoke([HumanMessage(content=prompt)])

    state.blog = response
    return state
