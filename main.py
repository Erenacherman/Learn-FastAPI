from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    id: int
    title: str
    content: str

my_posts = []

def find_post(id: int):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index
    return None

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post_by_id(id: int):
    index = find_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} was not found"
        )
    return {"data": my_posts[index]}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} was not found"
        )
    
    post_dict = post.model_dump()
    my_posts[index] = post_dict
    return {"message": "Post updated successfully", "data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} was not found"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    