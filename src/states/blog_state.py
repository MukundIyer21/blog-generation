from typing_extensions import TypedDict
from pydantic import BaseModel,Field
from typing import Optional
class Blog(BaseModel):
    title: str
    content: str

class BlogState(BaseModel):
    topic: str
    blog: Optional[Blog] = None