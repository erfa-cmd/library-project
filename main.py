from models import Book, Member, Library, Librarian

book1 = Book("The Lord of the Rings", "Tolkien", 5)
member1 = Member("Ali")
librarian1 = Librarian("Sara", "EMP001")

library = Library()
library.add_member(member1)
librarian1.add_new_book(library, book1)

# Save library data to a JSON file
library.save_to_file("data.json")

# Create a brand new empty Library and load data back from the file
new_library = Library()
new_library.load_from_file("data.json")

print("--- Loaded data ---")
for b in new_library.books:
    print(b)
for m in new_library.members:
    print(m)
