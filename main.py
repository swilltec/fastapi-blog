from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True



@app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    return {'data': f'{limit} blog list'}


@app.get('/blog/unpublished')
def unpublished_blogs():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def blog(id: int):
    return {'data': id}



@app.get('/blog/{id}/comments')
def single_blog(id, limit=10):
    return {'data': id}



@app.post("/blog/")
def create_blog(blog: Blog):
    return {"data": f"Blog is created with title as {blog.title}"}