from typing import TypedDict, Optional

class BlogState(TypedDict):
    topic: str
    title: Optional[str]
    content: Optional[str]
    hindi_translation: Optional[str]
    french_translation: Optional[str]