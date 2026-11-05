# Django Book Library API — Hands-On Lab Workbook

### Authentication · Sessions · HTTPS · API Testing

**Student edition** · 8 labs · about 12–16 hours · Windows PowerShell

> **Your goal:** understand the system well enough to *explain and test* authentication, sessions, cookies, HTTPS certificates and APIs on your own — not just to copy commands.

---

## Table of Contents

0. [Read me first](#0-read-me-first)
1. [Lab 0 — Architecture and design decisions](#lab-0--architecture-and-design-decisions)
2. [Lab 1 — Django project and your first endpoint](#lab-1--django-project-and-your-first-endpoint)
3. [Lab 2 — The Book model and CRUD](#lab-2--the-book-model-and-crud)
4. [Lab 3 — Users, sessions, CSRF and permissions](#lab-3--users-sessions-csrf-and-permissions)
5. [Lab 4 — Local HTTPS and certificates](#lab-4--local-https-and-certificates)
6. [Lab 5 — Backend unit and API behavior tests](#lab-5--backend-unit-and-api-behavior-tests)
7. [Lab 6 — Playwright API tests with TypeScript](#lab-6--playwright-api-tests-with-typescript)
8. [Lab 7 — Inspecting network traffic](#lab-7--inspecting-network-traffic)
9. [Lab 8 — README, troubleshooting and wrap-up](#lab-8--readme-troubleshooting-and-wrap-up)
10. [Appendices](#appendices)

---

## 0. Read me first

### 0.1 What you will build

A small **Book Library API**. People can register, log in, look at books, add books, delete *their own* books and log out. The API speaks JSON over **HTTPS**, remembers logged-in users with **session cookies**, and is protected by **permissions** and **CSRF checks**. You then test it twice:

| Test suite | Tool | Talks to | Question it answers |
|---|---|---|---|
| **Backend tests** | Django test framework + DRF `APIClient` | The Django code *in memory* (no network) | "Is my code correct?" |
| **API tests** | Playwright + TypeScript (`APIRequestContext` only) | The *running* server over real HTTPS | "Does the deployed system behave correctly, including TLS, cookies and headers?" |

> Playwright is used **only to send HTTP requests**. There are no browser pages, locators or UI automation anywhere in this project.

### 0.2 How to use this workbook

Every lab has the same shape:

| Icon | Section | What you do |
|---|---|---|
| 🎯 | **Objectives** | Read what you should be able to do afterwards. |
| 📖 | **Concepts** | Read *before* touching code. The code will make sense afterwards. |
| 📁 | **Files** | Why each file exists. |
| 🛠️ | **Build it** | Create files and run commands. Type or paste, then *read what you pasted*. |
| 👀 | **Expected output** | Compare with your screen. |
| 🧪 | **Exercises** | Practice. Answers are hidden in collapsible blocks — try first! |
| 🚑 | **Common errors** | Look here when something breaks. |
| ✅ | **Checkpoint** | A gate. **Do not start the next lab until every box is ticked.** |

**Rules of the game**

1. **One lab at a time.** Each lab builds on a working previous lab.
2. **Read the "why" before the "how".** If you can't explain a file, re-read its section.
3. **Break things on purpose** (the exercises tell you how). You learn the most from error messages you caused yourself.
4. **Write your own answers** in the *Lab journal* lines before opening the answer blocks.

> **Working with an AI tutor or instructor?** Do one lab at a time, run the commands, and report the output. Say *"Lab N complete"* only when the checkpoint passes. The tutor should not unlock Lab N+1 before that.

### 0.3 Progress tracker

Copy this table into your notes and tick as you go.

| Lab | Topic | Done |
|---|---|---|
| 0 | Architecture and design decisions | ☐ |
| 1 | Django project + health endpoint | ☐ |
| 2 | Book model + CRUD | ☐ |
| 3 | Users, sessions, CSRF, permissions | ☐ |
| 4 | Local HTTPS + certificates | ☐ |
| 5 | Backend tests | ☐ |
| 6 | Playwright API tests | ☐ |
| 7 | Network inspection | ☐ |
| 8 | README + wrap-up | ☐ |

### 0.4 Prerequisites

Check each tool in **Windows PowerShell** (right-click Start → *Windows PowerShell* or *Terminal*):

```powershell
python --version      # 3.12 or newer recommended (3.10+ works)
node --version        # 20 or newer (22 LTS is fine)
npm --version
curl.exe --version    # ships with Windows 10/11
openssl version       # needed in Lab 4 (see Lab 4 if this fails)
code --version        # optional: VS Code
```

| Tool | Where to get it |
|---|---|
| Python | <https://www.python.org/downloads/> — tick **"Add python.exe to PATH"** in the installer |
| Node.js | <https://nodejs.org/> (LTS) |
| OpenSSL | Included with **Git for Windows** (`C:\Program Files\Git\usr\bin\openssl.exe`), or `winget install ShiningLight.OpenSSL.Light` |
| VS Code | <https://code.visualstudio.com/> — a good editor makes copy-paste safer |

### 0.5 Conventions used in this workbook

* **Always run commands from the project root** (`book-library-lab`) unless a step says otherwise.
* **`curl.exe`, never `curl`.** In Windows PowerShell 5.1 the word `curl` is an *alias* for a different command (`Invoke-WebRequest`). Typing `.exe` gets the real curl.
* **JSON bodies go in files.** PowerShell mangles double quotes passed to programs, so we write the JSON to a small file in `scratch\` and send it with `--data "@scratch/file.json"`. Always write such files with `-Encoding ascii` (see the 🚑 table in Lab 2 for why).
* **Two terminals.** Later labs run the server in **Terminal A** and everything else in **Terminal B**. Each terminal needs the virtual environment activated.
* Code blocks marked `powershell` are for PowerShell. Blocks marked `python`, `typescript`, `json` are file contents.

### 0.6 Tested with

| Component | Version tested |
|---|---|
| Python | 3.12 |
| Django | 6.1.2 (5.2 LTS also expected to work) |
| Django REST Framework | 3.18.3 |
| uvicorn | 0.54.0 |
| Node.js | 22 LTS |
| `@playwright/test` | 1.64.1 |
| TypeScript | 7.0.2 |

If your versions are newer, small differences in wording of error messages are normal. The *concepts and status codes* will not change.

---

# Lab 0 — Architecture and design decisions

### 🎯 Objectives

* Describe what happens, step by step, when a client calls the API.
* Say which parts of the system are **Django-specific** and which are **general web concepts**.
* Explain the permission design of the library: *who may do what*.

### 📖 Concepts

#### 0.A The big picture

```text
 CLIENT                                  SERVER (one Python process)
 (browser, curl.exe,             ┌────────────────────────────────────────────────────┐
  Playwright)                    │  uvicorn  ── speaks HTTPS, hands requests to Django │
     │                           │     │                                              │
     │  HTTPS request            │     ▼                                              │
     │  ─────────────────────▶   │  MIDDLEWARE   security headers, session lookup,    │
     │  method + URL + headers   │               CSRF check, "who is request.user?"   │
     │  + cookies + JSON body    │     │                                              │
     │                           │     ▼                                              │
     │                           │  URL ROUTING  /api/books/  →  BookListCreateView   │
     │                           │     │                                              │
     │                           │     ▼                                              │
     │                           │  DRF VIEW     authentication → permissions         │
     │                           │     │         → serializer (validate input)        │
     │                           │     ▼                                              │
     │                           │  MODEL / ORM  Book, User, Session  ⇄  SQLite file  │
     │  HTTPS response           │     │                                              │
     │  ◀─────────────────────   │     ▼                                              │
     │  status + headers         │  RESPONSE     status code + JSON + Set-Cookie       │
     │  + cookies + JSON body    └────────────────────────────────────────────────────┘
```

#### 0.B The life of one request — `POST /api/books/`

1. The client opens a TLS connection, verifies the server certificate, and sends the request (Lab 4).
2. **SessionMiddleware** reads the `sessionid` cookie and loads the server-side session.
3. **AuthenticationMiddleware** attaches `request.user` (a real user, or `AnonymousUser`).
4. **URL routing** picks `BookListCreateView`.
5. DRF **authentication** class checks the session user *and* the CSRF token for unsafe methods.
6. DRF **permission** classes decide: allowed (continue), `401` (not logged in) or `403` (not allowed).
7. The **serializer** validates the JSON → `400` with field errors if invalid.
8. The **model** saves a row in SQLite; the view sets `owner = request.user`.
9. DRF renders JSON and sends **`201 Created`**.

#### 0.C Design decision: who owns books?

We chose a **shared public catalogue with owners**:

| Action | Anonymous | Logged in (not owner) | Owner | Staff user |
|---|---|---|---|---|
| List / view books | ✅ 200 | ✅ 200 | ✅ 200 | ✅ 200 |
| Add a book | ❌ 401 | ✅ 201 | ✅ 201 | ✅ 201 |
| Delete a book | ❌ 401 | ❌ 403 | ✅ 204 | ✅ 204 |

*Why this design?* Reading books is harmless and public. Writing needs an identity (**authentication**). Deleting needs *the right* identity (**authorization**: you may only delete what you own). It is small, secure by default, and gives us all of `401`, `403` and `404` to study. Books with no owner (created in Lab 2, before owners existed) can only be deleted by staff.

#### 0.D The API contract

| Method + URL | Purpose | Success | Typical errors |
|---|---|---|---|
| `GET /api/health/` | Is the server alive? | 200 | — |
| `GET /api/csrf/` | Get a CSRF token (+ cookie) | 200 | — |
| `POST /api/register/` | Create a user | 201 | 400, 403 (CSRF) |
| `POST /api/login/` | Start a session | 200 | 400, 401, 403 (CSRF) |
| `POST /api/logout/` | End the session | 204 | 401, 403 (CSRF) |
| `GET /api/me/` | Who am I? | 200 | 401 |
| `GET /api/books/` | List books | 200 | — |
| `GET /api/books/{id}/` | One book | 200 | 404 |
| `POST /api/books/` | Add a book | 201 | 400, 401, 403 |
| `DELETE /api/books/{id}/` | Remove a book | 204 | 401, 403, 404 |

**Differences from the original brief (documented on purpose):** three small extra endpoints (`/api/health/`, `/api/csrf/`, `/api/me/`) make the system easier to test and teach; bad credentials return **401** rather than 400; there is no update (`PUT`/`PATCH`) endpoint, so those return **405 Method Not Allowed**.

#### 0.E Django-specific or general?

| Idea | General web concept | How *Django/DRF* does it |
|---|---|---|
| HTTP methods, status codes, headers | ✅ universal | DRF `Response(..., status=...)` |
| Cookies | ✅ universal (browser feature) | `Set-Cookie` from Django |
| Server-side session | ✅ common pattern | `django.contrib.sessions`, table `django_session` |
| Session cookie name `sessionid` | ❌ Django-specific | `SESSION_COOKIE_NAME` |
| CSRF attack + token idea | ✅ universal | `csrftoken` cookie + `X-CSRFToken` header |
| Origin/Referer check over HTTPS | ✅ general defense | `CsrfViewMiddleware` |
| Password hashing | ✅ universal | PBKDF2 (default) via `create_user()` |
| Serializer / validation | General idea | DRF `serializers.Serializer` |
| TLS and certificates | ✅ universal, not Django at all | Handled by **uvicorn**, not Django |

### ✅ Checkpoint 0

- [ ] I can draw the request path from client to database without looking.
- [ ] I can explain why a non-owner deleting a book gets **403** but an anonymous visitor gets **401**.
- [ ] I know that Django's own `runserver` will **not** be used for HTTPS in this project.

**Lab journal:** In one sentence, what is the difference between *authentication* and *authorization*?

`______________________________________________`

---

# Lab 1 — Django project and your first endpoint

### 🎯 Objectives

* Create a Django project and an app, inside an isolated virtual environment.
* Explain what an HTTP request and response look like on the wire.
* Return JSON from one simple endpoint and call it with `curl.exe`.

### 📖 Concepts

#### 1.A HTTP in two minutes

HTTP is plain text sent between a client and a server. A **request** has a *method*, a *path*, *headers* and an optional *body*:

```http
GET /api/health/ HTTP/1.1
Host: 127.0.0.1:8000
Accept: application/json
```

A **response** has a *status code*, *headers* and an optional *body*:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Allow: GET, OPTIONS

{"status":"ok"}
```

| Part | Direction | Examples | Purpose |
|---|---|---|---|
| Method | request | `GET`, `POST`, `DELETE` | What do you want to do? |
| URL / path | request | `/api/books/7/` | Which thing? |
| **Request headers** | client → server | `Content-Type`, `Cookie`, `X-CSRFToken`, `Origin` | Information *about the request* |
| **Request body** | client → server | `{"title":"Dune"}` | The data being sent |
| Status code | server → client | `200`, `404` | Did it work? |
| **Response headers** | server → client | `Content-Type`, `Set-Cookie`, `ETag` | Information *about the response* |
| **Response body** | server → client | `{"id":7,...}` | The result |

#### 1.B Project vs app (Django vocabulary)

* A **project** (`config/`) holds *settings* and the top-level URL list.
* An **app** (`books/`) holds one feature: models, views, URLs.

#### 1.C How Django answers a request

`URL → view → response`. The URL list says "`/api/health/` is handled by the function `health`". The function returns a `Response`. **Django REST Framework (DRF)** adds tools on top of Django for building JSON APIs: parsers, renderers, serializers, permissions.

### 📁 Files you will create or change

| File | Why it exists |
|---|---|
| `requirements.txt` | Lists the Python packages so anyone can recreate your setup. |
| `config/settings.py` | All project-wide configuration. |
| `config/urls.py` | The top-level URL map: everything under `api/` goes to the `books` app. |
| `books/urls.py` | The app's own URL map. |
| `books/views.py` | The code that runs for each URL. |

### 🛠️ Build it

**Step 1 — Create the project folder and a virtual environment**

A *virtual environment* is a private copy of Python and its packages for one project, so projects don't interfere with each other.

```powershell
cd $HOME\Documents
mkdir book-library-lab
cd book-library-lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Your prompt should now start with `(.venv)`.

**Step 2 — Create `requirements.txt`** (open the folder in VS Code with `code .`)

**`requirements.txt`**

```text
# Tested with: Django 6.1.2, djangorestframework 3.18.3, uvicorn 0.54.0
# (Django 6 needs Python 3.12+; on older Python pip will pick Django 5.2, which also works.)
Django>=5.2,<7
djangorestframework>=3.16,<4
uvicorn>=0.30,<1
```

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Step 3 — Create the Django project and the `books` app**

```powershell
django-admin startproject config .
python manage.py startapp books
Remove-Item books\tests.py
```

> The **dot** in `startproject config .` matters: it creates the project in the current folder instead of a nested one. We delete `books\tests.py` because our tests live in their own folder in Lab 5.

**Step 4 — Replace `config/settings.py` completely** with this version. Read the comments — every line has a reason.

```python
"""
Django settings for the Book Library API lab.

LAB ONLY: these values are chosen for learning on your own computer.
They are NOT safe for a real deployment.
"""
import os
from pathlib import Path

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
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
}
```

**Step 5 — Replace `config/urls.py`**

**`config/urls.py`**

```python
from django.urls import include, path

urlpatterns = [
    path("api/", include("books.urls")),
]
```

**Step 6 — Replace `books/views.py`** (Phase 1 version)

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(request):
    """Phase 1: the simplest possible endpoint."""
    return Response({"status": "ok"})
```

**Step 7 — Create `books/urls.py`** (Phase 1 version)

```python
from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
]
```

**Step 8 — Prepare the database and start the server**

```powershell
python manage.py check
python manage.py migrate
python manage.py runserver
```

Leave it running. Open a **second** PowerShell window (Terminal B), `cd` to the project, activate `.venv`, and call the endpoint:

```powershell
curl.exe -i http://127.0.0.1:8000/api/health/
```

> `-i` means "also show the response headers". Stop the server any time with **Ctrl+C**.

### 👀 Expected output

`python manage.py check`:

```text
System check identified no issues (0 silenced).
```

`curl.exe -i ...` (header order and values will differ a little):

```text
HTTP/1.1 200 OK
Date: Thu, 22 Oct 2026 21:05:11 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Type: application/json
Allow: GET, OPTIONS
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

{"status":"ok"}
```

In the server window you will see one line per request, for example:

```text
[22/Oct/2026 21:05:11] "GET /api/health/ HTTP/1.1" 200 15
```

### 🔍 What just happened?

1. `curl.exe` sent `GET /api/health/`.
2. `config/urls.py` matched `api/` and passed the rest (`health/`) to `books/urls.py`.
3. That matched `health/` → the function `health`.
4. DRF's `@api_view(["GET"])` made sure only `GET` is allowed, ran the function, converted the dict to JSON, and set `Content-Type: application/json`.

### 🧪 Exercises

**1.1** Request a URL that does not exist: `curl.exe -i http://127.0.0.1:8000/api/nothing/`. What status do you get, and *which part of the system* produced it?

<details><summary>Answer</summary>

`404 Not Found`. It came from **Django's URL resolver**: no pattern matched, so no view ever ran. (You see a long HTML page because `DEBUG = True`; with `DEBUG = False` it would be a short page.)
</details>

**1.2** Send the wrong method: `curl.exe -i -X POST http://127.0.0.1:8000/api/health/`. What status and body? Which header tells you what *is* allowed?

<details><summary>Answer</summary>

`405 Method Not Allowed` with body `{"detail":"Method \"POST\" not allowed."}`. The **`Allow: GET, OPTIONS`** response header lists the permitted methods.
</details>

**1.3** Add a new endpoint `GET /api/hello/<name>/` that returns `{"message": "Hello, <name>!"}`. Test it with `curl.exe`.

<details><summary>Answer</summary>

In `books/views.py`:

```python
@api_view(["GET"])
def hello(request, name):
    return Response({"message": f"Hello, {name}!"})
```

In `books/urls.py` add: `path("hello/<str:name>/", views.hello, name="hello"),`

Test: `curl.exe http://127.0.0.1:8000/api/hello/Ada/` → `{"message":"Hello, Ada!"}`.

Remove the `hello` endpoint afterwards (or keep it; later labs do not depend on it being absent, but our final project does not include it).
</details>

### 🚑 Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'django'` | Virtual environment not active | Run `.\.venv\Scripts\Activate.ps1`; prompt must show `(.venv)` |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | PowerShell execution policy | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, answer **Y**, retry |
| `python` opens the Microsoft Store | Python not installed/on PATH | Install from python.org with "Add to PATH", or use `py -3.12 ...` |
| `django-admin` is not recognized | `.venv` not active | Activate the venv |
| `DisallowedHost at /` | You used a host name not in `ALLOWED_HOSTS` | Use `127.0.0.1` or `localhost` |
| `Error: That port is already in use.` | Another server runs on 8000 | `python manage.py runserver 8001` (adjust URLs) |
| `/api/health` (no trailing slash) answers 301 | Django adds the slash for you | Use `/api/health/` |

### ✅ Checkpoint 1

- [ ] `python manage.py check` prints *no issues*.
- [ ] `curl.exe -i http://127.0.0.1:8000/api/health/` returns `200` and `{"status":"ok"}`.
- [ ] I did exercises 1.1 and 1.2 and can explain `404` vs `405`.
- [ ] I can explain: project vs app; request vs response headers.

**Lab journal:** What is the difference between a request header and a response header? Give one example of each.

`______________________________________________`


---

# Lab 2 — The Book model and CRUD

### 🎯 Objectives

* Explain what a **model**, a **migration** and a **serializer** are.
* Implement **C**reate, **R**ead (list + one) and **D**elete over HTTP, with correct status codes.
* Spot the security problem we are leaving open *on purpose* (and fix it in Lab 3).

### 📖 Concepts

**Model** — a Python class that describes one database table. `Book` becomes the table `books_book`; each attribute becomes a column. The *ORM* (object-relational mapper) lets you write `Book.objects.all()` instead of SQL.

**Migration** — a small script that changes the database to match your models. It is a **two-step** process:

1. `makemigrations` — Django *compares your models to the migration history* and writes a new migration file.
2. `migrate` — Django *runs* the unapplied migrations against the database.

Migration files are code you commit to Git; the database file (`db.sqlite3`) is data you do not.

**Serializer** — the translator between Python objects and JSON, *and* the gatekeeper for input. It decides which fields are visible, which are read-only, and whether incoming data is valid (`400 Bad Request` if not).

**Generic views** — DRF ships ready-made views for common patterns:

| Class | HTTP methods it offers |
|---|---|
| `ListCreateAPIView` | `GET` (list), `POST` (create) |
| `RetrieveDestroyAPIView` | `GET` (one), `DELETE` |

Because we picked `RetrieveDestroyAPIView` — not `RetrieveUpdateDestroyAPIView` — `PUT` and `PATCH` are *not offered*: they answer `405`. Offering less is a security feature.

**Status codes you will produce in this lab**

| Code | Name | When |
|---|---|---|
| 200 | OK | A successful read |
| 201 | Created | A new book was stored |
| 204 | No Content | Deleted; there is nothing to send back |
| 400 | Bad Request | Invalid or missing JSON fields |
| 404 | Not Found | No book with that id |
| 405 | Method Not Allowed | e.g. `PUT` on a book |

> ⚠️ **Heads-up:** in this lab *anyone* can add and delete books. That is intentional scaffolding. Lab 3 closes the hole.

### 📁 Files

| File | Why it exists |
|---|---|
| `books/models.py` | Defines the `Book` table. |
| `books/serializers.py` | Converts `Book` ⇄ JSON and validates input. |
| `books/views.py` | One view for the collection (`/books/`), one for a single book (`/books/<id>/`). |
| `books/urls.py` | Maps the two URLs to the two views. |
| `books/migrations/0001_initial.py` | *Generated* by Django. Don't write it by hand. |

### 🛠️ Build it

**Step 1 — Replace `books/models.py`**

```python
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    published_year = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.title} by {self.author}"
```

`null=True, blank=True` means the year is optional. `auto_now_add=True` stamps the creation time automatically. `ordering = ["id"]` makes list order predictable.

**Step 2 — Create `books/serializers.py`**

```python
from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "published_year", "created_at"]
        read_only_fields = ["id", "created_at"]
```

`read_only_fields` means clients can *see* `id` and `created_at` but cannot set them.

**Step 3 — Replace `books/views.py`**

```python
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


class BookListCreateView(generics.ListCreateAPIView):
    """GET /api/books/ -> list.  POST /api/books/ -> create."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveDestroyAPIView):
    """GET /api/books/<id>/ -> one book.  DELETE -> remove it."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Step 4 — Replace `books/urls.py`**

```python
from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("books/", views.BookListCreateView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
]
```

**Step 5 — Create and apply the migration** (stop the server with Ctrl+C first, or use Terminal B)

```powershell
python manage.py makemigrations books
python manage.py sqlmigrate books 0001
python manage.py migrate
python manage.py runserver
```

`sqlmigrate` is optional but fascinating: it prints the SQL that migration will run.

**Step 6 — Try every endpoint** (Terminal B, project root, venv active)

Create small JSON files in a `scratch` folder (it is already in `.gitignore` — create `.gitignore` now, see Appendix A):

```powershell
mkdir scratch
Set-Content -Path scratch\dune.json -Encoding ascii -Value '{"title":"Dune","author":"Frank Herbert","published_year":1965}'
Set-Content -Path scratch\bad.json  -Encoding ascii -Value '{"author":"No Title Here"}'
```

Then, one at a time:

```powershell
# CREATE  -> expect 201
curl.exe -i -X POST http://127.0.0.1:8000/api/books/ -H "Content-Type: application/json" --data "@scratch/dune.json"

# CREATE with invalid data -> expect 400
curl.exe -i -X POST http://127.0.0.1:8000/api/books/ -H "Content-Type: application/json" --data "@scratch/bad.json"

# LIST -> expect 200
curl.exe -i http://127.0.0.1:8000/api/books/

# READ ONE -> expect 200
curl.exe -i http://127.0.0.1:8000/api/books/1/

# DELETE -> expect 204
curl.exe -i -X DELETE http://127.0.0.1:8000/api/books/1/

# READ the deleted one -> expect 404
curl.exe -i http://127.0.0.1:8000/api/books/1/

# PUT -> expect 405
curl.exe -i -X PUT http://127.0.0.1:8000/api/books/2/ -H "Content-Type: application/json" --data "@scratch/dune.json"
```

(Create one or two books again before you run the last commands, so there is something to find.)

### 👀 Expected output

Create (`201`):

```text
HTTP/1.1 201 Created
Content-Type: application/json
Allow: GET, POST, HEAD, OPTIONS
...

{"id":1,"title":"Dune","author":"Frank Herbert","published_year":1965,"created_at":"2026-10-22T21:06:07.606558Z"}
```

Invalid create (`400`) — the body names the broken field:

```text
HTTP/1.1 400 Bad Request
...
{"title":["This field is required."]}
```

Delete (`204`) has **no body**:

```text
HTTP/1.1 204 No Content
```

Deleted book (`404`):

```text
HTTP/1.1 404 Not Found
...
{"detail":"No Book matches the given query."}
```

`PUT` (`405`):

```text
HTTP/1.1 405 Method Not Allowed
Allow: GET, DELETE, HEAD, OPTIONS
...
{"detail":"Method \"PUT\" not allowed."}
```

Look inside the database:

```powershell
python manage.py shell -c "from books.models import Book; print(list(Book.objects.values()))"
```

### 🧪 Exercises

**2.1** Create three books and list them. What type is the JSON in the list response — object or array?

<details><summary>Answer</summary>An **array** (`[ {...}, {...}, {...} ]`). We did not configure pagination, so the list is returned as a plain array.</details>

**2.2** Send a `title` with 201 characters. Which status and message do you get?

```powershell
$body = @{ title = ("x" * 201); author = "A" } | ConvertTo-Json -Compress
Set-Content -Path scratch\long.json -Encoding ascii -Value $body
curl.exe -i -X POST http://127.0.0.1:8000/api/books/ -H "Content-Type: application/json" --data "@scratch/long.json"
```

<details><summary>Answer</summary>`400` with <code>{"title":["Ensure this field has no more than 200 characters."]}</code>. The limit comes from <code>max_length=200</code> on the model field; the serializer enforces it automatically.</details>

**2.3** Send the request *without* the `Content-Type: application/json` header. What happens and why?

<details><summary>Answer</summary>You get <code>415 Unsupported Media Type</code> (or a parse error). DRF picks a parser from the <code>Content-Type</code> request header. Without it, DRF does not know how to read the body. This is a nice example of a <em>request header</em> changing behaviour.</details>

**2.4** (Think) What is dangerous about the API in its current state?

<details><summary>Answer</summary>Anyone on the network can add or delete any book — there is no <strong>authentication</strong> (who are you?) and no <strong>authorization</strong> (are you allowed?). Lab 3 fixes both.</details>

### 🚑 Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `You have 1 unapplied migration(s)` in the server log | You skipped `migrate` | Run `python manage.py migrate` |
| `django.db.utils.OperationalError: no such table: books_book` | Migration never ran | `makemigrations books`, then `migrate` |
| `No changes detected` after `makemigrations` | App not listed in `INSTALLED_APPS`, or you forgot the app name | Check `"books"` is in `INSTALLED_APPS`; run `makemigrations books` |
| `400 {"detail":"JSON parse error - Expecting value: line 1 column 1 (char 0)"}` | The JSON file starts with an invisible **BOM** marker. In Windows PowerShell 5.1, `-Encoding utf8` adds one | Write JSON files with `-Encoding ascii` (our JSON is pure ASCII) |
| `400 JSON parse error - Expecting property name enclosed in double quotes` | Quotes were mangled by PowerShell | Use the `--data "@file.json"` approach from this workbook |
| `curl: (26)` or "couldn't read data from file" | Wrong path to the JSON file | Run from the project root; check with `Get-ChildItem scratch` |
| `Invoke-WebRequest : Cannot bind parameter...` | You typed `curl` not `curl.exe` | Use `curl.exe` |

### ✅ Checkpoint 2

- [ ] All seven requests in Step 6 return the status codes shown above (201, 400, 200, 200, 204, 404, 405).
- [ ] I can explain the difference between `makemigrations` and `migrate`.
- [ ] I can explain why `PUT` returns 405.
- [ ] I can name the security weakness of this lab's API.

**Lab journal:** Why does a successful `DELETE` return `204` and no body?

`______________________________________________`

---

# Lab 3 — Users, sessions, CSRF and permissions

This is the heart of the workbook. Take your time with the concepts; the code is short once they click.

### 🎯 Objectives

* Explain authentication vs authorization, cookies vs sessions, and CSRF vs CORS.
* Implement register, login, logout, "who am I?" and permissions with Django sessions.
* Follow a login from the first request to the cookie in the cookie jar, and see the session row in the database.

### 📖 Concepts

#### 3.A Authentication vs authorization

| | **Authentication** (AuthN) | **Authorization** (AuthZ) |
|---|---|---|
| Question | **Who are you?** | **What are you allowed to do?** |
| Evidence | Password, session cookie, token | Role, ownership, permissions |
| Happens | First | After authentication |
| Failure code | **401 Unauthorized** (poorly named: it means *unauthenticated*) | **403 Forbidden** |
| In our API | `login`, session cookie, `SessionAuthentication401` | `IsAuthenticatedOrReadOnly`, `IsOwnerOrStaffOrReadOnly` |

Example: a stranger tries to delete a book → **401** ("log in first"). Bob is logged in but the book is Alice's → **403** ("I know you, but no"). Nobody ever gets to Alice's book by guessing: the check is on the server.

#### 3.B Cookies: request vs response

A **cookie** is a small named value the *browser (or any client with a cookie jar)* stores and sends back automatically.

| | **Response cookie** | **Request cookie** |
|---|---|---|
| Direction | server → client | client → server |
| Header | `Set-Cookie: sessionid=abc123; HttpOnly; Path=/` | `Cookie: sessionid=abc123; csrftoken=xyz` |
| Contains | name, value **and attributes** (`HttpOnly`, `Secure`, `SameSite`, `Path`, `Max-Age`) | only `name=value` pairs |
| Purpose | "Please remember this." | "Here is what you asked me to remember." |

Cookie attributes that matter here:

| Attribute | Meaning |
|---|---|
| `HttpOnly` | JavaScript on the page cannot read the cookie (limits theft via XSS). |
| `Secure` | The client only sends it over HTTPS (we turn this on in Lab 4). |
| `SameSite=Lax` | The browser does not attach it to most cross-site POSTs (a CSRF defence layer). |
| `Max-Age` / `Expires` | How long it lives. Django's session default is 2 weeks. |
| `Path=/` | Sent for every URL on the site. |

#### 3.C Session cookie vs server-side session

```text
   CLIENT                                   SERVER
 ┌───────────────────────┐             ┌────────────────────────────────────┐
 │ cookie jar            │             │ table django_session               │
 │  sessionid = 79a6k…   │  ─────────▶ │  key       data (user id, …)  expiry│
 │  csrftoken = ypEI3…   │   sent with │  79a6k…    {"_auth_user_id":"1"}  …│
 └───────────────────────┘   each      └────────────────────────────────────┘
   only a random ID                        the real information lives here
```

| | **Session cookie** | **Server-side session** |
|---|---|---|
| Lives | In the client | In the server's database (`django_session`) |
| Contains | A long random **ID** — no user data, no password | The data: which user is logged in |
| Can the user edit it? | They can, but a changed ID simply matches nothing | No |
| Logout means | Cookie removed from the client | **Row deleted on the server** — this is the one that really matters |

Because the server deletes the row on logout, a *copied* old cookie is worthless. (You will prove it in an exercise and in a Playwright test.) The word *session cookie* is also used for "a cookie without an expiry that dies when the browser closes" — Django's cookie has a `Max-Age`, so strictly speaking it is a *persistent* cookie that holds a *session ID*. Don't let the vocabulary trip you.

#### 3.D The login flow — step by step

| # | What happens | Where in our code |
|---|---|---|
| 1 | The client sends `POST /api/login/` with JSON `{"username","password"}` plus a CSRF token | the request |
| 2 | Django **validates** the username and password: it hashes the given password and compares it to the stored hash | `authenticate(...)` in `LoginView` |
| 3 | Django **creates a server-side session** (a row in `django_session`) and rotates the CSRF token | `login(request, user)` |
| 4 | The response carries **`Set-Cookie: sessionid=…`** (and a fresh `csrftoken`) | automatic |
| 5 | The client **stores** the cookies and **sends** `Cookie: sessionid=…` on every later request | the client's cookie jar |
| 6 | Django looks the ID up in `django_session` and attaches `request.user` | `SessionMiddleware` + `AuthenticationMiddleware` |
| 7 | Before a write, DRF checks **permissions** (and CSRF) | `permission_classes`, `SessionAuthentication401` |
| 8 | `POST /api/logout/` deletes the session row and the cookie is cleared | `logout(request)` |

**Passwords are never stored.** `User.objects.create_user(...)` stores a salted, slow hash such as `pbkdf2_sha256$1000000$salt$hash`. At login Django hashes what you typed and compares hashes.

#### 3.E CSRF vs CORS

Imagine you are logged in to the library in one browser tab. In another tab you open `evil.example`. Its page quietly sends `POST https://library/api/books/delete…`. **Your browser attaches your session cookie automatically** — the server sees a perfectly valid logged-in request. That is **Cross-Site Request Forgery (CSRF)**.

**Django's defence:** every unsafe request (`POST`, `DELETE`, …) must also carry a *secret token* in a header, `X-CSRFToken`, that matches the `csrftoken` cookie. Evil.example can make the browser *send* the cookie, but it cannot *read* it, so it cannot copy the value into the header. Over HTTPS Django also checks the `Origin` (or `Referer`) header to make sure the request came from *our* site.

| | **CSRF protection** | **CORS** |
|---|---|---|
| What is it? | A defence against *forged writes* | A browser rule about *reading* responses across origins |
| Who enforces it? | **The server** (Django) | **The browser** |
| Protects against | A malicious site *causing* actions with your cookies | A malicious site *reading* your data |
| Configured with | `CsrfViewMiddleware`, `X-CSRFToken` | `Access-Control-Allow-Origin` headers (e.g. `django-cors-headers`) |
| Needed in this lab? | ✅ Yes | ❌ No — our clients are same-origin or not browsers |
| Does `curl`/Playwright care? | Yes, the *server* still checks | No, only browsers apply CORS |

> **CORS is not a CSRF defence**, and CSRF protection is not a CORS setting. Mixing them up is one of the most common beginner mistakes.

**Who needs a token in our API?** Every `POST`/`DELETE`: register, login, logout, add book, delete book. Reads (`GET`) never do.

#### 3.F Status codes — the full cast

| Code | Meaning | Example in our API |
|---|---|---|
| **200 OK** | Success with a body | login, `GET /api/books/` |
| **201 Created** | New resource created | register, add book |
| **204 No Content** | Success, empty body | logout, delete |
| **400 Bad Request** | Input is invalid | missing `title`, weak password |
| **401 Unauthorized** | Not authenticated | anonymous `POST /api/books/`, wrong password |
| **403 Forbidden** | Authenticated (or CSRF failed) but not allowed | deleting someone else's book, missing CSRF token |
| **404 Not Found** | No such resource | `GET /api/books/9999/` |
| 405 | Method not allowed | `PUT` |
| 415 | Unsupported media type | body not JSON |

#### 3.G A DRF quirk (and why `authentication.py` exists)

Out of the box, DRF's session login answers **403** for a stranger, not 401, because the session scheme has no "challenge" to put in a `WWW-Authenticate` header. We subclass it and add one. Now **401 means "I don't know who you are"** and **403 means "I know who you are, and no."** That distinction is exactly what the course is about.

### 📁 Files you will create or change

| File | Why it exists |
|---|---|
| `config/settings.py` (add a block) | Turns on session auth, "secure by default" permissions, JSON CSRF errors. |
| `books/authentication.py` (new) | Makes unauthenticated requests return 401. |
| `books/permissions.py` (new) | Rule "only the owner or staff may delete". |
| `books/models.py` (change) | Adds `owner` to `Book`. |
| `books/migrations/0002_…` (generated) | Adds the `owner` column to the existing table. |
| `books/serializers.py` (change) | Adds owner display, input validation, user serializers. |
| `books/views.py` (change) | Adds register/login/logout/me/csrf views and permissions on books. |
| `books/urls.py` (change) | Adds the new URLs. |

### 🛠️ Build it

Stop the server (Ctrl+C) while you edit.

**Step 1 — Append this block to the END of `config/settings.py`**

```python
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
```

**Step 2 — Create `books/authentication.py`**

**`books/authentication.py`**

```python
from rest_framework.authentication import SessionAuthentication


class SessionAuthentication401(SessionAuthentication):
    """
    Django REST Framework's stock SessionAuthentication has a quirk:
    when you are NOT logged in, it answers 403 instead of 401.

    By supplying an authenticate_header(), we tell DRF that this scheme can
    "challenge" the client, so DRF answers 401 Unauthorized (plus a
    WWW-Authenticate header).  Result:
        401 = "I don't know who you are"      (authentication problem)
        403 = "I know who you are, but no"    (authorization problem)
    """

    def authenticate_header(self, request):
        return "Session"
```

**Step 3 — Create `books/permissions.py`**

**`books/permissions.py`**

```python
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """
    Object-level rule for a single book:
      * Anyone may read (GET, HEAD, OPTIONS).
      * Only the book's owner, or a staff user, may change or delete it.
    Books with no owner (created before ownership existed) can only be
    removed by staff.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_staff or obj.owner_id == request.user.id)
```

**Step 4 — Replace `books/models.py`** (adds `owner`)

**`books/models.py`**

```python
from django.conf import settings
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    published_year = models.PositiveSmallIntegerField(null=True, blank=True)
    # Phase 3: every new book remembers who added it.
    # null=True because books created in Phase 2 have no owner.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="books",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.title} by {self.author}"
```

`on_delete=models.SET_NULL` means: if a user is deleted, keep their books but clear the owner. `null=True` lets the books you created in Lab 2 (which have no owner) survive the migration.

**Step 5 — Replace `books/serializers.py`**

**`books/serializers.py`**

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Book

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    # Show the owner's username; clients can never set it themselves.
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "published_year", "owner", "created_at"]
        read_only_fields = ["id", "owner", "created_at"]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be blank.")
        return value

    def validate_author(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Author cannot be blank.")
        return value

    def validate_published_year(self, value):
        if value is not None and not (1000 <= value <= 2100):
            raise serializers.ValidationError("Year must be between 1000 and 2100.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=[UnicodeUsernameValidator()])
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate(self, attrs):
        # Reuse Django's password rules (length, common passwords, ...).
        try:
            validate_password(attrs["password"], user=User(username=attrs["username"]))
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"password": list(exc.messages)})
        return attrs

    def create(self, validated_data):
        # create_user() hashes the password. We never store the plain text.
        return User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)
```

**Step 6 — Replace `books/views.py`**

**`books/views.py`**

```python
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import (
    BookSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)


def csrf_failure(request, reason=""):
    """Called by Django when a CSRF check fails on a non-DRF view (register/login)."""
    return JsonResponse({"detail": f"CSRF Failed: {reason}"}, status=403)


# --- Utility endpoints -----------------------------------------------------

@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok"})


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    """
    Hands out a CSRF token.  Calling get_token() also makes Django set the
    'csrftoken' cookie on the response.
    """
    return Response({"csrfToken": get_token(request)})


@api_view(["GET"])
def me(request):
    """Who am I?  Needs a valid session, otherwise 401."""
    return Response(UserSerializer(request.user).data)


# --- Authentication endpoints ----------------------------------------------
# Register and login are used by people who are NOT logged in yet, so DRF's
# session authentication would not check CSRF for them. We switch the check
# on explicitly with csrf_protect, so ALL unsafe requests need a token.

@method_decorator(csrf_protect, name="dispatch")
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # -> 400 with field errors
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            # Same message for "no such user" and "wrong password" on purpose.
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)  # creates the server-side session + Set-Cookie
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    # Default permission (IsAuthenticated) and default session authentication
    # (which enforces CSRF) apply here.
    def post(self, request):
        logout(request)  # deletes the server-side session
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Book endpoints --------------------------------------------------------

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.select_related("owner")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetailView(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.select_related("owner")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrStaffOrReadOnly]
```

**Step 7 — Replace `books/urls.py`**

**`books/urls.py`**

```python
from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("csrf/", views.csrf, name="csrf"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("me/", views.me, name="me"),
    path("books/", views.BookListCreateView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
]
```

**Step 8 — Migrate and run**

```powershell
python manage.py check
python manage.py makemigrations books -n add_book_owner
python manage.py migrate
python manage.py runserver
```

**Step 9 — Create a test user** (two ways; try both)

*Via the API* — this is what a real client does (shown in Step 10).
*Via the Django shell* — handy for scripts and for creating staff users:

```powershell
python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_user('shelluser', password='S3cure-Lab-Passw0rd!')"
```

**Step 10 — Walk the whole flow** (Terminal B). First set up two helpers and the JSON files:

```powershell
$BASE = "http://127.0.0.1:8000"
$JAR  = "scratch\jar.txt"
Remove-Item $JAR -ErrorAction SilentlyContinue

# Asks the server for a CSRF token (and stores the csrftoken cookie in the jar)
function Get-Csrf { (curl.exe -s -c $JAR -b $JAR "$BASE/api/csrf/" | ConvertFrom-Json).csrfToken }

Set-Content -Path scratch\alice.json -Encoding ascii -Value '{"username":"alice","password":"S3cure-Lab-Passw0rd!"}'
Set-Content -Path scratch\book.json  -Encoding ascii -Value '{"title":"Dune","author":"Frank Herbert","published_year":1965}'
```

> `-c $JAR` tells curl to **save** cookies into that file; `-b $JAR` tells it to **send** cookies from it. Together they behave like a tiny browser cookie jar.

```powershell
# A) Not logged in: try to add a book  -> expect 401
curl.exe -i -X POST "$BASE/api/books/" -H "Content-Type: application/json" --data "@scratch/book.json"

# B) Register alice -> expect 201     (every POST needs a fresh token)
$T = Get-Csrf
curl.exe -i -c $JAR -b $JAR -H "Content-Type: application/json" -H "X-CSRFToken: $T" --data "@scratch/alice.json" "$BASE/api/register/"

# C) Log in -> expect 200 and two Set-Cookie headers
$T = Get-Csrf
curl.exe -i -c $JAR -b $JAR -H "Content-Type: application/json" -H "X-CSRFToken: $T" --data "@scratch/alice.json" "$BASE/api/login/"

# D) Who am I? (the cookie jar is sent automatically) -> expect 200
curl.exe -b $JAR "$BASE/api/me/"

# E) Add a book -> expect 201 (note the "owner")
$T = Get-Csrf
curl.exe -i -c $JAR -b $JAR -H "Content-Type: application/json" -H "X-CSRFToken: $T" --data "@scratch/book.json" "$BASE/api/books/"

# F) Add a book WITHOUT the token -> expect 403 (CSRF)
curl.exe -i -c $JAR -b $JAR -H "Content-Type: application/json" --data "@scratch/book.json" "$BASE/api/books/"

# G) Anyone can read -> expect 200 (no cookies sent at all)
curl.exe "$BASE/api/books/"

# H) Delete your book -> expect 204.  Replace 3 with the "id" from step E.
$T = Get-Csrf
curl.exe -i -X DELETE -c $JAR -b $JAR -H "X-CSRFToken: $T" "$BASE/api/books/3/"

# I) Log out -> expect 204
$T = Get-Csrf
curl.exe -i -X POST -c $JAR -b $JAR -H "X-CSRFToken: $T" "$BASE/api/logout/"

# J) Who am I now? -> expect 401
curl.exe -i -b $JAR "$BASE/api/me/"
```

**Step 11 — Look at the evidence**

```powershell
Get-Content $JAR                       # the cookie jar (run it after step C and again after step I)
python manage.py shell -c "from django.contrib.sessions.models import Session; print('sessions in database:', Session.objects.count())"
```

### 👀 Expected output

**A** — not logged in:

```text
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Session
Content-Type: application/json
...
{"detail":"Authentication credentials were not provided."}
```

**C** — login (the heart of everything). Find the `Set-Cookie` lines:

```text
HTTP/1.1 200 OK
Content-Type: application/json
Vary: Cookie
Set-Cookie: csrftoken=ypEI3svNWvStAQSBbZ8iQoYxLoPnzvqH; expires=Thu, 21 Oct 2027 21:09:31 GMT; Max-Age=31449600; Path=/; SameSite=Lax
Set-Cookie: sessionid=79a6kpjmokk0djbp2lp72t09nqxeiqop; expires=Thu, 05 Nov 2026 21:09:31 GMT; HttpOnly; Max-Age=1209600; Path=/; SameSite=Lax

{"id":2,"username":"alice"}
```

The ids and token values will differ for you. Note: **no `Secure` flag yet** — that arrives with HTTPS in Lab 4.

**E** — created, with an owner:

```text
HTTP/1.1 201 Created
...
{"id":3,"title":"Dune","author":"Frank Herbert","published_year":1965,"owner":"alice","created_at":"2026-10-22T21:14:33.285370Z"}
```

**F** — missing CSRF token:

```text
HTTP/1.1 403 Forbidden
...
{"detail":"CSRF Failed: CSRF token missing."}
```

**J** — after logout:

```text
HTTP/1.1 401 Unauthorized
...
{"detail":"Authentication credentials were not provided."}
```

The cookie jar after login (tab-separated; the `#HttpOnly_` prefix is curl's way of marking an HttpOnly cookie):

```text
#HttpOnly_127.0.0.1	FALSE	/	FALSE	1793912971	sessionid	79a6kpjmokk0djbp2lp72t09nqxeiqop
127.0.0.1	FALSE	/	FALSE	1824152971	csrftoken	ypEI3svNWvStAQSBbZ8iQoYxLoPnzvqH
```

The session count is `1` while you are logged in and `0` after logout.

### 🧪 Exercises

**3.1** While logged in as alice, try to delete one of the books you created in Lab 2. What do you get, and why?

<details><summary>Answer</summary>`403 Forbidden`. Books from Lab 2 have <code>owner = NULL</code>. The permission rule is "owner or staff", and a real user never equals NULL, so only staff may delete them.</details>

**3.2** Make alice a staff user and try again — *without logging in again*.

```powershell
python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.filter(username='alice').update(is_staff=True)"
```

<details><summary>Answer</summary>The delete now succeeds (<code>204</code>) even though her session is old. The session stores only the <strong>user id</strong>; Django re-reads the user from the database on every request, so the new permission applies immediately. Undo with <code>update(is_staff=False)</code>.</details>

**3.3 — Replay attack.** Log in, *copy the jar file*, log out, then use the copy:

```powershell
Copy-Item $JAR scratch\jar-old.txt
# ... log out (step I) ...
curl.exe -i -b scratch\jar-old.txt "$BASE/api/me/"
```

What status do you get and what does that prove?

<details><summary>Answer</summary><code>401</code>. The old cookie still <em>exists</em> on the client, but the session row it points to was <strong>deleted on the server</strong> at logout. Server-side sessions can be revoked; that is their main advantage over self-contained tokens.</details>

**3.4** Look at alice's stored password:

```powershell
python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.get(username='alice').password)"
```

What do the `$`-separated parts mean?

<details><summary>Answer</summary>Format <code>algorithm$iterations$salt$hash</code>, e.g. <code>pbkdf2_sha256$1000000$Kd4…$9fX…</code>. The <em>salt</em> is random per user (so identical passwords give different hashes); the <em>iterations</em> make each guess slow for an attacker. The plain password is nowhere in the database.</details>

**3.5** Do the login with a *wrong* password, then with a *non-existent* user. Compare the two responses. Why are they identical?

<details><summary>Answer</summary>Both return <code>401 {"detail":"Invalid username or password."}</code>. Identical messages stop an attacker from using the login form to discover which usernames exist (<em>user enumeration</em>). (Our <em>register</em> endpoint does reveal existing names — a real-world trade-off; see Lab 8.)</details>

### 🚑 Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `ImportError: Could not import 'books.authentication.SessionAuthentication401'` | Settings block added before `authentication.py` exists | Create the file (Step 2); check spelling |
| `OperationalError: no such column: books_book.owner` | Forgot `makemigrations` / `migrate` | Run both |
| `403 {"detail":"CSRF Failed: CSRF token missing."}` | No `X-CSRFToken` header | Call `Get-Csrf` first and pass `-H "X-CSRFToken: $T"` |
| `403 CSRF Failed: CSRF token incorrect` right after login | You used a token from *before* login. Django **rotates** the token at login | Call `$T = Get-Csrf` again after every login |
| `Get-Csrf` returns nothing | Server not running, or typo in `$BASE` | Check Terminal A; open `$BASE/api/health/` |
| `401` on `/api/me/` right after login | The `-c`/`-b` flags were missing on the login call, so the cookie was not saved | Repeat step C with `-c $JAR -b $JAR` |
| `415 Unsupported Media Type` | Missing `Content-Type: application/json` | Add the header |
| `403` with *"Authentication credentials were not provided"* | You forgot `authentication.py`'s 401 override *or* your cookie jar is empty | Compare with the 401/403 table in 3.F |

### ✅ Checkpoint 3

- [ ] Steps A–J give exactly the status codes in the comments (401, 201, 200, 200, 201, 403, 200, 204, 204, 401).
- [ ] I found the `Set-Cookie: sessionid=...; HttpOnly` header in the login response.
- [ ] I can show the session row count going `0 → 1 → 0`.
- [ ] I can explain (out loud!) the difference between: authentication/authorization, request/response cookies, session cookie/server-side session, CSRF/CORS, 401/403.
- [ ] I did exercise 3.3 and understand why the replayed cookie fails.

**Lab journal:** Why can `evil.example` make your browser *send* your session cookie but not *read* your CSRF token?

`______________________________________________`


---

# Lab 4 — Local HTTPS and certificates

### 🎯 Objectives

* Explain HTTP vs HTTPS, SSL vs TLS, and what a certificate and a certificate authority are.
* Explain how a client validates a certificate and how HTTPS encrypts data.
* Explain why HTTPS does **not** replace authentication.
* Generate a self-signed certificate, run the API over HTTPS, and trust that certificate **explicitly** (never by turning validation off).

> ⚠️ **Learning setup only.** Nothing in this lab is a production deployment guide. See section 4.H.

### 📖 Concepts

#### 4.A HTTP vs HTTPS

| | **HTTP** | **HTTPS** (HTTP over TLS) |
|---|---|---|
| Default port | 80 | 443 (we use **8443**, a high port, so no admin rights are needed) |
| On the wire | Readable text | Encrypted bytes |
| Someone on the same Wi-Fi sees | Cookies, passwords, JSON bodies | Only *who* you connect to and how much data moves |
| Can be modified in transit | ✅ Yes | ❌ Tampering is detected |
| Proves the server's identity | ❌ No | ✅ Yes, via its certificate |

HTTPS gives you three things: **confidentiality** (nobody can read it), **integrity** (nobody can change it unnoticed), **server authentication** (you are really talking to `localhost`, not an impostor).

#### 4.B SSL vs TLS

**SSL** (Secure Sockets Layer, versions 2 and 3) was the original protocol. It is broken and obsolete. **TLS** (Transport Layer Security, versions 1.0 → 1.3) replaced it; today only **TLS 1.2 and 1.3** are considered safe. People still say "SSL certificate" and `openssl` still has "SSL" in its name — that is a *habit*, not a technology. Everything you do in this lab uses modern TLS.

#### 4.C What is inside a certificate?

A certificate (format **X.509**) is a signed ID card for a public key:

| Field | Meaning | Our value |
|---|---|---|
| **Subject** | Who the certificate is for | `CN = localhost` |
| **Subject Alternative Name (SAN)** | The host names the certificate is valid for. **Clients check this, not the CN.** | `DNS:localhost` |
| **Issuer** | Who signed it | `CN = localhost` (we signed it ourselves) |
| **Public key** | Used to set up encryption and verify the server's signature | RSA 2048 bit |
| **Validity** | `Not Before` / `Not After` dates | 365 days |
| **Basic Constraints** | May this certificate sign other certificates? | `CA:FALSE` (no) |
| **Signature** | The issuer's cryptographic signature over all of the above | `sha256WithRSAEncryption` |

The matching **private key** is a *separate file* that never leaves the server. Whoever has it can impersonate the server — so it stays out of Git.

#### 4.D What does a certificate authority (CA) do?

A **CA** is an organisation your computer already trusts. It checks that you control a domain and then **signs** your certificate. Your operating system and browser ship with a list of trusted **root CAs** (the *trust store*).

```text
  Root CA  (in your trust store)
     │ signs
     ▼
  Intermediate CA
     │ signs
     ▼
  Server certificate for  www.example.com        ← the chain the client verifies
```

Our certificate is **self-signed**: issuer = subject. There is no chain. Nobody vouches for it except ourselves, so **clients will not trust it unless we tell them to** — that is what the rest of this lab is about.

#### 4.E How does a client validate a certificate?

Before sending a single HTTP byte, the client checks that:

1. The certificate is **signed** by a CA it trusts (or *is itself* a certificate it has been told to trust).
2. The chain of signatures is **unbroken**.
3. Today's date is **within** `Not Before … Not After`.
4. The host name in the URL **matches the SAN** (`localhost` ✅, `127.0.0.1` ❌ for our certificate).
5. The certificate is not **revoked** (production CAs; not applicable to our local one).
6. The server proves it holds the **private key** by signing part of the handshake.

If any check fails, the client **refuses the connection**. That refusal is a feature — it is what stops man-in-the-middle attacks. *Disabling validation (for example `curl -k` or Playwright's `ignoreHTTPSErrors: true`) throws that protection away, so we never do it.*

#### 4.F How does HTTPS encrypt the data? (the TLS handshake, simplified)

1. **ClientHello** — "I speak TLS 1.3 / 1.2; here are my cipher suites and a random number."
2. **ServerHello + certificate** — "Let's use this suite. Here is my certificate."
3. The client **validates the certificate** (4.E).
4. **Key exchange** — both sides use an algorithm (ECDHE) to agree on a **shared secret** that never travels over the network.
5. Both derive **session keys** from it. Handshake finished.
6. All HTTP traffic is now encrypted with a fast **symmetric** cipher (AES-GCM or ChaCha20-Poly1305).

*Why two kinds of cryptography?* Public-key cryptography is great for proving identity and agreeing on a secret, but slow. Symmetric encryption is fast but needs a shared secret. TLS uses the first to bootstrap the second.

#### 4.G HTTPS does **not** replace authentication

| Question | Answered by |
|---|---|
| "Is nobody listening in?" | HTTPS ✅ |
| "Is this really the server I wanted?" | HTTPS ✅ |
| "**Who is this user?**" | Login + session ❌ not HTTPS |
| "**Is this user allowed to delete that book?**" | Permissions ❌ not HTTPS |
| "Is this request forged by another site?" | CSRF protection ❌ not HTTPS |
| "Is the password strong?" | Password validators ❌ not HTTPS |

Anybody on the internet can open an HTTPS connection to your server. HTTPS only makes sure the conversation is private; *who* is in the conversation and what they may do is still your code's job.

#### 4.H Development vs production certificates

| | **Our dev certificate** | **Production certificate** |
|---|---|---|
| Signed by | Itself | A public CA (e.g. Let's Encrypt) |
| Trusted by | Only the clients we configure | Every browser and OS by default |
| Name | `localhost` only | Your real domain |
| Lifetime | 1 year, manual | ~90 days, auto-renewed |
| Private key | A file on your laptop | Protected (secrets manager, HSM, or proxy) |
| Revocation | None | CRL/OCSP |
| Who terminates TLS | The Python server (uvicorn) | Usually a reverse proxy / load balancer in front of Django |

#### 4.I Django's `runserver` does **not** speak HTTPS

`python manage.py runserver` serves plain HTTP only. To get HTTPS we run Django under a real server process that can terminate TLS. We use **uvicorn**, which serves Django through its `config/asgi.py` file and accepts `--ssl-keyfile` and `--ssl-certfile`. (Other fine options: `django-extensions`' `runserver_plus`, Hypercorn, or a local reverse proxy such as Caddy/nginx.)

### 📁 Files

| File | Why it exists |
|---|---|
| `.gitignore` | Keeps keys, databases, `node_modules` and your virtual environment out of Git. |
| `certs/README.md` | The only file in `certs/` that **is** committed: explains what belongs there. |
| `certs/localhost-key.pem` | **Private key** (generated; never commit). |
| `certs/localhost-cert.pem` | The self-signed **certificate** (generated). |
| `config/settings.py` (add a block) | `Secure` cookies and trusted origins. |
| `config/asgi.py` | Generated by Django; uvicorn loads `config.asgi:application`. |

### 🛠️ Build it

Stop `runserver` (Ctrl+C).

**Step 1 — Protect your secrets first.** Create `.gitignore` in the project root:

**`.gitignore`**

```text
# --- Python ---
__pycache__/
*.py[cod]
.venv/
venv/

# --- Django ---
db.sqlite3
*.sqlite3
*.sqlite3-journal

# --- Certificates and private keys: NEVER commit these ---
certs/*
!certs/README.md

# --- Node / Playwright ---
node_modules/
api-tests/test-results/
api-tests/playwright-report/

# --- Local configuration and scratch files ---
.env
.env.*
scratch/
```

Create `certs\README.md`:

**`certs/README.md`**

```markdown
# certs/

This folder holds the **local development certificate** for the lab.
The files are generated on your own machine and are ignored by Git.

    localhost-key.pem    PRIVATE key  (never share, never commit)
    localhost-cert.pem   self-signed certificate for the name "localhost"

See Lab 4 of the workbook for the exact commands.
For development only. Do NOT use this setup in production.
```

*(Optional but recommended)* prove the rules work:

```powershell
git init
git add -A
git status --short       # you should NOT see .venv, db.sqlite3, scratch, or any .pem file
```

**Step 2 — Find OpenSSL**

```powershell
openssl version
```

If PowerShell says it is not recognized, and you have Git for Windows, add its copy for this session:

```powershell
$env:Path += ";C:\Program Files\Git\usr\bin"
openssl version
```

**Step 3 — Generate the key and certificate** (one line)

```powershell
openssl req -x509 -newkey rsa:2048 -nodes -keyout certs/localhost-key.pem -out certs/localhost-cert.pem -days 365 -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost" -addext "basicConstraints=critical,CA:FALSE"
```

| Part | Meaning |
|---|---|
| `req -x509` | Create a **self-signed** certificate directly |
| `-newkey rsa:2048` | Also create a new 2048-bit RSA key pair |
| `-nodes` | No passphrase on the key (convenient for a dev server) |
| `-keyout …` / `-out …` | Where to write the private key / the certificate |
| `-days 365` | Valid for one year |
| `-subj "/CN=localhost"` | Subject: common name `localhost` |
| `-addext "subjectAltName=DNS:localhost"` | The host name clients will match |
| `-addext "basicConstraints=critical,CA:FALSE"` | "This certificate may **not** act as a CA" — limits the damage if the key leaks |

**Step 4 — Read your certificate**

```powershell
openssl x509 -in certs/localhost-cert.pem -noout -text | Select-String "Issuer:|Subject:|Not Before|Not After|Public-Key|Signature Algorithm|DNS:|CA:"
```

**Step 5 — Append this block to the END of `config/settings.py`**

```python
# ---------------------------------------------------------------------------
# PHASE 4 ADDITIONS: HTTPS
# ---------------------------------------------------------------------------
# "Secure" cookies are only sent by clients over HTTPS connections.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Over HTTPS, Django also checks the Origin (or Referer) header of unsafe
# requests. This lists the web origins we accept besides the request's own host.
CSRF_TRUSTED_ORIGINS = ["https://localhost:8443"]
```

`Secure` cookies are only sent by clients over HTTPS. `CSRF_TRUSTED_ORIGINS` lists additional web origins Django accepts in the `Origin` header.

**Step 6 — Start the HTTPS server** (Terminal A, project root, venv active — one line)

```powershell
python -m uvicorn config.asgi:application --host 127.0.0.1 --port 8443 --ssl-keyfile certs/localhost-key.pem --ssl-certfile certs/localhost-cert.pem --lifespan off
```

(`--lifespan off` just hides a harmless "lifespan unsupported" notice.) Leave it running.

**Step 7 — Test it in Terminal B**

```powershell
# 1) WITHOUT trust: curl must REFUSE
curl.exe -i https://localhost:8443/api/health/

# 2) WITH explicit trust of OUR certificate: works
curl.exe -i --ssl-no-revoke --cacert certs/localhost-cert.pem https://localhost:8443/api/health/

# 3) Wrong host name (not in the certificate's SAN): must REFUSE again
curl.exe -i --ssl-no-revoke --cacert certs/localhost-cert.pem https://127.0.0.1:8443/api/health/

# 4) Peek at the TLS handshake
curl.exe -v --ssl-no-revoke --cacert certs/localhost-cert.pem https://localhost:8443/api/health/ 2>&1 | Select-String "TLS|SSL|subject|issuer|expire|HTTP/"
```

> `--cacert` means "trust *this specific certificate file* as a root". `--ssl-no-revoke` only skips the *revocation lookup* that Windows' curl performs — a self-signed local certificate has no revocation server. **It does not turn certificate validation off.**

**Step 8 — Log in over HTTPS and discover a new rule**

```powershell
$BASE = "https://localhost:8443"
$TLS  = @("--ssl-no-revoke", "--cacert", "certs/localhost-cert.pem")
$JAR  = "scratch\jar-https.txt"
Remove-Item $JAR -ErrorAction SilentlyContinue
function Get-Csrf { (curl.exe @TLS -s -c $JAR -b $JAR "$BASE/api/csrf/" | ConvertFrom-Json).csrfToken }
```

`@TLS` "splats" the three arguments into every call, so we don't retype them. Make sure `scratch\alice.json` and `scratch\book.json` exist from Lab 3, and that `alice` exists (Lab 3, step B or run it again).

```powershell
$T = Get-Csrf

# a) Token only, no Origin header -> expect 403
curl.exe @TLS -i -c $JAR -b $JAR -H "Content-Type: application/json" -H "X-CSRFToken: $T" --data "@scratch/alice.json" "$BASE/api/login/"

# b) Token AND Origin header -> expect 200
curl.exe @TLS -i -c $JAR -b $JAR -H "Content-Type: application/json" -H "X-CSRFToken: $T" -H "Origin: $BASE" --data "@scratch/alice.json" "$BASE/api/login/"

# c) Authenticated read, then an authenticated write (fresh token + Origin each time)
curl.exe @TLS -b $JAR "$BASE/api/me/"
$T = Get-Csrf
curl.exe @TLS -i -c $JAR -b $JAR -H "Content-Type: application/json" -H "X-CSRFToken: $T" -H "Origin: $BASE" --data "@scratch/book.json" "$BASE/api/books/"
```

**Step 9 — Trust the certificate in your browser (optional)**

You can simply click *Advanced → Continue to localhost* in the browser warning. To make the warning disappear (Edge/Chrome on Windows):

```powershell
certutil -addstore -user Root certs\localhost-cert.pem
```

Windows shows a security dialog; click **Yes**. Visit <https://localhost:8443/api/health/> — no warning. **When you finish the course, remove it:**

```powershell
certutil -delstore -user Root localhost
```

(Firefox keeps its own trust store: use its *Advanced → Accept the Risk* button, or set `security.enterprise_roots.enabled` to `true` in `about:config`.)

### 👀 Expected output

`openssl x509 … | Select-String`:

```text
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = localhost
            Not Before: Oct 22 21:13:40 2026 GMT
            Not After : Oct 22 21:13:40 2027 GMT
        Subject: CN = localhost
                Public-Key: (2048 bit)
                DNS:localhost
                CA:FALSE
```

Server start-up:

```text
INFO:     Started server process [12345]
INFO:     Application startup complete.
INFO:     Uvicorn running on https://127.0.0.1:8443 (Press CTRL+C to quit)
```

Step 7, test 1 — **a failure is the correct result** (wording depends on your curl build):

```text
curl: (35) schannel: SEC_E_UNTRUSTED_ROOT (0x80090325) - The certificate chain was issued by an authority that is not trusted.
   — or —
curl: (60) SSL certificate problem: self-signed certificate
```

Test 2 → `HTTP/1.1 200 OK` and `{"status":"ok"}`.
Test 3 → a failure such as `no alternative certificate subject name matches target host name '127.0.0.1'`.

Step 8a:

```text
HTTP/1.1 403 Forbidden
...
{"detail":"CSRF Failed: Referer checking failed - no Referer."}
```

Step 8b — note the new **`Secure`** attribute on both cookies:

```text
HTTP/1.1 200 OK
...
Set-Cookie: csrftoken=…; expires=…; Max-Age=31449600; Path=/; SameSite=Lax; Secure
Set-Cookie: sessionid=…; expires=…; HttpOnly; Max-Age=1209600; Path=/; SameSite=Lax; Secure

{"id":2,"username":"alice"}
```

### 🔍 Why did 8a fail?

Over **HTTPS**, Django's CSRF middleware also requires an **`Origin`** (or `Referer`) header on unsafe requests and checks that it matches the site. A browser adds `Origin` automatically; `curl.exe` and Playwright's API client do **not**, so we add it by hand: `-H "Origin: https://localhost:8443"`. Over plain HTTP in Lab 3 this extra check did not apply, which is why it surprised you now.

### ⚠️ Limitations of this approach

* The certificate is **its own root of trust**. Only the clients you configure (curl's `--cacert`, Node's `NODE_EXTRA_CA_CERTS`, the Windows store) believe it. Nobody else will.
* It is valid **only for the name `localhost`** and **only for 365 days**. After that, clients reject it (`certificate has expired`).
* Installing it in the OS store makes *every* program on your account trust it. Because the private key is just a file on your disk, **remove it when you are done** and never commit the key.
* There is **no revocation**: if the key leaked you would just delete it and generate another.
* **Not a production recipe.** Production uses a public CA, a real domain, automatic renewal, protected keys, and usually a reverse proxy that terminates TLS (then Django must be told with `SECURE_PROXY_SSL_HEADER`).
* *Tool alternative:* `mkcert` creates a local CA and installs it for you. Easier, but that CA key can mint certificates for *any* site on your machine, so it needs even more care.

### 🧪 Exercises

**4.1 — The SAN matters.** Regenerate the certificate with `-addext "subjectAltName=DNS:localhost,IP:127.0.0.1"`, restart the server and repeat Step 7, test 3. What changes? Then **restore the original certificate** (SAN `DNS:localhost` only). Why? (Hint: think ahead to Lab 6.)

<details><summary>Answer</summary>With the IP in the SAN, <code>https://127.0.0.1:8443</code> is accepted. We restore the original because one of our Playwright tests in Lab 6 deliberately connects through <code>127.0.0.1</code> and expects the connection to be <em>rejected</em> — it proves certificate-name validation is really active.</details>

**4.2** Open `http://localhost:8443/api/health/` (note: `http`, not `https`) in a browser. What happens and why?

<details><summary>Answer</summary>The page fails to load (or shows "empty response/SSL error"). The port expects a TLS handshake; plain HTTP bytes are not a valid handshake, so the server closes the connection. HTTP and HTTPS are different protocols and need different ports/URLs.</details>

**4.3** How many days until your certificate expires? What will clients do after that?

```powershell
openssl x509 -in certs/localhost-cert.pem -noout -enddate
```

<details><summary>Answer</summary>The command prints <code>notAfter=…</code>. After that date every client rejects the certificate (<code>certificate has expired</code>); you must generate a new one. Production setups automate renewal for exactly this reason.</details>

**4.4** In Step 8b's response, find the `Secure` attribute. In your own words, what will a browser do with a `Secure` cookie on an `http://` page of a *real* host name?

<details><summary>Answer</summary>It will not send (and usually won't even accept) it, so a login over plain HTTP would not stick. <em>Careful:</em> browsers and curl treat <code>localhost</code>/<code>127.0.0.1</code> as a special "secure enough" case, so on your own computer you might not see a failure. On a real server it matters a lot.</details>

**4.5** Run `openssl x509 -in certs/localhost-cert.pem -noout -fingerprint -sha256` and `Get-FileHash certs\localhost-key.pem`. Which of the two files is safe to show to a classmate, and which must stay secret?

<details><summary>Answer</summary>The <strong>certificate</strong> is public by design (it is sent to every visitor). The <strong>private key</strong> must stay secret.</details>

### 🚑 Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `openssl : The term 'openssl' is not recognized` | OpenSSL not installed / not on PATH | Add Git's copy (`$env:Path += ";C:\Program Files\Git\usr\bin"`) or `winget install ShiningLight.OpenSSL.Light` |
| `req: Unknown option -addext` | Very old OpenSSL/LibreSSL | Use OpenSSL 1.1.1+ (Git for Windows ships 3.x) |
| Subject comes out like `C:/Program Files/Git/CN=localhost` | You ran the command in **Git Bash**, which rewrites `/CN=…` into a path | Use PowerShell, or in Git Bash write `//CN=localhost` or `MSYS_NO_PATHCONV=1 openssl …` |
| `FileNotFoundError: … localhost-key.pem` when starting uvicorn | Wrong working directory or filename | Run from the project root; `Get-ChildItem certs` |
| `[Errno 10048] … only one usage of each socket address` | Port 8443 already in use | Stop the other server, or choose another port (update `CSRF_TRUSTED_ORIGINS` and `BASE_URL`) |
| `curl: (35) … CRYPT_E_NO_REVOCATION_CHECK` / `revocation function was unable to check` | Windows curl tries to check revocation | Add `--ssl-no-revoke` (keeps validation otherwise) |
| `curl: (35) … SEC_E_UNTRUSTED_ROOT` even **with** `--cacert` | Some Windows curl/schannel builds ignore `--cacert` | Trust the file once with `certutil -addstore -user Root …` (Step 9), then call curl without `--cacert` |
| Browser: `NET::ERR_CERT_AUTHORITY_INVALID` | Browser does not trust a self-signed cert | Step 9 or click through the warning |
| Browser: `ERR_CERT_COMMON_NAME_INVALID` | You used `127.0.0.1` instead of `localhost` | Use `https://localhost:8443` |
| `403 … Referer checking failed - no Referer` | HTTPS request without `Origin` | Add `-H "Origin: https://localhost:8443"` |
| `403 … Origin checking failed - https://… does not match any trusted origins` | Port/host differ from `CSRF_TRUSTED_ORIGINS` | Fix the setting or the URL |
| `ERR_SSL_PROTOCOL_ERROR` | You used `https://` against the plain `runserver` (port 8000) | Use `http://` for `runserver`, `https://` for uvicorn |

### ✅ Checkpoint 4

- [ ] `git status --short` shows **no** `.pem`, `db.sqlite3`, `.venv` or `scratch` files.
- [ ] uvicorn runs on `https://127.0.0.1:8443`.
- [ ] `curl.exe` **without** `--cacert` fails; **with** `--cacert` returns `200`.
- [ ] Connecting through `127.0.0.1` fails (name mismatch) — and I can explain why.
- [ ] My login response contains `Secure` on both cookies, and I know why 8a failed and 8b worked.
- [ ] I can explain: certificate contents, what a CA does, the six validation checks, why HTTPS ≠ authentication, dev vs production certificates.

**Lab journal:** Someone says "we use HTTPS, so we don't need to log users in." What is wrong with that sentence?

`______________________________________________`

