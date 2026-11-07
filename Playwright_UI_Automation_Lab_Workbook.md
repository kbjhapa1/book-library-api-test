# Playwright UI Automation with TypeScript — Hands-On Lab Workbook

### Built on the Book Library project · Student edition · 7 phases

> **Your goal:** learn to think and work like a QA Automation Engineer — understand an application, decide what is worth automating, build reliable UI and API tests with Playwright and TypeScript, organize them as a maintainable framework, and run them in CI/CD.

> **Edition status:** this file contains the **course overview, the inspection of the existing project, the seven-phase roadmap, and Phase 1 (complete)**. Phases 2–7 are added one at a time, after you finish the previous phase.

---

## Table of Contents

0. [Read me first](#0-read-me-first)
1. [The existing project (what we build on)](#1-the-existing-project-what-we-build-on)
2. [The seven-phase roadmap (syllabus)](#2-the-seven-phase-roadmap-syllabus)
3. [What you will have built at the end](#3-what-you-will-have-built-at-the-end)
4. [**Phase 1 — Testing fundamentals and web application concepts**](#phase-1--testing-fundamentals-and-web-application-concepts)
5. [Appendices](#appendices)

---

## 0. Read me first

### 0.1 How to use this workbook

Every lab has the same parts, so you always know where you are:

| Part | What it contains |
|---|---|
| **Lab number and title** | One focused skill |
| 🎯 **Learning objectives** | What you can do afterwards |
| **Prerequisites** | Which earlier labs must be finished |
| 📖 **Concepts** | The idea in simple language, **and why a QA automation engineer needs it** |
| 📁 **Files** | Which files you create or change, and why |
| 🛠️ **Steps** | Exact instructions and commands |
| 👀 **Expected results** | What your screen should show |
| 🚑 **Common errors** | Symptoms, causes and fixes |
| ✍️ **Practice exercise** | You do it alone; answers are hidden in collapsible blocks — try first |
| ✅ **Completion checklist** | A gate: do not start the next lab until every box is ticked |

Three kinds of activity are always labelled:

| Label | Meaning |
|---|---|
| 🧭 **Instructor-guided** | Follow along step by step; the instructor (or this workbook) shows the solution |
| ✍️ **Student independent** | You solve it yourself first; check the hidden answer afterwards |
| 🏆 **Optional challenge** | Extra stretch for fast finishers; not required for the checkpoint |

**Rules of the game**

1. **One phase at a time.** Each phase prepares you for the next. Do not skip.
2. **Type the code yourself.** Copy-pasting teaches nothing. Read each line, then type it.
3. **Understand before you automate.** In QA, the thinking comes first; the script comes last.
4. **Break things on purpose** when an exercise says so. Error messages you caused yourself teach the most.
5. **Write your own answers** before opening an answer block.

> **Working with an AI tutor or instructor?** Finish a phase, run the checks, and report the results. Say *"Phase N complete"* only when its checkpoint passes. The tutor should not unlock Phase N+1 before that.

### 0.2 Progress tracker

| Phase | Topic | Status in this file | Done |
|---|---|---|---|
| 1 | Testing fundamentals and web application concepts | **Included** | ☐ |
| 2 | TypeScript for automation testers | Next | ☐ |
| 3 | Playwright fundamentals | Planned | ☐ |
| 4 | Advanced UI automation | Planned | ☐ |
| 5 | Framework design and maintainability | Planned | ☐ |
| 6 | API testing and UI/API integration | Planned | ☐ |
| 7 | Cross-browser, quality and CI/CD | Planned | ☐ |

### 0.3 Tools you need

Check in **Windows PowerShell** (right-click Start → *Windows PowerShell* or *Terminal*):

```powershell
python --version      # 3.12 recommended (3.10+ works)
node --version        # 20 or newer (22 LTS is fine)
npm --version
git --version         # needed from Phase 7; install it now
code --version        # VS Code (recommended editor)
```

| Tool | Where to get it | Needed from |
|---|---|---|
| Python | <https://www.python.org/downloads/> (tick **Add python.exe to PATH**) | Phase 1 |
| Google Chrome or Microsoft Edge | Already installed on most PCs — **Phase 1 uses its DevTools** | Phase 1 |
| VS Code | <https://code.visualstudio.com/> | Phase 1 |
| Node.js LTS | <https://nodejs.org/> | Phase 2 |
| Git + a GitHub account | <https://git-scm.com/> · <https://github.com/> | Phase 7 |
| Docker Desktop (optional) | <https://www.docker.com/> | Phase 7 (optional lab) |

### 0.4 Conventions

* Commands run from the **project root** (`book-library-lab`) unless a step says otherwise.
* Code blocks marked `powershell` are for Windows PowerShell. Blocks marked `python`, `html`, `javascript`, `css`, `typescript` are file contents.
* **`curl.exe`, never `curl`.** In Windows PowerShell 5.1, `curl` is an alias for another command.
* **JSON for `curl.exe` goes in files** written with `-Encoding ascii` (PowerShell mangles quotes and `utf8` adds an invisible marker that breaks JSON).
* **Two terminals:** *Terminal A* runs the application; *Terminal B* is for everything else. Both need the Python virtual environment activated (`.\.venv\Scripts\Activate.ps1`).

---

## 1. The existing project (what we build on)

> **Rule of this course:** we **build on the existing project**. We do not start a new one, and we do not break what already works.

### 1.1 What exists today

You already have the **Book Library project** from the Django lab workbook:

```text
book-library-lab/
├── config/                 Django project settings and URL map
├── books/                  the Book API app (models, serializers, views, permissions, authentication)
├── backend_tests/          43 Django unit/API-behaviour tests             ← KEEP, keep passing
├── api-tests/              49 Playwright API tests over HTTPS (TypeScript) ← KEEP, keep passing
├── certs/                  local development certificate (git-ignored)
├── scratch/                helper files for curl.exe (git-ignored)
├── manage.py  requirements.txt  .gitignore  README.md
└── db.sqlite3              development database (git-ignored)
```

| Part | What it does | Reuse in this course |
|---|---|---|
| **REST API** (`/api/...`) | register, login, logout, `me`, list/view/add/delete books, CSRF token, health | ✅ The *backend* of the application under test. Phase 6 tests it again, together with the UI. |
| **Session authentication + CSRF** | cookie `sessionid`, token `X-CSRFToken` | ✅ Teaches authentication, cookies and storage state (Phase 4). |
| **Ownership rules** | everyone can read; owners can delete | ✅ Real business rules to test (authorization). |
| **`backend_tests/`** | fast in-memory tests of the Django code | ✅ Our **regression safety net** while we extend the app. |
| **`api-tests/`** | Playwright + TypeScript, API only, over HTTPS | ✅ A working example of `APIRequestContext`; **we do not touch it**. |
| **HTTPS / certificate setup** | self-signed certificate, uvicorn | ➡️ Optional. UI labs use plain `http://localhost:8000`; Phase 7 revisits HTTPS. |

### 1.2 What is missing for UI automation

| Gap | How we close it | When |
|---|---|---|
| The project has **no web pages** — only JSON. UI automation needs a UI. | A small, **supplied** front end (plain HTML, CSS and JavaScript — no React, no build step) served by Django. You **test** it; you do **not** build it. | Lab 1.0 |
| Books cannot be **edited** | `PATCH /api/books/{id}/` (owner or staff only) | Lab 1.0 |
| No **search** or **sort** | `?search=` and `?ordering=` on `GET /api/books/` | Lab 1.0 |

> **This is a QA course, not a development course.** The supplied files are given to you complete. Spend your time on understanding and testing them.

### 1.3 Features that do *not* exist (and are therefore not tested)

Real projects have gaps. Testers **document** them instead of inventing behaviour:

| Not available in this application | Consequence |
|---|---|
| Categories, ISBN, description fields | No category filter; books have only *title, author, published year, owner, added date* |
| Pagination | The list shows all books; the pagination labs use a small practice page in Phase 4 |
| Password reset, email verification | Not tested |
| Admin screens in the UI | Staff can delete via the API only |

---

## 2. The seven-phase roadmap (syllabus)

| Phase | Title | You learn | You add to the repository | Time |
|---|---|---|---|---|
| **1** | Testing fundamentals and web application concepts | Testing basics, client–server, HTTP, DOM, DevTools, selectors, UI→API traffic | The supplied UI; `docs/labs/phase-1/` (feature inventory, manual scenarios, locator notes, UI→API map) | 4–5 h |
| **2** | TypeScript for automation testers | Only the TypeScript you need: types, functions, interfaces, classes, async/await, JSON data | `e2e/practice/` practice files and a first reusable utility | 4–5 h |
| **3** | Playwright fundamentals | Installing Playwright, config, locators, assertions, auto-waiting, actions, dialogs, screenshots | `e2e/` project; first login, form, table and dialog tests | 6–7 h |
| **4** | Advanced UI automation | Locator chaining/filtering, dynamic elements, waits, iframes, popups, uploads, network mocking, storage state, data-driven tests, Inspector, trace | More tests; deliberately-broken debugging lab | 6–7 h |
| **5** | Framework design and maintainability | Page Objects, fixtures, test data, environments, auth setup, tags, naming | `pages/`, `fixtures/`, `utils/`; refactored tests | 6–7 h |
| **6** | API testing and integration | `APIRequestContext`, status/body/header checks, data setup and cleanup, UI+API workflows | `tests/api/`, `tests/integration/` | 5–6 h |
| **7** | Cross-browser, quality and CI/CD | Chromium/Firefox/WebKit, parallelism, retries, reports, Git/GitHub, GitHub Actions, Docker | `.github/workflows/`, reports, final README | 6–7 h |

**How each phase builds on the previous one**

```text
Phase 1  understand the app, the web, and the tools  ──▶  you know WHAT to test
Phase 2  learn the language of the tests              ──▶  you can READ and WRITE the code
Phase 3  write the first tests                        ──▶  you can AUTOMATE one thing
Phase 4  handle real-world difficulty                 ──▶  you can automate ANYTHING reliably
Phase 5  organize the code                            ──▶  you can MAINTAIN it
Phase 6  add the API layer                            ──▶  you can test FASTER and DEEPER
Phase 7  run it everywhere, automatically             ──▶  you can DELIVER it (CI/CD)
```

**Where things will live at the end of Phase 7**

```text
book-library-lab/
├── (existing: config/ books/ backend_tests/ api-tests/ certs/ manage.py ...)
├── ui/                          ← supplied front end (Phase 1, Lab 1.0)
├── e2e/                         ← THE Playwright framework you build (Phases 2–7)
│   ├── practice/                   Phase 2: TypeScript practice files
│   ├── tests/
│   │   ├── ui/authentication/      login, logout, protected pages, registration
│   │   ├── ui/books/               list, add, edit, delete, search, sort
│   │   ├── api/                    API tests
│   │   └── integration/            UI + API workflows
│   ├── pages/                      Page Objects
│   ├── fixtures/                   custom fixtures
│   ├── utils/                      test data, API client, environment
│   ├── playwright.config.ts  package.json  tsconfig.json  .env.example
├── .github/workflows/playwright.yml   Phase 7: CI
└── docs/
    ├── COURSE_SYLLABUS.md        (this roadmap)
    ├── PROJECT_STRUCTURE.md      (explains the tree above)
    ├── TESTING_GUIDE.md          (how to run UI and API tests)
    ├── FINAL_PROJECT.md          (final project requirements)
    └── labs/phase-1 … phase-7/   (your deliverables for each phase)
```

---

## 3. What you will have built at the end

1. A working Playwright automation framework (TypeScript).
2. A collection of UI test cases.
3. A collection of API test cases.
4. UI + API integration tests.
5. A cross-browser configured suite.
6. Test execution reports.
7. A GitHub repository.
8. A working CI/CD workflow.
9. A README documenting installation, execution and architecture.

And you will be able to answer the questions a hiring manager asks: *What should be automated — and what should not? How do you avoid flaky tests? When do you use the UI and when the API? How do you debug a failure that only happens in CI?*

---


# Phase 1 — Testing fundamentals and web application concepts

**Time:** about 4–5 hours · **Prerequisite:** the Django Book Library lab (through its Lab 5), or an equivalent running copy of the project · **No Playwright code is written in this phase** — on purpose.

### 🎯 Phase objectives

By the end of Phase 1 you can:

* explain what software testing is, and the difference between manual and automated testing;
* tell functional, regression, smoke and integration tests apart, and positive from negative tests;
* turn a feature into **test scenarios, test cases and test data**;
* explain client–server architecture, HTTP/HTTPS, methods and status codes;
* read HTML, CSS and the DOM, and explain how a browser renders a page;
* **inspect any web element** with browser DevTools (id, class, attributes, role, text) and write simple CSS and XPath selectors;
* show how a click in the browser turns into API requests.

> **Why this comes first.** Beginners open the editor and start writing selectors. Professionals first learn what the application is *supposed* to do. A test that checks the wrong thing — however well coded — is worthless. Phase 1 gives you the knowledge on which every later test is built.

### Labs in this phase

| Lab | Title | Type |
|---|---|---|
| 1.0 | Get the project ready (baseline + supplied UI) | 🧭 Instructor-guided |
| 1.1 | Testing fundamentals | 🧭 + ✍️ |
| 1.2 | How web applications work | 🧭 + ✍️ |
| 1.3 | Explore the application | ✍️ Student independent (guided tour) |
| 1.4 | Write manual test scenarios | 🧭 + ✍️ |
| 1.5 | Inspect elements with DevTools; selectors | 🧭 + ✍️ + 🏆 |
| 1.6 | How UI actions talk to the API | 🧭 + ✍️ |
| 1.7 | Phase 1 wrap-up: your Application Understanding Pack | ✍️ + knowledge check |

---

## Lab 1.0 — Get the project ready (baseline + supplied UI) 🧭

### 🎯 Learning objectives

* Prove the existing project works **before** changing anything (a *baseline*).
* Add the supplied web UI and three small API features to the existing project.
* Prove nothing broke, then run the application.

### Prerequisites

The Django project from the earlier workbook, working, with its virtual environment (`.venv`).

### 📖 Concepts

**Application under test (AUT).** The thing we test. Here: the Book Library — its web pages *and* its API.

**Baseline and regression.** A *regression* is something that used to work and now does not. Before you change a project, run its tests and write down the result. After the change, run them again. If the numbers match, you preserved existing behaviour. This habit is one of the main reasons teams automate.

**What the UI kit contains.** Three kinds of files:

| Kind | Files | Role |
|---|---|---|
| **Pages (HTML)** | `login.html`, `register.html`, `books.html`, `book-detail.html`, `book-form.html` | What the user sees. The same form page serves *Add book* and *Edit book*. |
| **Behaviour (JavaScript)** | `app.js` + a small script inside each page | Calls the API with `fetch`, shows messages, redirects |
| **Look (CSS)** | `styles.css` | Layout and colours |

Django serves them through `config/ui.py`. The API is unchanged except for three additions: **edit** (`PATCH`), **search** (`?search=`) and **sort** (`?ordering=`).

### 📁 Files you will create or change

| File | Action | Why |
|---|---|---|
| `books/views.py` | **replace** | adds search, sorting and `PATCH` (edit) |
| `config/ui.py` | **new** | serves the HTML/CSS/JS files |
| `config/urls.py` | **replace** | adds the page URLs next to the API URLs |
| `ui/styles.css`, `ui/app.js` | **new** | shared look and shared JavaScript helpers |
| `ui/login.html`, `ui/register.html` | **new** | authentication pages |
| `ui/books.html`, `ui/book-detail.html`, `ui/book-form.html` | **new** | book pages |
| `backend_tests/test_books_ui_features.py` | **new** | 11 tests for the three new API features |

### 🛠️ Steps

**Step 1 — Take the baseline** (Terminal B, project root)

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py test backend_tests
```

Write down the result. You should see `Ran 43 tests` and `OK`.

**Step 2 — Create the `ui` folder**

```powershell
mkdir ui
```

**Step 3 — Replace `books/views.py`**

The changes: `get_queryset` reads `?search=` and `?ordering=` (only whitelisted fields are accepted, so a client cannot sort by something private), and `BookDetailView` now allows `PATCH`. `http_method_names` still excludes `PUT`, so `PUT` keeps answering `405`.

**`books/views.py`**

```python
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
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

ALLOWED_ORDERING = {
    "id", "-id", "title", "-title", "author", "-author",
    "published_year", "-published_year", "created_at", "-created_at",
}


class BookListCreateView(generics.ListCreateAPIView):
    """
    GET /api/books/?search=dune&ordering=-title  -> list (search and ordering are optional)
    POST /api/books/                              -> create
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.select_related("owner")
        search = self.request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(author__icontains=search))
        ordering = self.request.query_params.get("ordering")
        if ordering in ALLOWED_ORDERING:
            queryset = queryset.order_by(ordering, "id")
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET one book, PATCH (partial update) or DELETE it. PUT is not offered."""
    queryset = Book.objects.select_related("owner")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrStaffOrReadOnly]
    http_method_names = ["get", "patch", "delete", "head", "options"]
```

**Step 4 — Create `config/ui.py`**

**`config/ui.py`**

```python
"""
Serves the small HTML/CSS/JS front end in the `ui/` folder.

This is the *application under test* for the Playwright UI labs. It is
deliberately tiny and framework-free so you can read all of it in an hour.
"""
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect


def serve(filename, content_type="text/html; charset=utf-8"):
    def view(request, **kwargs):
        body = (settings.BASE_DIR / "ui" / filename).read_bytes()
        return HttpResponse(body, content_type=content_type)

    return view


def home(request):
    return redirect("/books/")
```

**Step 5 — Replace `config/urls.py`**

**`config/urls.py`**

```python
from django.urls import include, path

from . import ui

urlpatterns = [
    path("api/", include("books.urls")),
    # --- the web pages (application under test for the Playwright labs) ---
    path("", ui.home),
    path("login/", ui.serve("login.html")),
    path("register/", ui.serve("register.html")),
    path("books/", ui.serve("books.html")),
    path("books/new/", ui.serve("book-form.html")),
    path("books/<int:pk>/", ui.serve("book-detail.html")),
    path("books/<int:pk>/edit/", ui.serve("book-form.html")),
    path("ui/app.js", ui.serve("app.js", "text/javascript; charset=utf-8")),
    path("ui/styles.css", ui.serve("styles.css", "text/css; charset=utf-8")),
]
```

**Step 6 — Create the shared files** (`ui/styles.css` and `ui/app.js`)

**`ui/styles.css`**

```css
:root { font-family: system-ui, sans-serif; color: #1b1f24; background: #f6f7f9; }
body { margin: 0; }
/* Author CSS such as 'display:inline-block' would otherwise beat the browser's rule for [hidden]. */
[hidden] { display: none !important; }
.topbar { display: flex; justify-content: space-between; align-items: center; padding: .75rem 1.5rem; background: #1f3a5f; color: #fff; }
.topbar a.brand { color: #fff; font-weight: 700; text-decoration: none; }
.topbar nav { display: flex; gap: 1rem; align-items: center; }
main { max-width: 56rem; margin: 1.5rem auto; padding: 0 1rem; }
h1 { margin-top: 0; }
label { display: block; font-weight: 600; margin: .75rem 0 .25rem; }
input, select { font: inherit; padding: .4rem .5rem; min-width: 16rem; max-width: 100%; box-sizing: border-box; }
button, a.button { font: inherit; padding: .45rem .9rem; border: 1px solid #1f3a5f; background: #1f3a5f; color: #fff; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
button.secondary, a.secondary { background: #fff; color: #1f3a5f; }
button.danger { background: #b3261e; border-color: #b3261e; }
button:disabled { opacity: .5; cursor: not-allowed; }
.field-error, .form-error { color: #b3261e; margin: .25rem 0 0; }
.form-error { padding: .5rem .75rem; background: #fdecea; border: 1px solid #f5c2be; border-radius: 4px; }
.flash, .toast { padding: .5rem .75rem; border-radius: 4px; background: #e6f4ea; border: 1px solid #b7dfc2; margin: .75rem 0; }
.toast.error { background: #fdecea; border-color: #f5c2be; }
.toolbar { display: flex; flex-wrap: wrap; gap: 1rem; align-items: end; margin: 1rem 0; }
table { width: 100%; border-collapse: collapse; background: #fff; table-layout: fixed; }
th, td { text-align: left; padding: .5rem .6rem; border-bottom: 1px solid #e3e6ea; overflow-wrap: anywhere; vertical-align: top; }
td.actions { display: flex; gap: .5rem; flex-wrap: wrap; }
dialog { border: 1px solid #999; border-radius: 6px; padding: 1.25rem; max-width: 24rem; }
dl { display: grid; grid-template-columns: 8rem 1fr; gap: .4rem 1rem; }
dt { font-weight: 600; } dd { margin: 0; overflow-wrap: anywhere; }
.actions-row { display: flex; gap: .75rem; margin-top: 1rem; }
@media (max-width: 600px) { th:nth-child(3), td:nth-child(3), th:nth-child(4), td:nth-child(4) { display: none; } input, select { min-width: 0; width: 100%; } }
```

**`ui/app.js`**

```javascript
/* Shared helpers for the Book Library pages. No framework, no build step. */
const App = (() => {
  async function csrfToken() {
    const res = await fetch('/api/csrf/');
    return (await res.json()).csrfToken;
  }

  /** Calls the JSON API. Unsafe methods automatically send the CSRF token. */
  async function api(method, url, body) {
    const options = { method, headers: { Accept: 'application/json' } };
    if (method !== 'GET') options.headers['X-CSRFToken'] = await csrfToken();
    if (body !== undefined) {
      options.headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(body);
    }
    const res = await fetch(url, options);
    let data = null;
    if (res.status !== 204) {
      try { data = await res.json(); } catch { /* no JSON body */ }
    }
    return { status: res.status, ok: res.ok, data };
  }

  /** A message to show on the NEXT page (survives a redirect). */
  function flash(message) { sessionStorage.setItem('flash', message); }

  function showFlash() {
    const message = sessionStorage.getItem('flash');
    if (!message) return;
    sessionStorage.removeItem('flash');
    const banner = document.getElementById('flash');
    if (banner) { banner.textContent = message; banner.hidden = false; }
    else toast(message);
  }

  let toastTimer;
  /** Notification that disappears by itself after 4 seconds. */
  function toast(message, kind = 'success') {
    const el = document.getElementById('toast');
    el.textContent = message;
    el.className = 'toast ' + kind;
    el.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { el.hidden = true; }, 4000);
  }

  /** Protected pages call this first. Anonymous visitors are sent to the login page. */
  async function requireLogin() {
    const res = await api('GET', '/api/me/');
    if (res.status === 401) {
      location.replace('/login/?next=' + encodeURIComponent(location.pathname));
      return null;
    }
    document.getElementById('whoami').textContent = 'Signed in as ' + res.data.username;
    document.getElementById('signout').addEventListener('click', signOut);
    document.getElementById('content').hidden = false;
    showFlash();
    return res.data;
  }

  async function signOut() {
    await api('POST', '/api/logout/');
    flash('You have been signed out.');
    location.assign('/login/');
  }

  /** Only follow ?next= when it is a path on this site. */
  function nextUrl() {
    const next = new URLSearchParams(location.search).get('next');
    return next && next.startsWith('/') && !next.startsWith('//') ? next : '/books/';
  }

  function setError(id, message) {
    const el = document.getElementById(id);
    el.textContent = message || '';
    el.hidden = !message;
  }

  function messages(value) {
    return Array.isArray(value) ? value.join(' ') : String(value);
  }

  return { api, flash, showFlash, toast, requireLogin, signOut, nextUrl, setError, messages };
})();
```

**Step 7 — Create the authentication pages**

**`ui/login.html`**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sign in – Book Library</title>
  <link rel="stylesheet" href="/ui/styles.css">
</head>
<body>
  <header class="topbar"><a class="brand" href="/books/">Book Library</a></header>
  <main>
    <h1>Sign in</h1>
    <p id="flash" class="flash" role="status" hidden></p>
    <form id="login-form" novalidate>
      <label for="username">Username</label>
      <input id="username" name="username" autocomplete="username">
      <p id="username-error" class="field-error" hidden></p>

      <label for="password">Password</label>
      <input id="password" name="password" type="password" autocomplete="current-password">
      <p id="password-error" class="field-error" hidden></p>

      <p id="form-error" class="form-error" role="alert" hidden></p>
      <div class="actions-row"><button type="submit">Sign in</button></div>
    </form>
    <p>No account yet? <a href="/register/">Create an account</a></p>
  </main>
  <script src="/ui/app.js"></script>
  <script>
    App.showFlash();
    document.getElementById('login-form').addEventListener('submit', async (event) => {
      event.preventDefault();
      const username = document.getElementById('username').value.trim();
      const password = document.getElementById('password').value;
      App.setError('username-error', username ? '' : 'Username is required.');
      App.setError('password-error', password ? '' : 'Password is required.');
      App.setError('form-error', '');
      if (!username || !password) return;

      const res = await App.api('POST', '/api/login/', { username, password });
      if (res.ok) { location.assign(App.nextUrl()); return; }
      App.setError('form-error', res.status === 401
        ? 'Invalid username or password.'
        : 'Sign-in failed. Please try again.');
    });
  </script>
</body>
</html>
```

**`ui/register.html`**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Create account – Book Library</title>
  <link rel="stylesheet" href="/ui/styles.css">
</head>
<body>
  <header class="topbar"><a class="brand" href="/books/">Book Library</a></header>
  <main>
    <h1>Create an account</h1>
    <form id="register-form" novalidate>
      <label for="username">Username</label>
      <input id="username" name="username" autocomplete="username">
      <p id="username-error" class="field-error" hidden></p>

      <label for="password">Password</label>
      <input id="password" name="password" type="password" autocomplete="new-password">
      <p id="password-error" class="field-error" hidden></p>

      <p id="form-error" class="form-error" role="alert" hidden></p>
      <div class="actions-row"><button id="submit" type="submit" disabled>Create account</button></div>
    </form>
    <p>Already registered? <a href="/login/">Sign in</a></p>
  </main>
  <script src="/ui/app.js"></script>
  <script>
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const submit = document.getElementById('submit');
    // The button stays disabled until BOTH fields contain something.
    function updateButton() { submit.disabled = !(username.value.trim() && password.value); }
    username.addEventListener('input', updateButton);
    password.addEventListener('input', updateButton);

    document.getElementById('register-form').addEventListener('submit', async (event) => {
      event.preventDefault();
      ['username-error', 'password-error', 'form-error'].forEach((id) => App.setError(id, ''));
      const res = await App.api('POST', '/api/register/', {
        username: username.value.trim(),
        password: password.value,
      });
      if (res.status === 201) {
        App.flash('Account created. Please sign in.');
        location.assign('/login/');
        return;
      }
      if (res.status === 400 && res.data) {
        if (res.data.username) App.setError('username-error', App.messages(res.data.username));
        if (res.data.password) App.setError('password-error', App.messages(res.data.password));
        return;
      }
      App.setError('form-error', 'Registration failed. Please try again.');
    });
  </script>
</body>
</html>
```

**Step 8 — Create the book pages**

**`ui/books.html`**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Books – Book Library</title>
  <link rel="stylesheet" href="/ui/styles.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/books/">Book Library</a>
    <nav aria-label="Account">
      <span id="whoami"></span>
      <button type="button" id="signout" class="secondary">Sign out</button>
    </nav>
  </header>
  <main id="content" hidden>
    <h1>Books</h1>
    <div id="toast" role="status" aria-live="polite" hidden></div>

    <div class="toolbar">
      <div>
        <label for="search">Search books</label>
        <input id="search" type="search" placeholder="Search by title or author">
      </div>
      <div>
        <label for="sort">Sort by</label>
        <select id="sort">
          <option value="-id">Recently added</option>
          <option value="title">Title (A–Z)</option>
          <option value="-title">Title (Z–A)</option>
          <option value="published_year">Year (oldest first)</option>
          <option value="-published_year">Year (newest first)</option>
        </select>
      </div>
      <a class="button" href="/books/new/">Add book</a>
    </div>

    <p id="loading" hidden>Loading books…</p>
    <p id="count"></p>
    <p id="empty" hidden></p>

    <table id="books-table" hidden>
      <caption hidden>Book list</caption>
      <thead><tr><th>Title</th><th>Author</th><th>Year</th><th>Owner</th><th>Actions</th></tr></thead>
      <tbody id="book-rows"></tbody>
    </table>

    <dialog id="confirm-dialog" aria-labelledby="confirm-title">
      <h2 id="confirm-title">Delete book?</h2>
      <p id="confirm-text"></p>
      <div class="actions-row">
        <button type="button" id="confirm-cancel" class="secondary">Cancel</button>
        <button type="button" id="confirm-delete" class="danger">Delete</button>
      </div>
    </dialog>
  </main>
  <script src="/ui/app.js"></script>
  <script>
    const rows = document.getElementById('book-rows');
    const table = document.getElementById('books-table');
    const dialog = document.getElementById('confirm-dialog');
    let me = null;
    let requestCounter = 0;
    let pendingDelete = null;

    function cell(text) { const td = document.createElement('td'); td.textContent = text; return td; }

    function render(books) {
      rows.replaceChildren();
      for (const book of books) {
        const tr = document.createElement('tr');
        tr.dataset.testid = 'book-row';

        const titleCell = document.createElement('td');
        const link = document.createElement('a');
        link.href = '/books/' + book.id + '/';
        link.textContent = book.title;
        titleCell.append(link);
        tr.append(titleCell, cell(book.author), cell(book.published_year ?? '—'), cell(book.owner ?? '—'));

        const actions = document.createElement('td');
        actions.className = 'actions';
        if (me && book.owner === me.username) {            // only the owner sees these controls
          const edit = document.createElement('a');
          edit.href = '/books/' + book.id + '/edit/';
          edit.className = 'button secondary';
          edit.textContent = 'Edit';
          edit.setAttribute('aria-label', 'Edit ' + book.title);
          const del = document.createElement('button');
          del.type = 'button';
          del.className = 'danger';
          del.textContent = 'Delete';
          del.setAttribute('aria-label', 'Delete ' + book.title);
          del.addEventListener('click', () => askDelete(book));
          actions.append(edit, del);
        }
        tr.append(actions);
        rows.append(tr);
      }
      table.hidden = books.length === 0;
      document.getElementById('count').textContent = books.length === 1 ? '1 book' : books.length + ' books';
      const empty = document.getElementById('empty');
      const term = document.getElementById('search').value.trim();
      empty.hidden = books.length !== 0;
      empty.textContent = term ? 'No books match “' + term + '”.' : 'No books yet. Add the first one!';
    }

    async function load() {
      const ticket = ++requestCounter;                       // ignore out-of-date responses
      document.getElementById('loading').hidden = false;
      const params = new URLSearchParams({ ordering: document.getElementById('sort').value });
      const term = document.getElementById('search').value.trim();
      if (term) params.set('search', term);
      const res = await App.api('GET', '/api/books/?' + params);
      if (ticket !== requestCounter) return;
      document.getElementById('loading').hidden = true;
      if (!res.ok) { App.toast('Could not load books.', 'error'); return; }
      render(res.data);
    }

    function askDelete(book) {
      pendingDelete = book;
      document.getElementById('confirm-text').textContent = 'This will permanently delete “' + book.title + '”.';
      dialog.showModal();
    }

    document.getElementById('confirm-cancel').addEventListener('click', () => { pendingDelete = null; dialog.close(); });
    document.getElementById('confirm-delete').addEventListener('click', async () => {
      const book = pendingDelete;
      dialog.close();
      const res = await App.api('DELETE', '/api/books/' + book.id + '/');
      if (res.status === 204) App.toast('Book deleted.');
      else if (res.status === 403) App.toast('You do not have permission to delete this book.', 'error');
      else App.toast('Could not delete the book.', 'error');
      load();
    });

    let searchTimer;
    document.getElementById('search').addEventListener('input', () => {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(load, 250);                   // small debounce while typing
    });
    document.getElementById('sort').addEventListener('change', load);

    App.requireLogin().then((user) => { if (user) { me = user; load(); } });
  </script>
</body>
</html>
```

**`ui/book-detail.html`**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Book details – Book Library</title>
  <link rel="stylesheet" href="/ui/styles.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/books/">Book Library</a>
    <nav aria-label="Account">
      <span id="whoami"></span>
      <button type="button" id="signout" class="secondary">Sign out</button>
    </nav>
  </header>
  <main id="content" hidden>
    <div id="toast" role="status" aria-live="polite" hidden></div>
    <p id="not-found" role="alert" hidden>Book not found.</p>
    <article id="book" hidden>
      <h1 id="book-title"></h1>
      <dl>
        <dt>Author</dt><dd id="book-author"></dd>
        <dt>Published</dt><dd id="book-year"></dd>
        <dt>Added by</dt><dd id="book-owner"></dd>
      </dl>
      <div class="actions-row">
        <a class="button secondary" href="/books/">Back to books</a>
        <a id="edit-link" class="button" href="#" hidden>Edit book</a>
        <button id="delete-button" type="button" class="danger" hidden>Delete book</button>
      </div>
    </article>

    <dialog id="confirm-dialog" aria-labelledby="confirm-title">
      <h2 id="confirm-title">Delete book?</h2>
      <p id="confirm-text"></p>
      <div class="actions-row">
        <button type="button" id="confirm-cancel" class="secondary">Cancel</button>
        <button type="button" id="confirm-delete" class="danger">Delete</button>
      </div>
    </dialog>
  </main>
  <script src="/ui/app.js"></script>
  <script>
    const id = location.pathname.match(/\/books\/(\d+)\//)[1];
    const dialog = document.getElementById('confirm-dialog');

    App.requireLogin().then(async (me) => {
      if (!me) return;
      const res = await App.api('GET', '/api/books/' + id + '/');
      if (res.status === 404) { document.getElementById('not-found').hidden = false; return; }
      const book = res.data;
      document.title = book.title + ' – Book Library';
      document.getElementById('book-title').textContent = book.title;
      document.getElementById('book-author').textContent = book.author;
      document.getElementById('book-year').textContent = book.published_year ?? 'Unknown';
      document.getElementById('book-owner').textContent = book.owner ?? 'Unknown';
      document.getElementById('book').hidden = false;
      if (book.owner === me.username) {
        const edit = document.getElementById('edit-link');
        edit.href = '/books/' + id + '/edit/';
        edit.hidden = false;
        document.getElementById('delete-button').hidden = false;
      }
      document.getElementById('delete-button').addEventListener('click', () => {
        document.getElementById('confirm-text').textContent = 'This will permanently delete “' + book.title + '”.';
        dialog.showModal();
      });
    });

    document.getElementById('confirm-cancel').addEventListener('click', () => dialog.close());
    document.getElementById('confirm-delete').addEventListener('click', async () => {
      dialog.close();
      const res = await App.api('DELETE', '/api/books/' + id + '/');
      if (res.status === 204) { App.flash('Book deleted.'); location.assign('/books/'); }
      else App.toast('Could not delete the book.', 'error');
    });
  </script>
</body>
</html>
```

**`ui/book-form.html`**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Book form – Book Library</title>
  <link rel="stylesheet" href="/ui/styles.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/books/">Book Library</a>
    <nav aria-label="Account">
      <span id="whoami"></span>
      <button type="button" id="signout" class="secondary">Sign out</button>
    </nav>
  </header>
  <main id="content" hidden>
    <h1 id="heading">Add book</h1>
    <div id="toast" role="status" aria-live="polite" hidden></div>
    <p id="not-found" role="alert" hidden>Book not found.</p>
    <form id="book-form" novalidate>
      <label for="title">Title</label>
      <input id="title" name="title" maxlength="200">
      <p id="title-error" class="field-error" hidden></p>

      <label for="author">Author</label>
      <input id="author" name="author" maxlength="120">
      <p id="author-error" class="field-error" hidden></p>

      <label for="year">Published year</label>
      <input id="year" name="published_year" inputmode="numeric">
      <p id="year-error" class="field-error" hidden></p>

      <p id="form-error" class="form-error" role="alert" hidden></p>
      <div class="actions-row">
        <button id="save" type="submit">Save book</button>
        <a class="button secondary" href="/books/">Cancel</a>
      </div>
    </form>
  </main>
  <script src="/ui/app.js"></script>
  <script>
    const editMatch = location.pathname.match(/\/books\/(\d+)\/edit\//);
    const bookId = editMatch ? editMatch[1] : null;
    const form = document.getElementById('book-form');
    const fields = ['title', 'author', 'year'];

    if (bookId) {
      document.getElementById('heading').textContent = 'Edit book';
      document.getElementById('save').textContent = 'Save changes';
      document.title = 'Edit book – Book Library';
    } else {
      document.title = 'Add book – Book Library';
    }

    App.requireLogin().then(async (me) => {
      if (!me || !bookId) return;
      const res = await App.api('GET', '/api/books/' + bookId + '/');
      if (res.status === 404) { form.hidden = true; document.getElementById('not-found').hidden = false; return; }
      document.getElementById('title').value = res.data.title;
      document.getElementById('author').value = res.data.author;
      document.getElementById('year').value = res.data.published_year ?? '';
    });

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      fields.concat('form').forEach((name) => App.setError(name + '-error', ''));
      const title = document.getElementById('title').value.trim();
      const author = document.getElementById('author').value.trim();
      const yearText = document.getElementById('year').value.trim();

      let invalid = false;
      if (!title) { App.setError('title-error', 'Title is required.'); invalid = true; }
      if (!author) { App.setError('author-error', 'Author is required.'); invalid = true; }
      if (yearText && !/^\d+$/.test(yearText)) { App.setError('year-error', 'Year must be a whole number.'); invalid = true; }
      if (invalid) return;                                   // nothing is sent to the server

      const payload = { title, author, published_year: yearText ? Number(yearText) : null };
      const res = bookId
        ? await App.api('PATCH', '/api/books/' + bookId + '/', payload)
        : await App.api('POST', '/api/books/', payload);

      if (res.ok) {
        App.flash(bookId ? 'Book updated.' : 'Book added.');
        location.assign('/books/');
        return;
      }
      if (res.status === 400 && res.data) {
        if (res.data.title) App.setError('title-error', App.messages(res.data.title));
        if (res.data.author) App.setError('author-error', App.messages(res.data.author));
        if (res.data.published_year) App.setError('year-error', App.messages(res.data.published_year));
        return;
      }
      App.setError('form-error', res.status === 403
        ? 'You do not have permission to change this book.'
        : 'The book could not be saved. Please try again.');
    });
  </script>
</body>
</html>
```

**Step 9 — Add tests for the new API features, then compare with the baseline**

**`backend_tests/test_books_ui_features.py`**

```python
from django.test import TestCase
from rest_framework.test import APIClient

from books.models import Book

from .helpers import logged_in_client, make_user


class SearchAndOrderingTests(TestCase):
    def setUp(self):
        owner = make_user("alice")
        Book.objects.create(title="Dune", author="Frank Herbert", published_year=1965, owner=owner)
        Book.objects.create(title="Emma", author="Jane Austen", published_year=1815, owner=owner)
        Book.objects.create(title="Persuasion", author="Jane Austen", published_year=1817, owner=owner)

    def titles(self, query=""):
        return [b["title"] for b in APIClient().get(f"/api/books/{query}").json()]

    def test_search_matches_title_case_insensitively(self):
        self.assertEqual(self.titles("?search=dUnE"), ["Dune"])

    def test_search_matches_author(self):
        self.assertEqual(self.titles("?search=austen"), ["Emma", "Persuasion"])

    def test_search_without_match_returns_empty_list(self):
        self.assertEqual(self.titles("?search=zzz"), [])

    def test_ordering_by_title_descending(self):
        self.assertEqual(self.titles("?ordering=-title"), ["Persuasion", "Emma", "Dune"])

    def test_ordering_by_year(self):
        self.assertEqual(self.titles("?ordering=published_year"), ["Emma", "Persuasion", "Dune"])

    def test_unknown_ordering_is_ignored(self):
        self.assertEqual(self.titles("?ordering=owner__password"), ["Dune", "Emma", "Persuasion"])


class UpdateTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.book = Book.objects.create(title="Emma", author="Jane Austen", owner=self.alice)
        self.url = f"/api/books/{self.book.id}/"

    def test_owner_can_patch_and_other_fields_stay(self):
        response = logged_in_client(self.alice).patch(self.url, {"title": "Emma (2nd ed.)"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Emma (2nd ed.)")
        self.assertEqual(response.json()["author"], "Jane Austen")

    def test_other_user_cannot_patch(self):
        bob = make_user("bob")
        self.assertEqual(logged_in_client(bob).patch(self.url, {"title": "Hacked"}).status_code, 403)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Emma")

    def test_anonymous_cannot_patch(self):
        self.assertEqual(APIClient().patch(self.url, {"title": "x"}).status_code, 401)

    def test_invalid_patch_returns_400(self):
        response = logged_in_client(self.alice).patch(self.url, {"title": "   "})
        self.assertEqual(response.status_code, 400)

    def test_put_is_still_not_allowed(self):
        response = logged_in_client(self.alice).put(self.url, {"title": "x", "author": "y"})
        self.assertEqual(response.status_code, 405)
```

```powershell
python manage.py test backend_tests
```

**Step 10 — Run the application** (Terminal A)

```powershell
python manage.py migrate
python manage.py runserver
```

Leave it running. In Terminal B:

```powershell
curl.exe -i http://localhost:8000/login/
curl.exe -i http://localhost:8000/
curl.exe -i http://localhost:8000/api/health/
```

Now open <http://localhost:8000/> in **Chrome or Edge**.

### 👀 Expected results

* Step 1: `Ran 43 tests … OK` (your baseline).
* Step 9: `Ran 54 tests … OK` — the original 43 **plus** 11 new ones. *Nothing that worked before is broken.*
* Step 10, first `curl.exe`: `HTTP/1.1 200 OK`, `Content-Type: text/html; charset=utf-8`, then the HTML text.
* Second: `HTTP/1.1 302 Found` with `Location: /books/` — the root redirects.
* Third: `HTTP/1.1 200 OK` and `{"status":"ok"}`.
* Browser: you land on a **Sign in** page. The address bar says `http://localhost:8000/login/?next=%2Fbooks%2F` — the Books page is protected, so the app sent you to sign in and remembered where you wanted to go. *Note this: it is your first discovered business rule.*

### 🚑 Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `FileNotFoundError: …\ui\login.html` | `ui` folder in the wrong place, or a file missing | `ui` must sit next to `manage.py`; check with `Get-ChildItem ui` |
| Browser shows `404 Not Found` for `/login/` | `config/urls.py` not replaced | Redo Step 5 and restart the server |
| Page loads but looks plain / buttons do nothing | `ui/app.js` or `ui/styles.css` missing or misnamed | Check both files exist; reload with **Ctrl+F5** |
| `ImportError: cannot import name 'Q'` or similar | Typo while copying `views.py` | Compare line by line with Step 3 |
| You sign in but are sent back to the sign-in page | The browser refused the `Secure` session cookie on plain HTTP | Use **Chrome or Edge** on `http://localhost:8000` (they accept it for localhost). Firefox/Safari behaviour can differ. |
| `DisallowedHost` | You used another host name | Use `localhost` or `127.0.0.1` |
| `Error: That port is already in use.` | Something else uses port 8000 | `python manage.py runserver 8001` and use that port everywhere |
| Test count is not 54 | A test file is missing or misnamed | Test files must start with `test_` and live in `backend_tests\` |

### ✍️ Practice exercise (student independent)

List **three observations** that prove, without looking at code, that the application is running correctly (for example: a status code, a redirect, a page title). Then stop the server and observe what the browser shows. What does that tell you about where the HTML comes from?

<details><summary>Answer</summary>

Examples: `/api/health/` returns `{"status":"ok"}`; `/` redirects to `/books/`; the Sign in page has the title *Sign in – Book Library*. With the server stopped the browser shows a connection error: **the HTML, CSS and JavaScript all come from the server** — the browser only displays what it is sent.
</details>

### ✅ Completion checklist

- [ ] I recorded the baseline: **43 tests OK**.
- [ ] After adding the UI kit the suite shows **54 tests OK**.
- [ ] `http://localhost:8000/` opens the Sign in page in my browser.
- [ ] I can say which three API features were added and which stayed unchanged.

---

## Lab 1.1 — Testing fundamentals 🧭 + ✍️

### 🎯 Learning objectives

* Define software testing and explain why we automate.
* Distinguish functional, regression, smoke and integration testing.
* Distinguish test scenarios, test cases and test data.
* Design positive, negative and boundary tests.

### Prerequisites

Lab 1.0.

### 📖 Concepts

#### 1.1.A What is software testing?

**Testing is the activity of checking whether software behaves as it should, in order to find problems before users do.** It answers: *Does the product do what the requirements say? What could go wrong?* Testing never proves there are no bugs; it builds *confidence* and finds *risks*.

> **Why a QA engineer cares.** Your job is not to "click everything". It is to provide *information about quality*, quickly and reliably, so the team can decide whether to release.

#### 1.1.B Manual vs automation testing

| | **Manual testing** | **Automation testing** |
|---|---|---|
| Who runs it | A person | A program (e.g. Playwright) |
| Strong at | Exploring, judging look and feel, first look at new features | Repeating the same checks fast and exactly, every day |
| Weak at | Repetition, speed, consistency | New or changing features, "does this feel right?" |
| Cost | Same effort every time | High to build, cheap to repeat |

Automation does **not** replace manual testing; it frees people for the work that needs a brain.

**What should be automated?** Checks that are **repeated often**, **important to the business**, **stable**, and **precise** (clear right/wrong answer).
**What should not?** Features that change every week, one-off checks, visual/"does it look nice" judgements, and anything whose automation costs more than doing it by hand.

#### 1.1.C Types of testing (the ones you will use)

| Type | Question it answers | Example in our app |
|---|---|---|
| **Functional** | Does a feature do what it should? | Adding a book saves it and shows it in the list |
| **Smoke** | Is the build alive enough to test further? | Sign in works; the book list opens |
| **Regression** | Did a change break something that worked? | After adding *Edit*, can we still *Delete*? (Lab 1.0's 43 → 54 tests) |
| **Integration** | Do parts work *together*? | A book added in the UI is really stored by the API |

*(There are many more — performance, security, usability — but these four drive this course.)*

#### 1.1.D Scenario, test case, test data

| Term | Meaning | Example |
|---|---|---|
| **Test scenario** | *What* to check, in one line | "A registered user can sign in" |
| **Test case** | *How*: ID, preconditions, steps, data, expected result | See below |
| **Test data** | The concrete values used | username `qa_anna`, password `S3cure-Lab-Passw0rd!` |

**One scenario → many test cases.** Every different *data set* or *path* is a new case.

| ID | Scenario | Data | Expected |
|---|---|---|---|
| AUTH-02 | Sign in with valid credentials | correct user + password | Goes to the book list |
| AUTH-03 | Sign in with a wrong password | correct user, wrong password | Error "Invalid username or password." |
| AUTH-04 | Sign in with nothing typed | empty fields | "Username is required." and "Password is required." |

#### 1.1.E Positive, negative and boundary testing

| Kind | Idea | Example |
|---|---|---|
| **Positive** | Valid input; the *happy path* works | Add a book with title, author, year 1965 |
| **Negative** | Invalid input or action; the system must refuse **safely** and say why | Add a book with no title → message, nothing saved |
| **Boundary** | Values at the **edge** of what is allowed — where bugs hide | Year **999** (too low), **1000** (lowest valid), **2100** (highest valid), **2101** (too high) |

Rule of thumb: for every limit, test **just inside**, **exactly on**, and **just outside** it.

> **A real detail of our application:** the *Title* box stops you typing more than 200 characters (an HTML `maxlength`), but the **API** also rejects 201 characters with `400`. Why test both? Because a UI limit is only a convenience; anybody can call the API directly. *The server must defend itself.*

### 🛠️ Steps

**Step 1 (🧭 guided) — Classify.** For each statement, decide the test type (functional / smoke / regression / integration) and whether it is positive, negative or boundary. Write your answers, then open the answer block.

1. After deploying, a script checks that the Sign in page opens.
2. A tester enters a published year of 2101.
3. After a code change, the whole delete-book flow is re-run to be sure it still works.
4. A tester adds a book in the browser, then checks the API returns the same title.
5. A tester signs in with a valid user and password.

<details><summary>Answer</summary>

1. **Smoke**, positive.
2. **Functional**, **negative + boundary** (just outside the limit).
3. **Regression**, positive.
4. **Integration** (UI + API), positive.
5. **Functional** (also a smoke candidate), positive.
</details>

**Step 2 (🧭 guided) — Boundary table.** For *Published year* (valid 1000–2100, optional) fill the table:

| Input | Valid? | Expected result |
|---|---|---|
| 999 | | |
| 1000 | | |
| 2100 | | |
| 2101 | | |
| *(empty)* | | |
| `abc` | | |

<details><summary>Answer</summary>

| Input | Valid? | Expected result |
|---|---|---|
| 999 | ❌ | Server message "Year must be between 1000 and 2100." |
| 1000 | ✅ | Book saved |
| 2100 | ✅ | Book saved |
| 2101 | ❌ | Same server message |
| *(empty)* | ✅ | Saved; year shown as "—" |
| `abc` | ❌ | Browser-side message "Year must be a whole number." (nothing sent to the server) |

(You will verify these by hand in Lab 1.3.)
</details>

**Step 3 (✍️ independent) — Decide what to automate.** For each item write **Automate / Manual / Don't test**, with a reason:

1. Sign in works (runs before every release).
2. Whether the blue header colour is a nice shade of blue.
3. Search finds a book by author.
4. A feature the product owner says will be removed next week.

<details><summary>Answer</summary>

1. **Automate** — critical, repeated, precise. 2. **Manual** (or skip) — subjective. 3. **Automate** — important and precise (a good UI *and* API candidate). 4. **Don't automate** — the effort will be wasted.
</details>

### 🚑 Common errors (thinking mistakes)

| Mistake | Better habit |
|---|---|
| "Test everything." | Choose tests by **risk and value**. |
| Only testing the happy path | Always add negative and boundary cases. |
| Vague expected results ("works fine") | Write a **specific, observable** result ("message 'Book added.' appears"). |
| Automating a test you never ran by hand | **Manual first.** If you cannot do it by hand, you cannot automate it. |

### ✍️ Practice exercise (student independent)

Write **five test cases** (ID, scenario, data, expected result) for *Register a new account*. Include at least two negative cases. (You will see the registration page in Lab 1.3; if you want, peek first.)

<details><summary>Answer (example)</summary>

| ID | Scenario | Data | Expected |
|---|---|---|---|
| REG-01 | Register with valid new data | new unique name, strong password | Goes to Sign in page; message "Account created. Please sign in." |
| REG-02 | Name already taken | an existing username | "A user with that username already exists." |
| REG-03 | Weak password | `12345678` | A password message (e.g. "too common" / "entirely numeric") |
| REG-04 | Fields empty | nothing typed | **Create account** button is disabled |
| REG-05 | Name differs only in capitals | `ALICE` when `alice` exists | Rejected as duplicate (names are compared case-insensitively) |
</details>

### ✅ Completion checklist

- [ ] I can explain testing, and manual vs automation, in my own words.
- [ ] I can name four test types and give an example of each from the Book Library.
- [ ] I can write a scenario, a test case and its test data.
- [ ] I can design positive, negative and boundary tests for a field.

---

## Lab 1.2 — How web applications work 🧭 + ✍️

### 🎯 Learning objectives

* Explain client–server architecture and frontend vs backend.
* Read an HTTP request and response; know methods and status codes.
* Explain HTML, CSS, the DOM and JavaScript, and how a browser renders a page.

### Prerequisites

Lab 1.0 (application running).

### 📖 Concepts

#### 1.2.A Client–server architecture

```text
   CLIENT (your browser)                       SERVER (Django)                     DATABASE
 ┌────────────────────────┐   HTTP request   ┌─────────────────────────┐        ┌───────────┐
 │ shows pages            │ ───────────────▶ │ sends HTML/CSS/JS files │        │  SQLite   │
 │ runs JavaScript        │                  │ answers API calls       │ ◀────▶ │ books,    │
 │ remembers cookies      │ ◀─────────────── │ checks who you are      │        │ users,    │
 └────────────────────────┘   HTTP response  └─────────────────────────┘        │ sessions  │
                                                                                 └───────────┘
```

| | **Frontend** (client side) | **Backend** (server side) |
|---|---|---|
| Runs in | The browser | On the server |
| Our files | `ui/*.html`, `ui/app.js`, `ui/styles.css` | `books/*.py`, `config/*.py` |
| Responsible for | What you see and click; showing messages | Rules, security, saving data |
| Can be trusted? | **No** — the user controls their browser | **Yes** — it makes the final decision |

> **Why a QA engineer cares.** Because the browser cannot be trusted, rules must be checked on the server — so you test *both* layers. And when a UI test fails you must be able to say *which side* is at fault.

#### 1.2.B HTTP and HTTPS

HTTP is plain text sent between client and server. **Request**:

```http
GET /api/books/?search=dune HTTP/1.1
Host: localhost:8000
Accept: application/json
Cookie: sessionid=79a6kpjmokk0djbp2lp72t09nqxeiqop
```

**Response**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[{"id":4,"title":"Dune","author":"Frank Herbert","published_year":1965,"owner":"anna","created_at":"2026-11-06T09:12:44.512Z"}]
```

| Part | Request | Response |
|---|---|---|
| Start line | method + path (`GET /api/books/`) | status code (`200 OK`) |
| Headers | `Cookie`, `Content-Type`, `X-CSRFToken`, `Origin` | `Content-Type`, `Set-Cookie`, `Allow` |
| Body | data you send (JSON) | data you get back (HTML or JSON) |

**HTTPS** is HTTP wrapped in encryption (TLS): nobody on the network can read or change it, and the browser checks it is talking to the right server. Our UI labs use plain `http://localhost:8000` to keep things simple; the Django lab's Lab 4 explains certificates in depth, and Phase 7 returns to HTTPS.

#### 1.2.C HTTP methods

| Method | Meaning | In our application |
|---|---|---|
| **GET** | Read | List books, open a book |
| **POST** | Create / perform an action | Add a book, sign in, register, sign out |
| **PUT** | Replace a whole item | *Not offered* — answers `405` |
| **PATCH** | Change *part* of an item | Edit a book |
| **DELETE** | Remove | Delete a book |

*Safe* methods (GET) only read; *unsafe* ones change data — and our server demands a CSRF token for those.

#### 1.2.D Status codes

| Code | Meaning | When you see it here |
|---|---|---|
| **200** OK | Success, with a body | list, login |
| **201** Created | Something new was stored | register, add book |
| **204** No Content | Success, nothing to return | delete, sign out |
| **302** Found | Redirect | `/` → `/books/` |
| **400** Bad Request | Invalid input | title missing |
| **401** Unauthorized | "Who are you?" (not signed in) | `/api/me/` without login |
| **403** Forbidden | "I know you, but no" / CSRF failed | editing someone else's book |
| **404** Not Found | No such thing | `/api/books/99999/` |
| **405** Method Not Allowed | Method not offered | `PUT` on a book |

*Groups:* 2xx success · 3xx redirect · 4xx *the client did something wrong* · 5xx *the server failed* (a 5xx is always worth a bug report).

#### 1.2.E HTML, CSS, DOM and JavaScript

| Technology | Job | Example from `login.html` |
|---|---|---|
| **HTML** | Structure and meaning | `<label for="username">Username</label> <input id="username" name="username">` |
| **CSS** | Looks | `.field-error { color: #b3261e; }` |
| **JavaScript** | Behaviour | the script that sends the sign-in request and shows errors |
| **DOM** | The browser's *live, in-memory tree* of the page that JavaScript can change | `<input id="username">` is a node you can find, read and change |

```text
html
├── head   (title, link to styles.css)
└── body
    ├── header ── a.brand "Book Library"
    └── main
        ├── h1 "Sign in"
        ├── form#login-form
        │   ├── label[for=username]  +  input#username
        │   ├── label[for=password]  +  input#password
        │   └── button "Sign in"
        └── p ── a "Create an account"
```

**Elements can exist but be invisible.** The error text `<p id="form-error" role="alert" hidden>` is in the DOM from the start; the `hidden` attribute keeps it invisible until JavaScript fills it. *Exists in the DOM* and *visible to the user* are different things — the source of countless automation bugs.

#### 1.2.F How a browser renders a page

1. **Request** the URL → the server sends HTML.
2. **Parse** the HTML into the **DOM** tree.
3. **Load** linked files (`styles.css`, `app.js`).
4. **Apply CSS** → work out how each element looks.
5. **Run JavaScript** — which may call the API and **change the DOM** (our Books page fills its table this way).
6. **Layout and paint** the pixels you see.

> **Why a QA engineer cares.** Automation must wait for step 5: the Books page arrives *without* rows; the rows appear a moment later. Phase 3 teaches Playwright's *auto-waiting*, which exists exactly because of this.

### 🛠️ Steps

**Step 1 (🧭) — See what the browser receives.** In Terminal B:

```powershell
curl.exe -i http://localhost:8000/login/
```

Find the **status line**, the **`Content-Type` header**, and the **HTML body**. This is the *entire* response — the browser does everything else.

**Step 2 (🧭) — View Source vs the live DOM.** Sign in (create an account at `/register/` first — Lab 1.3 shows how), open <http://localhost:8000/books/>, then:

1. Press **Ctrl+U** (*View page source*). Find `<tbody id="book-rows">`. It is **empty**.
2. Press **F12** → **Elements** tab. Expand the same `<tbody>`. It now contains `<tr>` rows (once you have added a book).

The rows were created by JavaScript *after* the page loaded. **View Source shows what the server sent; Elements shows the live DOM.** Automation tools see the live DOM.

**Step 3 (🧭) — Talk to the API directly.**

```powershell
curl.exe -i http://localhost:8000/api/books/
curl.exe -i http://localhost:8000/api/books/99999/
curl.exe -i http://localhost:8000/api/me/
curl.exe -i -X POST http://localhost:8000/api/health/
```

Match each response to the status-code table above.

### 👀 Expected results

| Command | Status | Body (start) |
|---|---|---|
| `GET /api/books/` | `200 OK` | a JSON array `[...]` (maybe empty `[]`) |
| `GET /api/books/99999/` | `404 Not Found` | `{"detail":"No Book matches the given query."}` |
| `GET /api/me/` | `401 Unauthorized` + `WWW-Authenticate: Session` | `{"detail":"Authentication credentials were not provided."}` |
| `POST /api/health/` | `405 Method Not Allowed` + `Allow: GET, OPTIONS` | `{"detail":"Method \"POST\" not allowed."}` |

### 🚑 Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `curl: (7) Failed to connect` | Server not running | Start Terminal A (`python manage.py runserver`) |
| `Invoke-WebRequest : Cannot bind parameter…` | You typed `curl` instead of `curl.exe` | Use `curl.exe` |
| View Source shows JSON, not a page | You opened `/api/books/` instead of the page | Open `/books/` (the page), not `/api/books/` |
| Elements panel shows no rows | You are not signed in, or no books exist yet | Sign in and add a book (Lab 1.3) |

### ✍️ Practice exercise (student independent)

1. Which side — frontend or backend — decides whether a book **title of 201 characters** is acceptable? Which side *also* prevents typing it? Why have both?
2. `GET /api/me/` returned `401`. Which part of the HTTP *response* tells you what kind of login the server expects?
3. A colleague says: "The error message `<p id="form-error">` is in the page, so the login failed." Explain what is wrong.

<details><summary>Answer</summary>

1. The **backend** decides (it answers `400`). The **frontend** also stops typing (`maxlength`) as a convenience. Both exist because the browser cannot be trusted — the server must always defend itself.
2. The **`WWW-Authenticate: Session`** response header.
3. The element is in the DOM from the start but **hidden**. It only matters when it is **visible and contains text**.
</details>

### ✅ Completion checklist

- [ ] I can draw browser ⇄ server ⇄ database and say what runs where.
- [ ] I can read a request and response and name method, path, headers, body and status.
- [ ] I know what 200, 201, 204, 302, 400, 401, 403, 404 and 405 mean.
- [ ] I proved to myself that View Source and the live DOM differ on `/books/`.
- [ ] I can explain "exists in the DOM" vs "visible".


---

## Lab 1.3 — Explore the application ✍️ (guided tour)

### 🎯 Learning objectives

* Explore a feature **manually before** thinking about automation.
* Identify the pages, features, states and business rules of an application.
* Record what you find in a **feature inventory**, including what is *not* available.

### Prerequisites

Lab 1.0 (app running at <http://localhost:8000>), Lab 1.2.

### 📖 Concepts

**Exploratory testing.** Using the product with curiosity, watching carefully, asking *"what if…?"* and writing down what you learn. It is the very first step of every automation task: *you cannot automate behaviour you do not understand.*

**Business rule.** A statement about how the application *must* behave ("only the owner may delete a book"). Tests exist to check rules; so finding the rules is the real goal of exploring.

**Testable state.** A condition the app can be in: signed out, signed in, empty list, list with results, dialog open, form with errors. Tests move the app into a state, act, and check the new state.

### 📁 Files

You create `docs/labs/phase-1/feature-inventory.md` (template below). No code changes.

```powershell
mkdir docs\labs\phase-1 -Force
```

### 🛠️ Steps

Pages in the application:

| URL | Page | Signed in required? |
|---|---|---|
| `/login/` | Sign in | No |
| `/register/` | Create an account | No |
| `/books/` | Book list (search, sort, add, edit, delete) | **Yes** |
| `/books/new/` | Add book form | **Yes** |
| `/books/{id}/` | Book details | **Yes** |
| `/books/{id}/edit/` | Edit book form | **Yes** |

Work through the tour in **Chrome or Edge**. For each item, **predict** the result first, then observe, then write down any surprise.

| # | Do this | Look for |
|---|---|---|
| T1 | Open `/register/`. Look at the **Create account** button. Type only a username. Then also a password. | Is the button enabled or disabled at each moment? |
| T2 | Register with password `12345678`. | Which message appears, and where? |
| T3 | Register with a name you choose (e.g. `student_anna`) and password `S3cure-Lab-Passw0rd!`. | Where are you sent? Is there a message? |
| T4 | On Sign in, click **Sign in** with both boxes empty. Then type a wrong password. Then a name that does not exist. | Which messages? Are the last two identical? |
| T5 | Sign in correctly. | The URL, the heading, the text in the top bar |
| T6 | Click **Add book**, then **Save book** with nothing typed. Then try year `abc`, then year `99`, then a valid book (year 1965). | Messages per field; what happens to the page after a valid save |
| T7 | Click the book title. | Which details are shown? Which buttons exist? |
| T8 | Click **Edit book**, change the title, save. | Is the old value pre-filled? Message after saving? |
| T9 | Back on the list: search for part of the title; then for the author; then for `zzz`. Change **Sort by**. | Result counts, the empty-state text, the order |
| T10 | Click **Delete** on a book. Press **Cancel**. Delete again and confirm. | Dialog title and text; messages; is the row gone? |
| T11 | **Ownership.** Open a **private/Incognito window**, register a second user, sign in. Open the first user's book (list and details page). | Do **Edit** and **Delete** appear? Now type `/books/<id>/edit/` of that book into the address bar and try to save a change. |
| T12 | **Sign out**. Press the browser **Back** button. Then open `/books/new/` directly. | Where do you land each time? After signing in again, where do you end up? |
| T13 | While signed in, press **F5** on the list. | Still signed in? |
| T14 | Watch a notification (e.g. after adding a book) for several seconds. | Does it stay forever? |

Now create `docs/labs/phase-1/feature-inventory.md` with this structure and fill it **from your own observations**:

```markdown
# Feature inventory — Book Library

## Pages
| URL | Purpose | Needs sign-in | Notes |

## Features
| ID | Feature | Page | How to trigger | Observed result |
| F-01 | Register | /register/ | ... | ... |

## Business rules I found
| ID | Rule | Evidence (what I did / saw) |

## States I saw
(e.g. signed out, signed in, empty search result, dialog open, form with errors)

## Not available / out of scope
(categories? pagination? ...)

## Questions and surprises
```

### 👀 Expected results (check your inventory against this)

<details><summary>Business rules the tour should reveal</summary>

| # | Rule |
|---|---|
| R1 | Protected pages send a signed-out visitor to `/login/?next=<page>`; after signing in the user returns to that page |
| R2 | **Create account** stays disabled until *both* username and password have text |
| R3 | Usernames are unique, ignoring capital letters; passwords must pass server rules (minimum length 8, not entirely numeric, not too common, not too similar to the username) |
| R4 | Sign-in errors: empty fields → "Username is required." / "Password is required."; wrong password **and** unknown user → the same "Invalid username or password." |
| R5 | A book needs a **title** (max 200) and an **author** (max 120); the year is optional, a whole number, valid range **1000–2100** |
| R6 | Messages: "Title is required.", "Author is required.", "Year must be a whole number." (browser side), "Year must be between 1000 and 2100." (server side) |
| R7 | After a successful add/edit/delete the list shows "Book added." / "Book updated." / "Book deleted."; these notifications disappear after about 4 seconds |
| R8 | Deleting asks first, in a dialog titled **Delete book?**, naming the book; **Cancel** keeps it |
| R9 | Search matches **title or author**, ignores capitals, matches part of a word; no match → `No books match “…”.`; the count reads "1 book" / "N books" |
| R10 | Sort options: Recently added (default), Title A–Z, Title Z–A, Year oldest first, Year newest first |
| R11 | Everyone signed in sees **all** books (shared catalogue), but only the **owner** sees Edit/Delete — and the server refuses changes by others: "You do not have permission to change this book." |
| R12 | Refreshing keeps you signed in; **Sign out** ends the session ("You have been signed out.") and protected pages are closed again |
</details>

<details><summary>Features that do not exist</summary>

Categories and category filter, ISBN and description, pagination, password reset, admin pages. Record these as **"not available — not tested"**, never as failures.
</details>

### 🚑 Common errors

| Symptom | Cause | Fix |
|---|---|---|
| The notification vanished before I could read it | It disappears after ~4 s | Repeat the action and read it immediately (and note: automation must be quick or wait for it correctly — Phase 3) |
| Edit/Delete buttons never appear | You are looking at someone else's book | They appear only for books **you** added |
| Everything redirects to Sign in | Session ended (signed out, or different browser window) | Sign in again |
| Second user logged out the first | You used the same browser profile | Use a **private window** — separate cookies |

### ✍️ Practice exercise (student independent)

Explore these **extra "what if" questions** and add the answers to *Questions and surprises*:

1. What happens if you add a book whose title contains `<b>bold</b>`? Is it shown as text or as bold formatting? Why does it matter?
2. What happens if you put spaces only in the title?
3. What if you open `/books/999999/` or `/books/abc/`?
4. Add 3 books with the same title. Is that allowed? Does the requirement say it should be?

<details><summary>Answer</summary>

1. Shown **as plain text** (tags are not interpreted) — good: this protects against script injection (XSS). 2. "Title is required." (spaces are trimmed). 3. `/books/999999/` → "Book not found."; `/books/abc/` → a plain 404 page (no such URL). 4. Allowed — nothing forbids duplicates. A tester *asks the product owner* instead of assuming it is a bug, and records the question.
</details>

### ✅ Completion checklist

- [ ] I completed T1–T14 and the four extra questions.
- [ ] `feature-inventory.md` lists pages, features, rules (at least 10), states, unavailable features and questions.
- [ ] I compared my rules with the answer block and added any I missed.
- [ ] I tested the ownership rule with **two** users.

---

## Lab 1.4 — Write manual test scenarios 🧭 + ✍️

### 🎯 Learning objectives

* Turn the feature inventory into scenarios and then into complete test cases.
* Classify each by type, priority and the best test layer (UI, API or both).
* Decide what is worth automating.

### Prerequisites

Lab 1.3 (your inventory).

### 📖 Concepts

**Traceability.** Every test should be able to say *which rule it protects*. Link scenarios to your rules (R1…R12): then, when a rule changes, you know exactly which tests to update, and you can see which rules have **no** test.

**Priority.** You cannot automate everything first. Rank by *business impact × likelihood of breaking*:

| Priority | Meaning | Suite |
|---|---|---|
| **Smoke** | If this fails, nothing else is worth testing | Run on every change (minutes) |
| **Regression** | Important behaviour that must keep working | Run nightly / before release |
| **Low** | Rare or cosmetic | Maybe manual |

**Best layer.** A rule enforced by the **server** (validation, permissions) is best checked at the **API** — fast and precise. A rule about **what the user sees and does** (messages, dialogs, redirects) needs the **UI**. Some need both. We come back to this in Phase 6.

### 📁 Files

`docs/labs/phase-1/manual-test-scenarios.md` (you create it).

### 🛠️ Steps

**Step 1 (🧭) — The starting list.** These scenarios are the minimum for this course. IDs stay the same through all later phases.

| ID | Scenario | Expected result | Type | Priority | Layer |
|---|---|---|---|---|---|
| AUTH-01 | Open the login page | Login form is displayed | + | Smoke | UI |
| AUTH-02 | Sign in with valid credentials | User reaches the book list | + | **Smoke** | UI (+API) |
| AUTH-03 | Sign in with an incorrect password | Rejected; "Invalid username or password." | − | Regression | UI + API |
| AUTH-04 | Submit the sign-in form with empty fields | Required-field messages shown | − | Regression | UI |
| AUTH-05 | Sign out | Signed out; protected content closed | + | **Smoke** | UI + API |
| AUTH-06 | Open a protected page while signed out | Redirected to sign in | − | Regression | UI |
| AUTH-07 | Refresh while signed in | Still signed in | + | Regression | UI |
| BOOK-01 | Open the book list | List and controls displayed | + | **Smoke** | UI |
| BOOK-02 | Add a book with valid data | Saved; appears in the list | + | **Smoke** | UI + API |
| BOOK-03 | Submit the book form with required fields missing | Messages shown; nothing saved | − | Regression | UI + API |
| BOOK-04 | Open a book's details | Correct information shown | + | Regression | UI |
| BOOK-05 | Edit an existing book | New values saved and shown | + | Regression | UI + API |
| BOOK-06 | Cancel the delete confirmation | Book remains | − | Regression | UI |
| BOOK-07 | Confirm deletion | Book removed | + | **Smoke** | UI + API |
| BOOK-08 | Search for an existing title | Matching book shown | + | Regression | UI + API |
| BOOK-09 | Search for something with no match | "No books match…" message | − | Regression | UI |
| BOOK-10 | Search by author | Matching books shown | + | Regression | UI + API |
| BOOK-11 | Sort the list | Order follows the chosen option | + | Regression | UI + API |

(+ positive, − negative.)

**Step 2 (🧭) — The test-case template.** Each case in `manual-test-scenarios.md` uses this shape:

| Field | Meaning |
|---|---|
| **ID / Title** | `AUTH-03` — Sign in with incorrect password |
| **Rule(s)** | `R4` (links back to your inventory) |
| **Preconditions** | The state before you start |
| **Test data** | Exact values |
| **Steps** | Numbered, one action each |
| **Expected result** | Specific and *observable* |
| **Type / Priority / Layer** | From the table above |

**Step 3 (🧭) — Four worked examples.**

**AUTH-03 — Sign in with an incorrect password**

| | |
|---|---|
| Rule | R4 |
| Preconditions | Signed out. A user `qa_anna` exists with password `S3cure-Lab-Passw0rd!` |
| Test data | username `qa_anna`; password `wrong-password-1` |
| Steps | 1. Open `/login/`. 2. Type the username. 3. Type the wrong password. 4. Click **Sign in**. |
| Expected | A visible message **"Invalid username or password."**; the page is still the Sign in page; no "Signed in as…" text anywhere |
| Type / Priority / Layer | Negative · Regression · UI + API (API: `POST /api/login/` → `401`) |

**BOOK-03 — Required fields missing**

| | |
|---|---|
| Rules | R5, R6 |
| Preconditions | Signed in |
| Test data | none (all fields empty) |
| Steps | 1. Click **Add book**. 2. Click **Save book** without typing. |
| Expected | **"Title is required."** and **"Author is required."** appear; the URL is still `/books/new/`; no new book in the list |
| Type / Priority / Layer | Negative · Regression · UI (browser-side check) + API (`POST /api/books/` without title → `400 {"title":["This field is required."]}`) |

**BOOK-07 — Confirm deletion**

| | |
|---|---|
| Rules | R7, R8 |
| Preconditions | Signed in; this user owns a book titled `Dune <random>` |
| Steps | 1. Open the list. 2. Click **Delete** on that book. 3. Check the dialog. 4. Click **Delete** in the dialog. |
| Expected | Dialog titled **Delete book?** names the book; afterwards "Book deleted." appears, the row is gone, and `GET /api/books/<id>/` returns `404` |
| Type / Priority / Layer | Positive · **Smoke** · UI + API |

**BOOK-09 — Search with no match**

| | |
|---|---|
| Rule | R9 |
| Preconditions | Signed in |
| Test data | search text `no-such-book-8f3a` |
| Steps | 1. Open the list. 2. Type the text in **Search books**. |
| Expected | Text `No books match “no-such-book-8f3a”.` is visible; the table shows no rows |
| Type / Priority / Layer | Negative · Regression · UI |

> Notice what the good cases have in common: the **data is exact**, each **step is one action**, and the **expected result can be checked with your eyes** (or a status code) — nothing like "works correctly".

### 👀 Expected results

A file `manual-test-scenarios.md` that contains: the 18-row scenario table, full test cases for the four worked examples (copied or rewritten), and your own cases from the practice exercise.

### 🚑 Common errors

| Mistake | Fix |
|---|---|
| Steps like "test the login" | One action per step: "Type the username `qa_anna`." |
| Expected result "it works" | Name the exact message, URL, or status code |
| Test data "any password" | Fixed, documented values (or "unique random name") |
| Depending on data from a previous test | State the **precondition** and create the data yourself |
| No link to a rule | Add the rule ID (R1–R12) to every case |

### ✍️ Practice exercise (student independent)

1. Write **full test cases** (all fields) for **AUTH-02, AUTH-04, BOOK-02 and BOOK-08**.
2. Add **six more scenarios** that are not in the list: at least two boundary, two negative and one ownership scenario.
3. For each of your 22+ scenarios mark **Smoke / Regression** and **UI / API / both**, then answer: *which scenarios would you automate first, and why?*

<details><summary>Answer (example extra scenarios and thinking)</summary>

| ID | Scenario | Expected | Type | Layer |
|---|---|---|---|---|
| BOOK-12 | Year **1000** (lowest valid) | Saved | Boundary + | UI + API |
| BOOK-13 | Year **999** | "Year must be between 1000 and 2100." | Boundary − | API first, UI check once |
| BOOK-14 | Year **2101** | Same message | Boundary − | API |
| BOOK-15 | Year `abc` | "Year must be a whole number."; nothing sent | − | UI |
| AUTH-08 | Register with an existing name in different capitals | "A user with that username already exists." | − | UI + API |
| BOOK-16 | Another user opens my book | No Edit/Delete; server answers `403` to a forced change | Authorization | UI + API |

*Automate first:* the **Smoke** set (AUTH-02, AUTH-05, BOOK-01, BOOK-02, BOOK-07) — cheap to run, covers the core journey. Then the **negative** and **ownership** cases, because these are the rules most likely to be broken by a careless change. *Boundary* values are best at the **API** (fast, many values); one UI check is enough to prove the message is displayed.
</details>

### ✅ Completion checklist

- [ ] `manual-test-scenarios.md` contains all 18 starter scenarios with type, priority and layer.
- [ ] I wrote full test cases for AUTH-02, AUTH-04, BOOK-02, BOOK-08.
- [ ] I added six of my own scenarios (≥2 boundary, ≥2 negative, ≥1 ownership).
- [ ] Every case points to a rule ID from my inventory.
- [ ] I can explain why some checks belong at the API rather than the UI.

---

## Lab 1.5 — Inspect elements with DevTools; selectors 🧭 + ✍️ + 🏆

### 🎯 Learning objectives

* Open and use the **Elements** and **Console** panels.
* Identify an element's **id, class, attributes, role and text**.
* Write simple **CSS selectors** and **XPath** expressions and test them in the Console.
* Judge whether a selector is reliable or fragile.

### Prerequisites

Labs 1.2 and 1.3.

### 📖 Concepts

#### 1.5.A Browser DevTools

Press **F12** (or **Ctrl+Shift+I**, or right-click → **Inspect**). Panels you will use:

| Panel | Use |
|---|---|
| **Elements** | The live DOM and the CSS applied to each element |
| **Console** | Type JavaScript; test selectors; see errors |
| **Network** | Every request and response (Lab 1.6) |
| **Application** | Cookies and storage (Lab 1.6) |

Shortcut: **Ctrl+Shift+C** = *inspect mode*; click any element on the page to jump to it in the Elements panel.

#### 1.5.B What identifies an element

| Property | What it is | Reliability for tests |
|---|---|---|
| **Tag** | `input`, `button`, `a` … | Weak alone — many share a tag |
| **`id`** | Should be unique on the page | Good *if* developers keep it; may be auto-generated |
| **`class`** | Styling names, e.g. `btn-primary` | **Fragile** — designers change them |
| **Attributes** | `name`, `type`, `placeholder`, `href`, `data-testid` | `data-testid` is made *for* tests; others vary |
| **Text** | What the user reads: "Sign in" | Good — it is what the user sees (but changes with wording or language) |
| **Role + accessible name** | What assistive technology (and Playwright) sees: *button named "Sign in"* | **Best** — describes meaning, survives restyling |

**Accessible name** comes from a visible label (`<label for="username">`), the element's text, or an `aria-label`. Our Books table gives each row's buttons names such as **"Delete Dune"** — the *visible* text is just "Delete", but the *accessible* name is longer so that several Delete buttons can be told apart.

#### 1.5.C CSS selectors (the basics)

| Selector | Meaning | Example |
|---|---|---|
| `tag` | by tag name | `button` |
| `#id` | by id | `#username` |
| `.class` | by class | `.field-error` |
| `[attr="value"]` | by attribute | `[type="password"]`, `[data-testid="book-row"]` |
| `A B` | B anywhere **inside** A | `form button` |
| `A > B` | B a **direct child** of A | `dl > dt` |
| `A + B` | B **right after** A | `dt + dd` |
| `:nth-child(n)` | by position — avoid when possible | `tr:nth-child(2)` |

#### 1.5.D XPath (basics — a last resort)

| XPath | Meaning |
|---|---|
| `//button` | any button anywhere |
| `//input[@id="username"]` | input with that id |
| `//button[text()="Sign in"]` | button whose text is exactly *Sign in* |
| `//label[text()="Password"]/following-sibling::input` | the input after a label |
| `//tr[.//a[text()="Dune"]]//button` | the button inside the row that contains the link "Dune" |

XPath can walk **up** and sideways, which CSS cannot — but it is harder to read and break-prone. Playwright's recommended locators (Phase 3) are better.

### 📁 Files

`docs/labs/phase-1/locator-notes.md` (you create it).

### 🛠️ Steps

**Step 1 (🧭) — Inspect the Username box.** Open `/login/`, press **Ctrl+Shift+C**, click the Username box. In the Elements panel you should see:

```html
<input id="username" name="username" autocomplete="username">
```

Note: tag `input`, id `username`, name `username`. Click the label text "Username" and note `for="username"`: the label points at the id — that is how the *accessible name* "Username" is built.

**Step 2 (✍️) — Complete the element table for the Sign in page.** Inspect each element and fill the blank cells:

| Element | Tag | id | Other attributes | Role | Accessible name / text |
|---|---|---|---|---|---|
| Brand link (top bar) | | | | | |
| Page heading | | | | | |
| Username box | | | | | |
| Password box | | | | | |
| Sign in button | | | | | |
| Error banner `form-error` | | | | | |
| "Create an account" link | | | | | |

<details><summary>Answer</summary>

| Element | Tag | id | Other attributes | Role | Accessible name / text |
|---|---|---|---|---|---|
| Brand link | `a` | — | `class="brand"` `href="/books/"` | link | "Book Library" |
| Page heading | `h1` | — | — | heading (level 1) | "Sign in" |
| Username box | `input` | `username` | `name="username"` `autocomplete="username"` | textbox | "Username" (from the label) |
| Password box | `input` | `password` | `type="password"` `autocomplete="current-password"` | textbox | "Password" |
| Sign in button | `button` | — | `type="submit"` | button | "Sign in" |
| Error banner | `p` | `form-error` | `class="form-error"` `role="alert"` `hidden` | alert (only when visible) | the error text |
| Create account link | `a` | — | `href="/register/"` | link | "Create an account" |
</details>

**Step 3 (🧭) — See the page the way a test sees it.** Playwright will later describe a page by roles and names. Here is the Sign in page in that view (you will produce this yourself in Phase 3):

```text
- banner:
  - link "Book Library":
    - /url: /books/
- main:
  - heading "Sign in" [level=1]
  - text: Username
  - textbox "Username"
  - text: Password
  - textbox "Password"
  - button "Sign in"
  - paragraph:
    - text: No account yet?
    - link "Create an account":
      - /url: /register/
```

Notice what is **missing**: the hidden banner `form-error` and the hidden `flash` message. *Hidden elements do not appear* — they exist in the DOM but are not part of what the user (or an assistive technology) can perceive.

You can see the browser's own version: Elements panel → select an element → **Accessibility** tab (beside *Styles*).

**Step 4 (🧭) — Test selectors in the Console.** On `/login/`, open the **Console** and run each line. Predict the answer first.

```javascript
document.querySelectorAll('input').length                    // how many inputs?
document.querySelector('#username').name                     // the name attribute
document.querySelector('label[for="password"]').textContent  // the label text
document.querySelector('input[type="password"]').id          // which id?
document.querySelector('#form-error').hidden                 // hidden right now?
$$('button').length                                          // Chrome shortcut for querySelectorAll
$x('//button[text()="Sign in"]').length                      // XPath (Chrome Console only)
```

<details><summary>Answer</summary>

`2` · `"username"` · `"Password"` · `"password"` · `true` · `1` · `1`
</details>

**Step 5 (🧭) — The Books page.** Sign in, add at least one book, open `/books/` and run:

```javascript
document.querySelectorAll('[data-testid="book-row"]').length   // one per book
$$('tbody a[aria-label^="Edit"]').length                       // Edit links you may use (your own books)
document.querySelector('#sort').options.length                 // sort choices
document.querySelector('#toast').getAttribute('role')          // notification role
```

Expected: the row count equals the count text on the page; the sort list has `5` options; the toast role is `"status"`. Then inspect one table row and find `data-testid="book-row"`. *This attribute exists only to help tests* — table rows have no role-and-name that identifies them.

**Step 6 (✍️) — Judge the selectors.** All of these find the **Sign in** button on `/login/`. For each, say how likely it is to break when the page changes, and why.

| # | Selector | Brittleness (low / medium / high)? Why? |
|---|---|---|
| 1 | `button` | |
| 2 | `.topbar + main button` | |
| 3 | `main > form > div:nth-child(5) > button` | |
| 4 | `button[type="submit"]` | |
| 5 | `//button[text()="Sign in"]` | |
| 6 | *role = button, name = "Sign in"* | |

<details><summary>Answer</summary>

1. **High** — breaks the moment a second button is added. 2. **High** — depends on page layout. 3. **Very high** — depends on exact position. 4. **Medium** — breaks if another submit button appears. 5. **Medium** — depends on exact wording and on XPath structure. 6. **Low** — describes *what it is for the user*; survives re-styling and re-ordering (changes only if the visible name changes — which is a *real* change worth failing for). This is why Phase 3 teaches `getByRole()` first.
</details>

**Step 7 (✍️) — Write `locator-notes.md`.** For the Sign in page and the Books page list every important element with: its best locator idea (role+name / label / text / test id), and why it is reliable. Include the *exists vs visible* note for hidden elements.

### 👀 Expected results

* Steps 4 and 5 produce the answers shown.
* `locator-notes.md` has an entry for at least: username, password, Sign in button, error message, search box, sort list, Add book link, a book row, a row's Delete button, the delete dialog, the notification.

### 🚑 Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `$x is not defined` / `$$ is not defined` | You are not in Chrome/Edge's Console | Use `document.querySelectorAll(...)` instead |
| `document.querySelector(...)` returns `null` | Wrong page, not signed in, or the element is created later by JavaScript | Check the URL, sign in, wait a second and retry |
| `Copy → Copy selector` gives something like `body > main > div:nth-child(2) > …` | DevTools builds position-based selectors | Do not use them as-is — write a meaningful one |
| You cannot find the toast | It disappears after ~4 s | Trigger the action again; or in the Console type `document.querySelector('#toast')` right away |
| Row selector finds 0 | List is empty or still loading | Add a book; reload and retry |

### ✍️ Practice exercise (student independent)

1. List **three things that can differ** between *"an element exists in the DOM"* and *"a user can see it"*.
2. The Delete button of a row has visible text **Delete** but accessible name **Delete Dune**. Why was it designed that way, and what would go wrong with a locator that searched for the name "Delete" on a page showing five books?
3. Open the **Add book** page. Which labelled form fields exist? Write the best locator idea for each.

<details><summary>Answer</summary>

1. Examples: the `hidden` attribute; CSS `display:none`; an element covered by a dialog; an element scrolled out of view; zero size.
2. Several rows need *different* names so a screen-reader user (and a test) can tell which book a button affects. A locator for plain "Delete" would match **five** buttons — ambiguous. You scope it to the row or use the full name.
3. **Title** (`label "Title"`), **Author**, **Published year**; buttons **Save book** and link **Cancel**. Best idea: by *label* (`getByLabel`-style) for fields, by *role + name* for the button/link.
</details>

### 🏆 Optional challenge

Write (a) a CSS selector and (b) an XPath expression that find **the Delete button of the row whose title is "Dune"**, and test both in the Console. Which is shorter? Which survives a change to the table's column order?

<details><summary>Answer (one possible solution)</summary>

CSS: `button[aria-label="Delete Dune"]` (short, and independent of column order — it relies on the accessible name).
XPath: `//tr[.//a[text()="Dune"]]//button` (finds the row containing the link "Dune", then any button inside it — also independent of column order). Both work as long as the title text stays.
</details>

### ✅ Completion checklist

- [ ] I can open DevTools, use inspect mode, and read the DOM.
- [ ] I can find id, class, attributes, role, accessible name and text of an element.
- [ ] I ran the Console exercises and got the expected answers.
- [ ] I can write simple CSS and XPath selectors and explain why most are fragile.
- [ ] `locator-notes.md` is complete.

---

## Lab 1.6 — How UI actions talk to the API 🧭 + ✍️

### 🎯 Learning objectives

* Use the **Network** and **Application** panels to watch requests and cookies.
* Map each UI action to its API requests.
* Reproduce one UI action with `curl.exe`.

### Prerequisites

Labs 1.2, 1.3, 1.5.

### 📖 Concepts

When you click **Sign in**, the page does not "log you in" by magic: JavaScript sends **HTTP requests** to the API and reacts to the answers. *Every UI test therefore also tests the API*, and many checks are faster and more precise when made at the API (Phase 6).

Our JavaScript follows a fixed pattern for anything that changes data:

1. `GET /api/csrf/` — ask for a **CSRF token** (a secret the server will demand).
2. `POST` / `PATCH` / `DELETE` — send the change, adding the token in the `X-CSRFToken` header. The browser adds the cookies and the `Origin` header by itself.
3. Show a message or move to another page based on the status code.

> **Why a QA engineer cares.** When a UI test fails, the Network tab tells you in seconds whether the *page* failed (no request sent, wrong message) or the *server* failed (error status). That decides who gets the bug.

### 📁 Files

`docs/labs/phase-1/ui-api-map.md` (you create it).

### 🛠️ Steps

**Step 1 (🧭) — Prepare the panel.** Open `/login/`, press **F12** → **Network**. Tick **Preserve log**. Choose the filter **Fetch/XHR**. Click the 🚫 button to clear the list.

**Step 2 (🧭) — Sign in and watch.** Sign in correctly. You should see these requests, in this order:

| # | Request | Status |
|---|---|---|
| 1 | `GET /api/csrf/` | 200 |
| 2 | `POST /api/login/` | 200 |
| 3 | `GET /api/me/` | 200 |
| 4 | `GET /api/books/?ordering=-id` | 200 |

(#3 and #4 happen on the *next* page, which asks "who am I?" and then loads the books.) Clear the filter to **All** and you will also see the page itself (`books/`), `app.js` and `styles.css`.

**Step 3 (🧭) — Dissect the login request.** Click `login` and look through the sub-tabs:

| Sub-tab | What to find |
|---|---|
| **Headers → General** | Request URL `http://localhost:8000/api/login/`, method `POST`, status `200 OK` |
| **Request Headers** | `Content-Type: application/json` · `X-CSRFToken: …` · `Origin: http://localhost:8000` · `Cookie: csrftoken=…` |
| **Payload** | `{"username":"…","password":"…"}` — visible to *you* in DevTools |
| **Response** | `{"id":…,"username":"…"}` — and **no password** |
| **Response Headers** | `Set-Cookie: sessionid=…; HttpOnly; Path=/; SameSite=Lax; Secure` and a new `Set-Cookie: csrftoken=…` |

Then open **Application → Cookies → `http://localhost:8000`**. You should see **`sessionid`** (HttpOnly ✔) and **`csrftoken`** (HttpOnly not ticked). The server created a *session*; the cookie is just its random id. **The browser sends it back automatically** on every later request — that is how you stay signed in.

**Step 4 (✍️) — Build the UI → API map.** Perform each action with the Network panel open and write down the requests (method, URL, status):

| UI action | Requests you observe |
|---|---|
| Open `/books/` (signed in) | |
| Type in the search box | |
| Change **Sort by** | |
| Save a new book | |
| Save an edit | |
| Confirm a delete | |
| Click **Sign out** | |
| Register a new user | |
| Sign in with a **wrong** password | |

<details><summary>Answer</summary>

| UI action | Requests |
|---|---|
| Open `/books/` | `GET /books/` (HTML) · `GET /ui/styles.css` · `GET /ui/app.js` · `GET /api/me/` → 200 · `GET /api/books/?ordering=-id` → 200 |
| Type in search | (after ~¼ s pause) `GET /api/books/?ordering=-id&search=…` → 200 |
| Change sort | `GET /api/books/?ordering=title` (or the chosen value) → 200 |
| Save new book | `GET /api/csrf/` → 200, then `POST /api/books/` → **201** |
| Save an edit | `GET /api/csrf/`, then `PATCH /api/books/{id}/` → **200** |
| Confirm delete | `GET /api/csrf/`, then `DELETE /api/books/{id}/` → **204** |
| Sign out | `GET /api/csrf/`, then `POST /api/logout/` → **204** |
| Register | `GET /api/csrf/`, then `POST /api/register/` → **201** |
| Wrong password | `GET /api/csrf/`, then `POST /api/login/` → **401** — and **no `sessionid` cookie** appears |

Observe: typing in the search box sends *nothing* until you pause (a debounce) — one request, not one per letter. A UI test must be written with that in mind.
</details>

**Step 5 (🧭) — Reproduce one action with `curl.exe`** (Terminal B, project root). Replace `YOUR_NAME` and `YOUR_PASSWORD` with the account you registered.

```powershell
$BASE = "http://127.0.0.1:8000"
$JAR  = "scratch\jar-phase1.txt"
mkdir scratch -ErrorAction SilentlyContinue
Remove-Item $JAR -ErrorAction SilentlyContinue
function Get-Csrf { (curl.exe -s -c $JAR -b $JAR "$BASE/api/csrf/" | ConvertFrom-Json).csrfToken }

Set-Content -Path scratch\login-phase1.json -Encoding ascii -Value '{"username":"YOUR_NAME","password":"YOUR_PASSWORD"}'
Set-Content -Path scratch\book-phase1.json  -Encoding ascii -Value '{"title":"Made with curl","author":"Me","published_year":2024}'

# 1) sign in (token first!)
$T = Get-Csrf
curl.exe -i -c $JAR -b $JAR -H "Content-Type: application/json" -H "X-CSRFToken: $T" --data "@scratch/login-phase1.json" "$BASE/api/login/"

# 2) who am I?
curl.exe -b $JAR "$BASE/api/me/"

# 3) search, the way the page does
curl.exe -b $JAR "$BASE/api/books/?search=curl&ordering=title"

# 4) add a book WITHOUT the token -> expect 403
curl.exe -i -c $JAR -b $JAR -H "Content-Type: application/json" --data "@scratch/book-phase1.json" "$BASE/api/books/"

# 5) add it WITH a fresh token -> expect 201
$T = Get-Csrf
curl.exe -i -c $JAR -b $JAR -H "Content-Type: application/json" -H "X-CSRFToken: $T" --data "@scratch/book-phase1.json" "$BASE/api/books/"
```

Then reload `/books/` in the browser: "Made with curl" is in the list, owned by *you*. **The browser and `curl.exe` use the very same API.**

### 👀 Expected results

* Step 2: four API requests as tabulated, all `200`.
* Step 3: the `Set-Cookie` lines described, including `HttpOnly`.
* Step 5: (1) `200 {"id":…,"username":"…"}` with two `Set-Cookie` headers; (2) `{"id":…,"username":"…"}`; (3) a JSON array; (4) `403` with `{"detail":"CSRF Failed: CSRF token missing."}`; (5) `201` with the new book as JSON.

### 🚑 Common errors

| Symptom | Cause | Fix |
|---|---|---|
| Network tab is empty | The filter or *Preserve log* is wrong, or you cleared it | Untick filters; reload and repeat the action |
| `login` request is missing after Sign in | The page redirected and the log was cleared | Tick **Preserve log** *before* signing in |
| `curl.exe`: `401` on `/api/me/` after login | Cookie jar flags missing | Use `-c $JAR -b $JAR` on the login call |
| `403 CSRF token incorrect` | You used an old token (login **rotates** it) | Call `$T = Get-Csrf` again right before each unsafe request |
| `400 JSON parse error` | JSON file has a hidden marker | Create it with `-Encoding ascii` |
| `Get-Csrf` returns nothing | Server not running or wrong `$BASE` | Check Terminal A; open `$BASE/api/health/` |

### ✍️ Practice exercise (student independent)

1. Sign in with a **wrong** password with the Network panel open. Which request fails, with which status, and what does the *page* do with that information?
2. From the Network evidence alone: is the message "Invalid username or password." produced by the **server** or by the **page**?
3. Which two things does the browser add to the `POST` automatically that our JavaScript never writes?
4. Name one check from your scenario list that you could make **faster and more precisely at the API than through the UI**.

<details><summary>Answer</summary>

1. `POST /api/login/` → **401**; the page reads the status and shows the banner text. 2. The **page**: the server's JSON body is `{"detail":"Invalid username or password."}`, but the *banner wording* comes from the page's JavaScript. (Both say the same thing here; in other cases wording can differ — a good reason to test both.) 3. The **`Cookie`** header and the **`Origin`** header. 4. For example BOOK-13/14 (year 999 and 2101): one API call each, in milliseconds, instead of loading a form.
</details>

### ✅ Completion checklist

- [ ] I watched `login` in the Network tab and found headers, payload, response and cookies.
- [ ] I found `sessionid` (HttpOnly) in the Application panel.
- [ ] `ui-api-map.md` lists the requests for all nine actions.
- [ ] My `curl.exe` flow ended with `201` and the book appeared in the browser.
- [ ] I can explain why a UI test also tests the API.

---

## Lab 1.7 — Phase 1 wrap-up: your Application Understanding Pack ✍️

### 🎯 Learning objectives

* Assemble and review your Phase 1 deliverables.
* Check your understanding with the knowledge check.
* Be ready to start TypeScript and Playwright with a clear plan.

### Prerequisites

Labs 1.0–1.6.

### 📁 Files — your Phase 1 deliverables

```text
docs/labs/phase-1/
├── feature-inventory.md       (Lab 1.3)  pages · features · rules R1… · states · unavailable features · questions
├── manual-test-scenarios.md   (Lab 1.4)  18 starter + your own scenarios · full test cases
├── locator-notes.md           (Lab 1.5)  important elements and the best locator idea for each
└── ui-api-map.md              (Lab 1.6)  UI action → API requests
```

### 🛠️ Steps

**Step 1 — Review each file against its checklist.**

| File | It is good when… |
|---|---|
| `feature-inventory.md` | Every page is listed; ≥10 rules; unavailable features noted; each rule has *evidence* |
| `manual-test-scenarios.md` | All scenarios have type, priority, layer; ≥4 full test cases; every case cites a rule; steps are single actions; expected results are observable |
| `locator-notes.md` | Each locator idea says *why* it is reliable; hidden elements are noted |
| `ui-api-map.md` | Method, URL and status for all nine actions |

**Step 2 — Re-run the safety net.**

```powershell
python manage.py test backend_tests
```

`Ran 54 tests … OK`.

**Step 3 — (Optional) save your work with Git.**

```powershell
git status --short
```

Make sure no `.venv`, database, `scratch` or certificate files are listed (they are in `.gitignore`). Full Git training comes in Phase 7.

**Step 4 — Take the knowledge check** (below). Aim for 12 of 15 without looking back.

### ❓ Knowledge check

1. Give one difference between manual and automated testing, and one thing that should *not* be automated.
2. What is the difference between a test scenario and a test case?
3. Name the four test types of this phase and give an example of each.
4. For a field valid from 1000 to 2100, list the boundary values to test.
5. Which side — browser or server — must always enforce a business rule, and why?
6. What does a `401` mean? A `403`? A `404`? A `405`?
7. What is the difference between `PUT` and `PATCH`?
8. What is the DOM, and how does it differ from "View Source"?
9. A `<p hidden>` error message is in the page. Is the error showing? Explain.
10. Why is `.btn-primary` a poor selector? What is a better kind?
11. What is an *accessible name*, and where does the name of the Username box come from?
12. When you click **Sign in**, which two requests are sent first, and why is the first one needed?
13. Which browser feature stores the `sessionid`, and which attribute stops JavaScript from reading it?
14. Why do boundary values often find bugs?
15. Name two scenarios you would automate first for this application, and justify your choice.

<details><summary>Answers</summary>

1. Manual: a person judges and explores; automation: a program repeats precisely. *Don't automate* a feature that changes weekly or a purely subjective judgement. 2. A scenario says *what* to check; a test case adds ID, preconditions, steps, exact data and expected result. 3. Functional (add a book), smoke (sign-in works), regression (delete still works after the edit feature was added), integration (UI-added book is stored by the API). 4. 999, 1000, 2100, 2101 (plus empty and non-numeric). 5. The **server**, because the browser is controlled by the user. 6. 401 = not signed in; 403 = signed in but not allowed (or CSRF failed); 404 = no such resource; 405 = method not offered. 7. PUT replaces the whole item; PATCH changes part. 8. The DOM is the browser's live tree of the page, which JavaScript can change; View Source is the text the server sent. 9. No — `hidden` keeps it invisible; it matters only when visible with text. 10. Class names are for styling and change often; prefer role + accessible name, label, text, or a test id. 11. The text a user (and assistive tech) gets for an element; from the `<label for="username">`. 12. `GET /api/csrf/` then `POST /api/login/`; the token is required by the server for every unsafe request. 13. The browser's cookie jar; `HttpOnly`. 14. Developers often write `<` where they needed `<=`; the edge is where such mistakes show. 15. For example AUTH-02 and BOOK-02: they are on the core user journey, quick to run, and a failure there means the product is broken.
</details>

### Glossary (Phase 1)

| Term | Meaning |
|---|---|
| **AUT** | Application under test |
| **Test scenario / test case / test data** | What to check / exactly how, with expected result / the values used |
| **Positive / negative / boundary test** | Valid input / invalid input / values at the edge of a limit |
| **Smoke / regression / integration test** | Is it alive? / did we break something? / do the parts work together? |
| **Client, server, frontend, backend** | Browser / machine answering requests / code in the browser / code on the server |
| **HTTP method, status code, header, body** | Request verb / result number / extra information / the data |
| **DOM** | The browser's live tree of a page |
| **Selector / locator** | A way to point at an element |
| **Role / accessible name** | What an element *is* / its name for users and assistive technology |
| **Session / cookie / CSRF token** | Server record of a sign-in / small value the browser stores and returns / secret that proves a write came from our page |
| **Business rule** | A statement of how the application must behave |

### ✅ Phase 1 checkpoint — do not start Phase 2 until all boxes are ticked

- [ ] **43 → 54** backend tests pass (baseline preserved, new features covered).
- [ ] The application runs at <http://localhost:8000> and I can use every page.
- [ ] All four documents in `docs/labs/phase-1/` exist and pass the review table.
- [ ] I scored at least 12/15 on the knowledge check.
- [ ] I can explain, without notes, what happens from clicking **Sign in** to seeing the book list (requests, cookie, redirect, rendering).
- [ ] I can say which of my scenarios belong at the UI, which at the API, and why.

> **Next — Phase 2: TypeScript for automation testers.** You will install Node.js tooling and learn only the TypeScript you need to read and write Playwright tests: variables, types, functions, interfaces, classes, `async`/`await`, imports and JSON data. When your checkpoint passes, say **"Phase 1 complete"** and ask for Phase 2.

---

# Appendices

## Appendix A — Quick reference

**DevTools**

| Task | Shortcut |
|---|---|
| Open DevTools | **F12** or **Ctrl+Shift+I** |
| Inspect mode | **Ctrl+Shift+C** |
| View page source | **Ctrl+U** |
| Hard reload (ignore cache) | **Ctrl+F5** |
| Private window (separate cookies) | **Ctrl+Shift+N** (Chrome/Edge) |

**Console helpers (Chrome/Edge):** `$$('css')` all matches · `$('css')` first match · `$x('//xpath')` XPath · `$0` the element selected in the Elements panel.

**Selectors**

| Want | CSS | XPath |
|---|---|---|
| by id | `#username` | `//*[@id="username"]` |
| by attribute | `[data-testid="book-row"]` | `//*[@data-testid="book-row"]` |
| by text | *(not possible in plain CSS)* | `//button[text()="Sign in"]` |
| inside | `form button` | `//form//button` |
| next sibling | `dt + dd` | `//dt/following-sibling::dd[1]` |

**Commands used in this phase**

| Task | Command |
|---|---|
| Activate the environment | `.\.venv\Scripts\Activate.ps1` |
| Run backend tests | `python manage.py test backend_tests` |
| Start the application | `python manage.py runserver` → <http://localhost:8000> |
| Raw HTTP request | `curl.exe -i http://localhost:8000/api/health/` |

## Appendix B — The documentation set of this repository

These files are produced as the course proceeds; this workbook is their source.

| File | Content | Created |
|---|---|---|
| `README.md` | Overview, prerequisites, setup, execution | grows each phase; final in Phase 7 |
| `docs/COURSE_SYLLABUS.md` | The seven-phase roadmap (Section 2) | Phase 1 |
| `docs/PROJECT_STRUCTURE.md` | The folder tree and what each folder is for | grows; final in Phase 5 |
| `docs/TESTING_GUIDE.md` | How to run UI and API tests, one file, by tag, by browser | from Phase 3 |
| `docs/FINAL_PROJECT.md` | Requirements of the final project | Phase 7 |
| `docs/labs/phase-N/` | Your deliverables for each phase | each phase |

## Appendix C — Instructor notes and verification record

**Verified by execution** (Linux sandbox, Python 3.12, Node 22, headless Chromium):

* The existing project's **43** backend tests pass; with the UI kit and the 11 new tests, **54** pass.
* The existing **49** Playwright API tests (HTTPS) still pass against the upgraded application.
* The supplied UI was driven end to end in a real browser (register → sign in → add → search → delete → sign out) on both `localhost` and `127.0.0.1` over plain HTTP; the browser accepted the `Secure` session cookie on localhost.
* The request sequence on **Sign in** (`csrf → login → me → books`) and the accessibility tree of the Sign in page shown in Lab 1.5 are captured output.
* A reference automation suite for later phases (page objects, fixtures, 60 tests across UI, API and integration, including a phone-sized run) passes against this application. It is **not included here**; students build it in Phases 3–7.

**Not executed here:** the PowerShell command lines, the DevTools click-paths and Console results on Windows/Chrome (standard behaviour, but check on your machine), and Firefox/WebKit behaviour.

**Found while building the reference suite (useful later as debugging material):** a CSS rule `display:inline-block` on a link overrode the HTML `hidden` attribute, so a link meant to be hidden was visible. The UI kit's stylesheet already contains the one-line fix (`[hidden] { display: none !important; }`).

**Pacing:** Lab 1.0 (45 min) · 1.1 (45) · 1.2 (45) · 1.3 (60) · 1.4 (60) · 1.5 (60) · 1.6 (45) · 1.7 (30).

**Suggested Phase 1 grading:** feature inventory 20% · manual scenarios 30% · locator notes 15% · UI→API map 15% · knowledge check 10% · explanation of the sign-in flow 10%.
