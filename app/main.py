from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from .database import engine, get_db
from .model import Base, Post
from .schema import PostCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)


# -----------------------------
# CREATE
# -----------------------------

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db)
):

    new_post = Post(
        id=post.id,
        title=post.title,
        content=post.content
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "data": new_post
    }


# -----------------------------
# GET ALL POSTS
# -----------------------------

@app.get("/posts")
def get_posts(
    db: Session = Depends(get_db)
):

    posts = db.query(Post).all()

    return {
        "data": posts
    }


# -----------------------------
# GET ONE POST
# -----------------------------

@app.get("/posts/{id}")
def get_post_by_id(
    id: int,
    db: Session = Depends(get_db)
):

    post = (
        db.query(Post)
        .filter(Post.id == id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    return {
        "data": post
    }

# -----------------------------
# UPDATE
# -----------------------------

@app.put("/posts/{id}")
def update_post(
    id: int,
    post: PostCreate,
    db: Session = Depends(get_db)
):

    existing_post = (
        db.query(Post)
        .filter(Post.id == id)
        .first()
    )

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    existing_post.title = post.title
    existing_post.content = post.content

    db.commit()
    db.refresh(existing_post)

    return {
        "message": "Post updated successfully",
        "data": existing_post
    }


# -----------------------------
# DELETE
# -----------------------------

@app.delete(
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    id: int,
    db: Session = Depends(get_db)
):

    post = (
        db.query(Post)
        .filter(Post.id == id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    db.delete(post)
    db.commit()