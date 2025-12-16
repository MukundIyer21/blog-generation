from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.graphs.graph import create_blog_graph
import uvicorn

app = FastAPI()

class BlogRequest(BaseModel):
    topic: str

class BlogResponse(BaseModel):
    title: str
    content: str
    hindi_translation: str
    french_translation: str

@app.post("/blogs", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    try:
        graph = create_blog_graph()
        result = graph.invoke({"topic": request.topic})
        
        return BlogResponse(
            title=result.get("title", ""),
            content=result.get("content", ""),
            hindi_translation=result.get("hindi_translation", ""),
            french_translation=result.get("french_translation", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blog: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)