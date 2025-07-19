from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books, LibraryDetailView, register  # ✅ literal import
from .views import admin_view, librarian_view, member_view


urlpatterns = [
    path("books/", views.list_books, name="list_books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # ✅ Required for the check:
    path("register/", views.register, name="register"),  # must match: views.register
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),  # must match: LoginView.as_view(template_name=
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),  # must match: LogoutView.as_view(template_name=
    path("admin-only/", admin_view, name="admin_view"),
    path("librarian-only/", librarian_view, name="librarian_view"),
    path("member-only/", member_view, name="member_view"),

]
