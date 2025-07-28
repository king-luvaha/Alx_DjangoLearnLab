from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet

# ✅ Set up the router
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Keep the original list-only endpoint (optional)
    path('books/', BookList.as_view(), name='book-list'),

    path('token/', obtain_auth_token, name='api-token'),  # ✅ Token login endpoint

    # ✅ Include router URLs for full CRUD support
    path('', include(router.urls)),
]
