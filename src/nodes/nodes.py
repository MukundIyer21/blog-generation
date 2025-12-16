from src.states.states import BlogState
from src.llms.llm import get_llm

def title_creation_node(state):
    llm = get_llm()
    topic = state["topic"]
    
    prompt = f"""Create a catchy and engaging blog title for the following topic: {topic}    
    Respond with ONLY the title, no additional text."""
    
    title = llm.invoke(prompt).content.strip()
    state["title"] = title
    return state

def content_generator_node(state):
    llm = get_llm()
    topic = state["topic"]
    title = state["title"]
    
    prompt = f"""Write a comprehensive blog post on the following topic: {topic}
    Blog Title: {title}    
    Write the blog content:"""
    
    content = llm.invoke(prompt).content.strip()
    state["content"] = content
    return state

def route_node(state):
    return state

def route_selector(state):
    if state["language"]=="hindi":
        return "hindi"
    if state["language"]=="french":
        return "french"
    return "english"
    
def hindi_translation_node(state):
    llm = get_llm()
    title = state["title"]
    content = state["content"]
    
    prompt = f"""Translate the following blog post to Hindi. Maintain the tone and style.
    
    Title: {title}
    
    Content:
    {content}
    
    Provide the Hindi translation (include both title and content):"""
    
    hindi_translation = llm.invoke(prompt).content.strip()
    state["hindi_translation"] = hindi_translation
    return state

def french_translation_node(state):
    llm = get_llm()
    title = state["title"]
    content = state["content"]
    
    prompt = f"""Translate the following blog post to French. Maintain the tone and style.
    
    Title: {title}
    
    Content:
    {content}
    
    Provide the French translation (include both title and content):"""
    
    french_translation = llm.invoke(prompt).content.strip()
    state["french_translation"] = french_translation
    return state