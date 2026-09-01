from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
import mariadb


app = FastAPI()


# -----------------------------
# Database connection
# -----------------------------

def get_db_connection():
    try:
        connection = mariadb.connect(
            host="localhost",
            port=3306,
            user="root",
            password="mariadb_password",
            database="fastapi"
        )

        return connection

    except mariadb.Error as e:
        print(f"Database connection error: {e}")
        raise


# -----------------------------
# Pydantic model
# -----------------------------

class Post(BaseModel):
    id: int
    title: str
    content: str


# -----------------------------
# CREATE
# -----------------------------

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        query = """
            INSERT INTO posts (id, title, content)
            VALUES (?, ?, ?)
        """

        cursor.execute(
            query,
            (post.id, post.title, post.content)
        )

        connection.commit()

        return {
            "data": {
                "id": post.id,
                "title": post.title,
                "content": post.content
            }
        }

    except mariadb.IntegrityError:

        connection.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Post with id {post.id} already exists"
        )

    finally:
        cursor.close()
        connection.close()


# -----------------------------
# GET ALL POSTS
# -----------------------------

@app.get("/posts")
def get_posts():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            "SELECT id, title, content FROM posts"
        )

        posts = cursor.fetchall()

        return {
            "data": posts
        }

    finally:
        cursor.close()
        connection.close()


# -----------------------------
# GET ONE POST
# -----------------------------

@app.get("/posts/{id}")
def get_post_by_id(id: int):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        query = """
            SELECT id, title, content
            FROM posts
            WHERE id = ?
        """

        cursor.execute(query, (id,))

        post = cursor.fetchone()

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} was not found"
            )

        return {
            "data": post
        }

    finally:
        cursor.close()
        connection.close()


# -----------------------------
# UPDATE
# -----------------------------

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        query = """
            UPDATE posts
            SET title = ?, content = ?
            WHERE id = ?
        """

        cursor.execute(
            query,
            (post.title, post.content, id)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} was not found"
            )

        connection.commit()

        return {
            "message": "Post updated successfully",
            "data": {
                "id": id,
                "title": post.title,
                "content": post.content
            }
        }

    finally:
        cursor.close()
        connection.close()


# -----------------------------
# DELETE
# -----------------------------

@app.delete(
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(id: int):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        query = """
            DELETE FROM posts
            WHERE id = ?
        """

        cursor.execute(query, (id,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} was not found"
            )

        connection.commit()

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    finally:
        cursor.close()
        connection.close()