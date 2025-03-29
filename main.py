from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg
import psycopg.rows
from typing import AsyncGenerator, Optional

app = FastAPI()

DATABASE_URL = "postgresql://postgres:1011@localhost:5432/mydatabase"

async def get_db() -> AsyncGenerator:
    async with await psycopg.AsyncConnection.connect(
        DATABASE_URL, row_factory=psycopg.rows.dict_row
    ) as conn:
        yield conn

# Models
class User(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class Form(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# User 
#create
@app.post("/users/")
async def create_user(user: User, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id",
            (user.username, user.email))
        user_id = await cur.fetchone()
        await db.commit()
    if not user_id:
        return {"status": "error", "message": "Failed to create user"}
    return {"id": user_id["id"], "message": "User created"}

#API to send back information
@app.get("/users/")
async def get_users(db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("SELECT * FROM users")
        users = await cur.fetchall()
    return users

#update
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "UPDATE users SET username = %s, email = %s WHERE id = %s RETURNING id",
            (user.username, user.email, user_id))
        updated = await cur.fetchone()
        await db.commit()
    if not updated:
        return {"status": "error", "message": "Failed to update user"}
    return {"message": "User updated"}

#delete
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id,))
        deleted = await cur.fetchone()
        await db.commit()
    if not deleted:
        return {"status": "error", "message": "Failed to delete user"}
    return {"message": "User deleted"}

# Form 
#create
@app.post("/forms/")
async def create_form(form: Form, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "INSERT INTO forms (title, description) VALUES (%s, %s) RETURNING id",
            (form.title, form.description))
        form_id = await cur.fetchone()
        await db.commit()
    if not form_id:
        return {"status": "error", "message": "Failed to create form"}
    return {"id": form_id["id"], "message": "Form created"}

@app.get("/forms/")
async def get_forms(db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("SELECT * FROM forms")
        forms = await cur.fetchall()
    return forms

#update
@app.put("/forms/{form_id}")
async def update_form(form_id: int, form: Form, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "UPDATE forms SET title = %s, description = %s WHERE id = %s RETURNING id",
            (form.title, form.description, form_id))
        updated = await cur.fetchone()
        await db.commit()
    if not updated:
        return {"status": "error", "message": "Failed to update form"}
    return {"message": "Form updated"}

#delete
@app.delete("/forms/{form_id}")
async def delete_form(form_id: int, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("DELETE FROM forms WHERE id = %s RETURNING id", (form_id,))
        deleted = await cur.fetchone()
        await db.commit()
    if not deleted:
        return {"status": "error", "message": "Failed to delete form"}
    return {"message": "Form deleted"}
