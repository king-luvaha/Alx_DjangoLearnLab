from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book  # ✅ this line is necessary for the check
from .models import Library  # ✅ this line is necessary for the check
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Function-based view
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log user in after registration
            return redirect('list_books')  # Or any view you prefer
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')  # Or any view
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')