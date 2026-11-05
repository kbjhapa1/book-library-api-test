from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

PASSWORD = "S3cure-Lab-Passw0rd!"


def make_user(username="alice", password=PASSWORD, **extra):
    return User.objects.create_user(
        username=username, 
        password=password, 
        **extra)


def logged_in_client(user=None):
    """A client that already has a session cookie (CSRF checks are OFF here)."""
    user = user or make_user()
    client = APIClient()
    assert client.login(username=user.username, password=PASSWORD)
    return client


def csrf_client():
    """A client that behaves like a real browser: CSRF checks are ON."""
    return APIClient(enforce_csrf_checks=True)


def fresh_csrf_token(client):
    """Ask the API for a token (this also stores the csrftoken cookie in the client)."""
    return client.get("/api/csrf/").json()["csrfToken"]