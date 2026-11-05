from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import identify_hasher
from django.contrib.sessions.models import Session
from django.test import TestCase
from rest_framework.test import APIClient

from .helpers import PASSWORD, logged_in_client, make_user

User = get_user_model()


class RegistrationTests(TestCase):
    def test_register_creates_user_and_returns_201(self):
        response = APIClient().post(
            "/api/register/", {"username": "bob", "password": PASSWORD}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "bob")
        self.assertTrue(User.objects.filter(username="bob").exists())

    def test_response_never_contains_the_password(self):
        response = APIClient().post(
            "/api/register/", {"username": "bob", "password": PASSWORD}
        )
        self.assertNotIn("password", response.json())

    def test_password_is_hashed_not_plain_text(self):
        APIClient().post("/api/register/", {"username": "bob", "password": PASSWORD})
        user = User.objects.get(username="bob")
        self.assertNotEqual(user.password, PASSWORD)
        identify_hasher(user.password)  # raises ValueError if it is not a known hash format
        self.assertTrue(user.check_password(PASSWORD))

    def test_duplicate_username_is_rejected_case_insensitively(self):
        make_user("bob")
        response = APIClient().post(
            "/api/register/", {"username": "BOB", "password": PASSWORD}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.json())

    def test_weak_password_is_rejected(self):
        response = APIClient().post(
            "/api/register/", {"username": "bob", "password": "12345678"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())

    def test_missing_fields_are_rejected(self):
        response = APIClient().post("/api/register/", {"username": "bob"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["password"], ["This field is required."])


class LoginTests(TestCase):
    def setUp(self):
        self.user = make_user("alice")

    def test_login_success_returns_200_and_creates_session(self):
        client = APIClient()
        response = client.post(
            "/api/login/", {"username": "alice", "password": PASSWORD}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "alice")
        self.assertIn("sessionid", response.cookies)
        self.assertEqual(Session.objects.count(), 1)  # server-side record exists
        self.assertEqual(client.get("/api/me/").status_code, 200)

    def test_wrong_password_returns_401_and_no_session(self):
        response = APIClient().post(
            "/api/login/", {"username": "alice", "password": "nope"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("sessionid", response.cookies)
        self.assertEqual(Session.objects.count(), 0)

    def test_unknown_user_gets_same_401_message(self):
        wrong_pw = APIClient().post("/api/login/", {"username": "alice", "password": "x"})
        no_user = APIClient().post("/api/login/", {"username": "ghost", "password": "x"})
        self.assertEqual(no_user.status_code, 401)
        self.assertEqual(wrong_pw.json(), no_user.json())

    def test_inactive_user_cannot_log_in(self):
        make_user("sleepy", is_active=False)
        response = APIClient().post(
            "/api/login/", {"username": "sleepy", "password": PASSWORD}
        )
        self.assertEqual(response.status_code, 401)

    def test_missing_fields_return_400(self):
        response = APIClient().post("/api/login/", {"username": "alice"})
        self.assertEqual(response.status_code, 400)


class LogoutTests(TestCase):
    def test_logout_returns_204_and_ends_the_session(self):
        client = logged_in_client()
        self.assertEqual(client.get("/api/me/").status_code, 200)
        self.assertEqual(Session.objects.count(), 1)

        response = client.post("/api/logout/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Session.objects.count(), 0)  # server forgot the session
        self.assertEqual(client.get("/api/me/").status_code, 401)

    def test_old_session_cookie_is_useless_after_logout(self):
        client = logged_in_client()
        stolen_cookie = client.cookies["sessionid"].value
        client.post("/api/logout/")

        attacker = APIClient()
        attacker.cookies["sessionid"] = stolen_cookie
        self.assertEqual(attacker.get("/api/me/").status_code, 401)

    def test_logout_requires_authentication(self):
        self.assertEqual(APIClient().post("/api/logout/").status_code, 401)


class WhoAmITests(TestCase):
    def test_me_requires_login_and_sends_a_challenge_header(self):
        response = APIClient().get("/api/me/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["WWW-Authenticate"], "Session")