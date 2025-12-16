from typing import TypedDict, Optional

class BlogState(TypedDict):
    youtube_url: str
    video_id: Optional[str]
    transcript: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    blog_content: Optional[str]
    french_title: Optional[str]
    french_summary: Optional[str]
    french_blog_content: Optional[str]
    error: Optional[str]
    status: str