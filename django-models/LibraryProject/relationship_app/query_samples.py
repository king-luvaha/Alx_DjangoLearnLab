import os
import sys
import django

# Add the project base directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Clean slate for testing (optional)
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create sample data
author1 = Author.objects.create(name="George Orwell")
author2 = Author.objects.create(name="J.K. Rowling")

book1 = Book.objects.create(title="1984", author=author1)
book2 = Book.objects.create(title="Animal Farm", author=author1)
book3 = Book.objects.create(title="Harry Potter", author=author2)

library = Library.objects.create(name="Central Library")
library.books.add(book1, book3)

librarian = Librarian.objects.create(name="Alice", library=library)

# Query 1: All books by a specific author
print("Books by George Orwell:")
for book in Book.objects.filter(author=author1):
    print(f"- {book.title}")

# Query 2: List all books in a library
print("\nBooks in Central Library:")
for book in library.books.all():
    print(f"- {book.title}")

# Query 3: Retrieve the librarian for a library
librarian_for_library = Librarian.objects.get(library=library)
print(f"\nLibrarian for {library.name}: {librarian_for_library.name}")
