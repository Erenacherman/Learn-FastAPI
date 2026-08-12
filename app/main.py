from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mariadb


app = FastAPI()


# -----------------------------
# Database connection
# -----------------------------

try:
    conn = mariadb.connect(
        host="localhost",
        port=3306,
        user="root",
        password="lechu",
        database="fastapi"
    )

    cursor = conn.cursor()

    print("MariaDB successfully connected")

except mariadb.Error as e:
    print("Connecting to MariaDB failed")
    print("Error:", e)


# -----------------------------
# Pydantic model
# -----------------------------

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None


# -----------------------------
# CREATE
# -----------------------------

@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    try:
        query = """
            INSERT INTO posts (title, content, rating)
            VALUES (?, ?, ?)
        """

        values = (
            post.title,
            post.content,
            post.rating
        )

        cursor.execute(query, values)
        conn.commit()

        post_id = cursor.lastrowid

        return {
            "message": "Post created successfully",
            "data": {
                "id": post_id,
                "title": post.title,
                "content": post.content,
                "rating": post.rating
            }
        }

    except mariadb.Error as e:
        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )


# -----------------------------
# READ ALL
# -----------------------------

@app.get("/getall")
def get_all():

    try:
        cursor.execute(
            "SELECT id, title, content, rating FROM posts"
        )

        posts = cursor.fetchall()

        result = []

        for post in posts:
            result.append({
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "rating": post[3]
            })

        return {
            "data": result
        }

    except mariadb.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )


# -----------------------------
# READ ONE
# -----------------------------

@app.get("/getposts/{id}")
def get_post(id: int):

    try:
        cursor.execute(
            """
            SELECT id, title, content, rating
            FROM posts
            WHERE id = ?
            """,
            (id,)
        )

        post = cursor.fetchone()

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} was not found"
            )

        return {
            "data": {
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "rating": post[3]
            }
        }

    except mariadb.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )


# -----------------------------
# UPDATE
# -----------------------------

@app.put("/update/{id}")
def update_post(id: int, post: Post):

    try:

        # First check if post exists
        cursor.execute(
            "SELECT id FROM posts WHERE id = ?",
            (id,)
        )

        existing_post = cursor.fetchone()

        if existing_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} was not found"
            )

        # Update post
        cursor.execute(
            """
            UPDATE posts
            SET title = ?, content = ?, rating = ?
            WHERE id = ?
            """,
            (
                post.title,
                post.content,
                post.rating,
                id
            )
        )

        conn.commit()

        return {
            "message": "Post updated successfully",
            "data": {
                "id": id,
                "title": post.title,
                "content": post.content,
                "rating": post.rating
            }
        }

    except mariadb.Error as e:
        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )


# -----------------------------
# DELETE
# -----------------------------

@app.delete("/dlt/{id}")
def delete_post(id: int):

    try:

        # Check if post exists
        cursor.execute(
            """
            SELECT id, title, content, rating
            FROM posts
            WHERE id = ?
            """,
            (id,)
        )

        post = cursor.fetchone()

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} does not exist"
            )

        # Delete
        cursor.execute(
            "DELETE FROM posts WHERE id = ?",
            (id,)
        )

        conn.commit()

        return {
            "message": f"Post with id {id} deleted successfully",
            "data": {
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "rating": post[3]
            }
        }

    except mariadb.Error as e:
        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )