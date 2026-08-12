from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import random

many_posts = [{"id":1,"titile":"Mahabarath","content":"nothing"},
              {"id":2,"title":"KingofKotha","content":"this also nothing"}]

def find_post(id):
    for post in many_posts:
        if post["id"] == id:
            return id

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None

app = FastAPI()

@app.post("/")
def root(post:Post):
    post_dict = post.dict()
    post_dict['id'] = random.randint(1,1000)
    print(post_dict)
    return post_dict

@app.get("/getposts/{id}")
def get_post(id:int):
    post = find_post(id)
    return f"This is your content {post['content']} for {id} "

@app.get("/getall")
def get_all():
    return f"data : {many_posts}"

@app.delete("/dlt/{id}")
def delete(id):
    many_posts.
    return many_posts