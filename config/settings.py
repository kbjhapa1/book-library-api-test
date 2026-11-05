"""
Django settings for the Book Library API lab.

LAB ONLY: these values are chosen for learning on your own computer.
They are NOT safe for a real deployment.
"""
import os
from pathlib import Path
from typing import Any
import sys 

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-lab-only-do-not-use-in-production"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "rest_framework",
    "books",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        # LAB_DB_PATH lets us point the server at a separate throwaway database later.
        "NAME": os.environ.get("LAB_DB_PATH", BASE_DIR / "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework: speak JSON only (no browsable HTML API).
REST_FRAMEWORK: dict[str, Any] = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
}


# ---------------------------------------------------------------------------
# PHASE 3 ADDITIONS: authentication, sessions, CSRF
# ---------------------------------------------------------------------------
REST_FRAMEWORK.update(
    {
        # Who are you?  Look for a Django session cookie.
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "books.authentication.SessionAuthentication401",
        ],
        # Secure by default: every view needs a logged-in user unless it says otherwise.
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
        # Lets APIClient in our tests send JSON without repeating format="json".
        "TEST_REQUEST_DEFAULT_FORMAT": "json",
    }
)

# When Django's CSRF check fails, answer with JSON instead of an HTML page.
CSRF_FAILURE_VIEW = "books.views.csrf_failure"

SESSION_COOKIE_HTTPONLY = True   # JavaScript cannot read the session cookie (default, stated for teaching)
SESSION_COOKIE_SAMESITE = "Lax"  # browser will not send it on most cross-site POSTs (default)
CSRF_COOKIE_SAMESITE = "Lax"

# ---------------------------------------------------------------------------
# PHASE 4 ADDITIONS: HTTPS
# ---------------------------------------------------------------------------
# "Secure" cookies are only sent by clients over HTTPS connections.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Over HTTPS, Django also checks the Origin (or Referer) header of unsafe
# requests. This lists the web origins we accept besides the request's own host.
CSRF_TRUSTED_ORIGINS = ["https://localhost:8443"]

# ---------------------------------------------------------------------------
# PHASE 5 ADDITIONS: faster tests
# ---------------------------------------------------------------------------
# Password hashing is deliberately SLOW (that is what protects real passwords).
# During `manage.py test` we swap in a fast hasher so 40+ tests do not take
# half a minute. Never do this outside of tests.
if "test" in sys.argv:
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]