from typing import TypedDict, Optional, NotRequired

class BlogState(TypedDict):
    topic: str
    title: Optional[str]
    content: Optional[str]
    language : str
    hindi_translation: Optional[str]
    french_translation: Optional[str]
