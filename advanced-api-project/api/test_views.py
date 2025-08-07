from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Quentin Tarantino")  # Create Author
        self.book1 = Book.objects.create(title="Django Unchained", author=self.author, year=2012)
        self.book2 = Book.objects.create(title="Pulp Fiction", author=self.author, year=1994)

        self.list_url = reverse("book-list")  # DRF viewset route name

    def test_create_book(self):
        data = {"title": "Clean Code", "author": "Robert C. Martin", "year": 2008}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.latest("id").title, "Clean Code")

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_update_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        updated_data = {"title": "Django Reloaded", "author": "Quentin", "year": 2014}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Django Reloaded")

    def test_delete_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {"author": "Greenfeld"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Greenfeld")

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url, {"search": "Django"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Django Unchained")

    def test_order_books_by_year_desc(self):
        response = self.client.get(self.list_url, {"ordering": "-year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data[0]["year"], response.data[1]["year"])

    def test_unauthenticated_access_denied(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # or 401 depending on your settings
