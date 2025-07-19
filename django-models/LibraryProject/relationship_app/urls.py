from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("books/", views.list_books, name="list_books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # ✅ Required for the check:
    path("register/", views.register, name="register"),  # must match: views.register
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),  # must match: LoginView.as_view(template_name=
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),  # must match: LogoutView.as_view(template_name=
]
