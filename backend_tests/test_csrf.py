from django.test import TestCase

from books.models import Book

from .helpers import PASSWORD, csrf_client, fresh_csrf_token, make_user

LOGIN = {"username": "alice", "password": PASSWORD}
BOOK = {"title": "Dune", "author": "Frank Herbert"}


class CsrfTests(TestCase):
    """
    These tests use a client with enforce_csrf_checks=True, so they behave
    like a real browser. The other test files switch the check off to keep
    them short.
    """

    def setUp(self):
        make_user("alice")

    def test_csrf_endpoint_returns_token_and_sets_cookie(self):
        client = csrf_client()
        response = client.get("/api/csrf/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["csrfToken"])
        self.assertIn("csrftoken", response.cookies)

    def test_login_without_token_is_rejected_with_json_403(self):
        response = csrf_client().post("/api/login/", LOGIN)
        self.assertEqual(response.status_code, 403)
        self.assertIn("CSRF", response.json()["detail"])

    def test_login_with_token_succeeds(self):
        client = csrf_client()
        token = fresh_csrf_token(client)
        response = client.post("/api/login/", LOGIN, headers={"X-CSRFToken": token})
        self.assertEqual(response.status_code, 200)

    def test_register_without_token_is_rejected(self):
        response = csrf_client().post(
            "/api/register/", {"username": "bob", "password": PASSWORD}
        )
        self.assertEqual(response.status_code, 403)

    def _login(self, client):
        token = fresh_csrf_token(client)
        client.post("/api/login/", LOGIN, headers={"X-CSRFToken": token})

    def test_authenticated_write_without_token_is_rejected(self):
        client = csrf_client()
        self._login(client)
        response = client.post("/api/books/", BOOK)
        self.assertEqual(response.status_code, 403)
        self.assertIn("CSRF", response.json()["detail"])
        self.assertEqual(Book.objects.count(), 0)

    def test_authenticated_write_with_wrong_token_is_rejected(self):
        client = csrf_client()
        self._login(client)
        response = client.post("/api/books/", BOOK, headers={"X-CSRFToken": "wrong"})
        self.assertEqual(response.status_code, 403)

    def test_authenticated_write_with_valid_token_succeeds(self):
        client = csrf_client()
        self._login(client)
        token = fresh_csrf_token(client)
        response = client.post("/api/books/", BOOK, headers={"X-CSRFToken": token})
        self.assertEqual(response.status_code, 201)

    def test_token_from_before_login_is_rejected_after_login(self):
        """Django rotates the CSRF token at login, so an old token stops working."""
        client = csrf_client()
        old_token = fresh_csrf_token(client)
        client.post("/api/login/", LOGIN, headers={"X-CSRFToken": old_token})
        response = client.post("/api/books/", BOOK, headers={"X-CSRFToken": old_token})
        self.assertEqual(response.status_code, 403)

    def test_logout_needs_a_token_too(self):
        client = csrf_client()
        self._login(client)
        self.assertEqual(client.post("/api/logout/").status_code, 403)
        token = fresh_csrf_token(client)
        self.assertEqual(
            client.post("/api/logout/", headers={"X-CSRFToken": token}).status_code, 204
        )

    def test_safe_methods_never_need_a_token(self):
        self.assertEqual(csrf_client().get("/api/books/").status_code, 200)