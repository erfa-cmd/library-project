import json


class Book:
    def __init__(self, title, author, quantity):
        self.title = title
        self.author = author
        self.quantity = quantity

    def __str__(self):
        return f"{self.title} by {self.author} — Available: {self.quantity}"


class Member:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def __str__(self):
        return f"{self.name} — Borrowed: {len(self.borrowed_books)} book(s)"


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def add_member(self, member):
        self.members.append(member)

    def borrow_book(self, member, book):
        if book.quantity > 0:
            book.quantity -= 1
            member.borrowed_books.append(book)
            print(f"{member.name} borrowed '{book.title}'")
        else:
            print(f"Sorry, '{book.title}' is not available.")

    def return_book(self, member, book):
        if book in member.borrowed_books:
            book.quantity += 1
            member.borrowed_books.remove(book)
            print(f"{member.name} returned '{book.title}'")
        else:
            print(f"{member.name} didn't borrow this book.")

    def save_to_file(self, filename):
        data = {
            "books": [
                {"title": b.title, "author": b.author, "quantity": b.quantity}
                for b in self.books
            ],
            "members": [
                {"name": m.name, "borrowed_titles": [
                    b.title for b in m.borrowed_books]}
                for m in self.members
            ]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Library data saved.")

    def load_from_file(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        self.books = [Book(b["title"], b["author"], b["quantity"])
                      for b in data["books"]]
        self.members = [Member(m["name"]) for m in data["members"]]
        print("Library data loaded.")


class Librarian(Member):
    def __init__(self, name, employee_id):
        super().__init__(name)
        self.employee_id = employee_id

    def add_new_book(self, library, book):
        library.add_book(book)
        print(f"Librarian {self.name} added a new book: '{book.title}'")
