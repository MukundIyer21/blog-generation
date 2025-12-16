from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from graphs.graph import create_blog_graph
import uvicorn

app = FastAPI()

class BlogRequest(BaseModel):
    topic: str

class BlogResponse(BaseModel):
    title: str
    content: str
    hindi_translation : Optional[str] = None    
    french_translation: Optional[str] = None   

@app.post("/blogs", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    try:
        graph = create_blog_graph()
        result = graph.invoke({"topic": request.topic,"language":"english"})
        
        return BlogResponse(
            title=result.get("title", ""),
            content=result.get("content", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blog: {str(e)}")

@app.post("/blogs/hindi", response_model=BlogResponse)
async def generate_blog_hindi(request: BlogRequest):
    try:
        graph = create_blog_graph()
        result = graph.invoke({"topic": request.topic,"language":"hindi"})
        
        return BlogResponse(
            title=result.get("title", ""),
            content=result.get("content", ""),
            hindi_translation=result.get("hindi_translation", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blog: {str(e)}")

@app.post("/blogs/french", response_model=BlogResponse)
async def generate_blog_french(request: BlogRequest):
    try:
        graph = create_blog_graph()
        result = graph.invoke({"topic": request.topic,"language":"french"})
        
        return BlogResponse(
            title=result.get("title", ""),
            content=result.get("content", ""),
            french_translation=result.get("french_translation", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blog: {str(e)}")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)