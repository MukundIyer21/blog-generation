from typing import TypedDict, Optional

class BlogState(TypedDict):
    youtube_url: str
    transcript: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    blog_content: Optional[str]
    error: Optional[str]
    status: str