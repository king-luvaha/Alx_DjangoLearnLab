from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import SearchForm  # Add this form for input validation
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Securely handle user input using a Django form
    form = SearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        books = books.filter(title__icontains=query)

    # Secure response: template uses {% csrf_token %} in forms
    return render(request, 'books/book_list.html', {'books': books, 'form': form})
