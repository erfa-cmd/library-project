import sqlite3


def create_connection():
    conn = sqlite3.connect("library.db")
    return conn


def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()


def add_book(title, author, quantity):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
        (title, author, quantity)
    )
    conn.commit()
    conn.close()
    print(f"book '{title}' added to database.")


def get_all_books():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_books(keywords):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?" ,
        (f"%{keywords}%" , f"%{keywords}%")
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_quantity(book_id, new_quantity):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE books SET quantity = ? WHERE id = ?",
        (new_quantity, book_id)
    )
    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed


def delete_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed


if __name__ == "__main__":
    create_table()
    add_book("Test Book", "Test Author", 1)

    books = get_all_books()
    for book in books:
        print(book)

    last_id = books[-1][0]
    delete_book(last_id)

    print("After delete:")
    for book in get_all_books():
        print(book)
