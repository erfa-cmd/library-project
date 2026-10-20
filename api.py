from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_all_books, add_book, delete_book, update_quantity, search_books
from auth import create_users_table, hash_password, verify_password, get_user, create_access_token,  create_connection as auth_connection, get_current_user
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()


class BookCreate(BaseModel):
    title: str
    author: str
    quantity: int


class QuantityUpdate(BaseModel):
    quantity: int


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@app.get("/")
def home():
    return {"message": "Library API is running"}


@app.get("/books")
def read_books():
    rows = get_all_books()
    books = []
    for row in rows:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "quantity": row[3],
        })
    return books


@app.post("/books")
def create_book(book: BookCreate, current_user: str = Depends(get_current_user)):
    add_book(book.title, book.author, book.quantity)
    return {"message": f"Book '{book.title}' added"}


@app.put("/books/{book_id}")
def change_quantity(book_id: int, data: QuantityUpdate, current_user: str = Depends(get_current_user)):
    changed = update_quantity(book_id, data.quantity)
    if changed == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book {book_id} quantity set to {data.quantity}"}


@app.delete("/books/{book_id}")
def remove_book(book_id: int, current_user: str = Depends(get_current_user)):
    changed = delete_book(book_id)
    if changed == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book {book_id} deleted"}


@app.get("/books/search")
def find_books(keyword: str):
    rows = search_books(keyword)
    books = []
    for row in rows:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "quantity": row[3],
        })
    return books


@app.post("/register")
def register(user: UserCreate):
    conn = auth_connection()
    cursor = conn.cursor()

    hashed = hash_password(user.password)
    try:
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            (user.username, hashed)
        )
        conn.commit()
    except Exception:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    conn.close()
    return {"message": f"User '{user.username}' registered"}


@app.post("/login")
def login(from_data: OAuth2PasswordRequestForm = Depends()):
    row = get_user(from_data.username)
    if row is None:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    stored_hashed_password = row[2]
    if not verify_password(from_data.password, stored_hashed_password):
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    token = create_access_token(from_data.username)
    return {"access_token": token, "token_type": "bearer"}
