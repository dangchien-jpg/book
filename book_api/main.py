from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql",       
            user="root",      
            password="",       
            database="local_db"
        )
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Lỗi kết nối CSDL: {e}")

@app.post("/books/")
def create_book(book: Book):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = "INSERT INTO books (id, title) VALUES (%s, %s)"
        cursor.execute(query, (book.id, book.title))
        connection.commit()
        return {"message": "Book created successfully", "book": book}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {e}")
    finally:
        cursor.close()
        connection.close()

@app.get("/lookup_book/")
def lookup_book(title: str):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM books WHERE title = %s"
        cursor.execute(query, (title,))
        book = cursor.fetchone()
        
        if book:
            return book
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {e}")
    finally:
        cursor.close()
        connection.close()

@app.get("/books/")
def get_all_books():
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM books"
        cursor.execute(query)
        books = cursor.fetchall()
        
        if books:
            return books
        else:
            raise HTTPException(status_code=404, detail="No books found")
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {e}")
    finally:
        cursor.close()
        connection.close()

@app.put("/books/{id}")
def update_book(id: int, book: Book):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = "UPDATE books SET title = %s WHERE id = %s"
        cursor.execute(query, (book.title, id))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book updated successfully", "id": id}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {e}")
    finally:
        cursor.close()
        connection.close()

@app.delete("/books/{id}")
def delete_book(id: int):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = "DELETE FROM books WHERE id = %s"
        cursor.execute(query, (id,))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully", "id": id}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {e}")
    finally:
        cursor.close()
        connection.close()
