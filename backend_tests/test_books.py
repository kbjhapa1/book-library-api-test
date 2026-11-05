from django.test import TestCase
from rest_framework.test import APIClient

from books.models import Book

from .helpers import logged_in_client, make_user

VALID_BOOK = {"title": "Dune", "author": "Frank Herbert", "published_year": 1965}


class ListAndRetrieveTests(TestCase):
    def setUp(self):
        self.owner = make_user("alice")
        self.book = Book.objects.create(title="Emma", author="Jane Austen", owner=self.owner)

    def test_anyone_can_list_books(self):
        response = APIClient().get("/api/books/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([b["title"] for b in response.json()], ["Emma"])

    def test_list_item_shape(self):
        item = APIClient().get("/api/books/").json()[0]
        self.assertEqual(
            set(item), {"id", "title", "author", "published_year", "owner", "created_at"}
        )
        self.assertEqual(item["owner"], "alice")

    def test_anyone_can_view_one_book(self):
        response = APIClient().get(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["author"], "Jane Austen")

    def test_unknown_book_id_returns_404(self):
        response = APIClient().get("/api/books/9999/")
        self.assertEqual(response.status_code, 404)

    def test_put_is_not_allowed(self):
        client = logged_in_client(self.owner)
        response = client.put(f"/api/books/{self.book.id}/", VALID_BOOK)
        self.assertEqual(response.status_code, 405)


class CreateTests(TestCase):
    def test_authenticated_user_can_create_and_becomes_owner(self):
        user = make_user("alice")
        client = logged_in_client(user)
        response = client.post("/api/books/", VALID_BOOK)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["owner"], "alice")
        self.assertEqual(Book.objects.get().owner, user)

    def test_anonymous_user_cannot_create(self):
        response = APIClient().post("/api/books/", VALID_BOOK)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Book.objects.count(), 0)

    def test_client_cannot_choose_the_owner(self):
        make_user("mallory")
        client = logged_in_client(make_user("alice"))
        response = client.post("/api/books/", {**VALID_BOOK, "owner": "mallory"})
        self.assertEqual(response.json()["owner"], "alice")

    def test_missing_title_returns_400(self):
        client = logged_in_client()
        response = client.post("/api/books/", {"author": "Someone"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["title"], ["This field is required."])

    def test_blank_title_returns_400(self):
        client = logged_in_client()
        response = client.post("/api/books/", {"title": "   ", "author": "Someone"})
        self.assertEqual(response.status_code, 400)

    def test_invalid_year_returns_400(self):
        client = logged_in_client()
        response = client.post("/api/books/", {**VALID_BOOK, "published_year": 99})
        self.assertEqual(response.status_code, 400)
        self.assertIn("published_year", response.json())

    def test_non_json_body_returns_415(self):
        client = logged_in_client()
        response = client.post("/api/books/", "title=Dune", content_type="text/plain")
        self.assertEqual(response.status_code, 415)


class DeleteTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")
        self.book = Book.objects.create(title="Emma", author="Jane Austen", owner=self.alice)
        self.url = f"/api/books/{self.book.id}/"

    def test_owner_can_delete_own_book(self):
        response = logged_in_client(self.alice).delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_other_user_gets_403_and_book_survives(self):
        response = logged_in_client(self.bob).delete(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())

    def test_anonymous_user_gets_401(self):
        response = APIClient().delete(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())

    def test_staff_can_delete_any_book(self):
        staff = make_user("admin", is_staff=True)
        response = logged_in_client(staff).delete(self.url)
        self.assertEqual(response.status_code, 204)

    def test_deleting_unknown_id_returns_404(self):
        response = logged_in_client(self.alice).delete("/api/books/9999/")
        self.assertEqual(response.status_code, 404)

    def test_book_without_owner_can_only_be_deleted_by_staff(self):
        orphan = Book.objects.create(title="Old", author="Nobody")
        self.assertEqual(logged_in_client(self.alice).delete(f"/api/books/{orphan.id}/").status_code, 403)
        staff = make_user("admin", is_staff=True)
        self.assertEqual(logged_in_client(staff).delete(f"/api/books/{orphan.id}/").status_code, 204)