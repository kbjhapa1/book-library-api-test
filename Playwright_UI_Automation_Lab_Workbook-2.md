# Playwright UI Automation with TypeScript — Hands-On Lab Workbook

### Built on the Book Library project · Student edition · 7 phases

> **Your goal:** learn to think and work like a QA Automation Engineer — understand an application, decide what is worth automating, build reliable UI and API tests with Playwright and TypeScript, organize them as a maintainable framework, and run them in CI/CD.

> **Edition status:** this file contains the **course overview, the inspection of the existing project, the seven-phase roadmap, Phase 1 (complete) and Phase 2 (complete)**. Phases 3–7 are added one at a time, after you finish the previous phase.

---

## Table of Contents

0. [Read me first](#0-read-me-first)
1. [The existing project (what we build on)](#1-the-existing-project-what-we-build-on)
2. [The seven-phase roadmap (syllabus)](#2-the-seven-phase-roadmap-syllabus)
3. [What you will have built at the end](#3-what-you-will-have-built-at-the-end)
4. [**Phase 1 — Testing fundamentals and web application concepts**](#phase-1--testing-fundamentals-and-web-application-concepts)
5. [**Phase 2 — TypeScript for automation testers**](#phase-2--typescript-for-automation-testers)
6. [Appendices](#appendices)

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
| 2 | TypeScript for automation testers | **Included** | ☐ |
| 3 | Playwright fundamentals | Next | ☐ |
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
| **2** | TypeScript for automation testers | Only the TypeScript you need: types, functions, interfaces, classes, async/await, JSON data | `e2e/practice/` practice files and a first reusable utility | 5–6 h |
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

> **Phase 1 is complete.** When your checkpoint passes, say **"Phase 1 complete"** — Phase 2 (TypeScript for automation testers) follows directly below.

---

# Phase 2 — TypeScript for automation testers

> **Time:** about 5–6 hours · **Where you work:** the new folder `e2e/` inside the project · **You will need:** the application from Phase 1 running (only Labs 2.7 and 2.9 call it)

## Phase 2 at a glance

Playwright tests are ordinary TypeScript programs. You do **not** need to become a programmer, but you must be able to **read** every line of a test and **write** small pieces yourself. This phase teaches exactly the TypeScript that automation testers use — nothing more — and every example comes from the Book Library.

| Lab | Topic | Type | Time |
|---|---|---|---|
| 2.0 | Set up the `e2e` project; JavaScript vs TypeScript | 🧭 instructor-guided | 45 min |
| 2.1 | Variables, data types, strings, template literals | 🧭 + ✍️ | 40 min |
| 2.2 | Arrays, objects, conditions, loops | 🧭 + ✍️ | 50 min |
| 2.3 | Functions, arrow functions, a reusable utility | 🧭 + ✍️ | 45 min |
| 2.4 | Interfaces and types (a test user, a book) | 🧭 + ✍️ | 40 min |
| 2.5 | Classes, objects, access modifiers | 🧭 + ✍️ | 45 min |
| 2.6 | Imports and exports between files | 🧭 + ✍️ | 40 min |
| 2.7 | Promises, `async`/`await`, exception handling | 🧭 + ✍️ | 60 min |
| 2.8 | Working with JSON test data | 🧭 + ✍️ | 45 min |
| 2.9 | Capstone: a smoke check; your own TypeScript notes | ✍️ independent | 45 min |
| 🏆 | Optional challenge: a cookie jar and a full API session | optional | 30 min |

**Symbols used in every lab**

* 🧭 **Instructor-guided** — follow the steps exactly; the explanation tells you why.
* ✍️ **Student-independent** — you decide how; a hidden hint or answer is provided to check yourself.
* 🏆 **Optional challenge** — harder; skipping it does not block Phase 3.

**How to study.** Type the code yourself instead of pasting it. Typing makes you notice every character; a missing comma is the most common reason for a red error, and meeting that error *now* is cheap.

**The big picture of this phase**

```
Lab 2.0   set up the tools; see TypeScript catch a mistake
Labs 2.1–2.3   values, collections, functions      ──▶  the building blocks
Labs 2.4–2.5   shapes (interfaces) and classes     ──▶  how page objects will look (Phase 5)
Lab 2.6        files that share code               ──▶  how the framework is organised
Lab 2.7        async / await and errors            ──▶  how EVERY browser step works (Phase 3)
Lab 2.8        JSON test data                      ──▶  data-driven tests
Lab 2.9        a small working check of the app    ──▶  everything together
```

---

## Lab 2.0 — Set up the `e2e` project; JavaScript vs TypeScript 🧭

### Learning objectives

After this lab you can:

* say in two sentences what TypeScript adds to JavaScript, and why testers benefit;
* create a Node project and install TypeScript tooling with `npm`;
* explain the three tools you will use: `node`, `tsx` and `tsc`;
* read the configuration file `tsconfig.json`;
* run a `.ts` file, and see the compiler reject a mistake **before** the code runs.

### Concepts in simple language

**JavaScript** is the language browsers and Node.js run. **TypeScript** is JavaScript **plus labels called types**. A type says what kind of value something is: text (`string`), a number (`number`), true/false (`boolean`), and so on.

Think of the labels on a spice rack. JavaScript lets you pour anything into any jar and finds out later, while cooking, that the "sugar" jar held salt. TypeScript reads the labels **before** you start cooking and tells you: *"this jar is for numbers, you are putting text in it."*

```
 your file  login.ts   ──▶  TypeScript checks the types  ──▶  JavaScript runs
                              (red squiggle, or error text            (browser or Node)
                               in the terminal, BEFORE running)
```

TypeScript is **removed** before the code runs: the types are only a safety net, and the final program is plain JavaScript.

### Why QA needs it

* **Fewer silly failures.** A typo such as `usrename` is caught while you type, not after a 4-minute test run.
* **Auto-complete.** The editor shows which actions a Playwright page offers, so you do not memorise them.
* **Readable contracts.** An interface (Lab 2.4) documents what an API returns — useful documentation for the whole team.
* Playwright is written in TypeScript and its examples, errors and community answers all assume it.

### The three tools

| Tool | What it does | When you use it |
|---|---|---|
| `node` | Runs JavaScript | Behind the scenes |
| `tsx` | Runs a `.ts` file **directly** (it strips the types and runs the rest) — it does **not** check types | `npx tsx practice/01-hello.ts` |
| `tsc` | The TypeScript **compiler**: checks all types; can also write `.js` files | `npx tsc --noEmit` (check only) |

> **Remember:** `tsx` runs, `tsc` checks. A file with a type error still *runs* under `tsx` — you saw it can; that is why we also run `npm run typecheck`. (In Phase 3, Playwright runs TypeScript itself; the checking habit stays.)

### Prerequisites

* Phase 1 complete; the application folder from Phase 1 (the one containing `manage.py`).
* **Node.js 20 or newer** (the course was verified with Node 22).
* A code editor — **Visual Studio Code** is recommended because it shows type errors as red underlines.

### Files created in this lab

```
e2e/
├── package.json        what this Node project is + its scripts + its tools
├── package-lock.json   exact versions installed (created by npm; commit it)
├── tsconfig.json       the TypeScript rules for the project
├── .gitignore          files Git must not store
└── practice/
    └── 01-hello.ts     your first TypeScript file
```

### Step-by-step

**Step 1 — Check Node.js and npm.**

```powershell
node --version
npm --version
```

Expected: `v20.x` or higher (for example `v22.12.0`) and a number such as `10.9.0`. If PowerShell says *"node is not recognized"*, install the **LTS** version from <https://nodejs.org/>, close PowerShell, open a new one, and try again.

**Step 2 — Create the folder and a Node project.** From the application folder (where `manage.py` is):

```powershell
mkdir e2e
cd e2e
mkdir practice, utils, data
```

Now create `e2e/package.json` with exactly this content (type it in your editor):

```json
{
  "name": "book-library-e2e",
  "version": "1.0.0",
  "description": "Playwright + TypeScript automation for the Book Library application",
  "private": true,
  "scripts": {
    "typecheck": "tsc --noEmit"
  }
}
```

| Line | Meaning |
|---|---|
| `"name"`, `"version"`, `"description"` | Labels for the project |
| `"private": true` | Never publish this folder to the public npm registry by accident |
| `"scripts"` | Shortcuts. `npm run typecheck` runs `tsc --noEmit` |

**Step 3 — Install the tools.**

```powershell
npm install --save-dev typescript tsx @types/node
```

`--save-dev` means "needed to develop and test, not to run a product". `@types/node` teaches TypeScript the shapes of Node's built-in features (`process`, `fs`, `crypto`…). It creates the folder `node_modules/` (thousands of files — never edit, never commit) and the file `package-lock.json`. Open `package.json` again: a `devDependencies` section has appeared.

**Step 4 — Create `tsconfig.json`.**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "noEmit": true,
    "types": ["node"]
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "dist-demo"]
}
```

| Setting | Meaning in plain words |
|---|---|
| `target: ES2022` | Which modern JavaScript the output may use (Node 20+ understands it) |
| `module` / `moduleResolution: NodeNext` | Follow Node's rules for how files import each other |
| **`strict: true`** | **The most important line.** Turns on the strictest, most helpful checks. Always keep it on |
| `esModuleInterop` | Smooths over differences between old and new import styles |
| `resolveJsonModule` | Lets you `import` a `.json` file (Lab 2.8) |
| `skipLibCheck` | Do not re-check other people's type files (faster) |
| `noEmit: true` | The compiler only **checks**; it does not write `.js` files |
| `types: ["node"]` | Load the Node type definitions |
| `include` / `exclude` | Which files belong to the project |

**Step 5 — Create `.gitignore`.**

```
node_modules/
dist-demo/
test-results/
playwright-report/
.auth/
.env
```

(`.auth/` and `.env` appear in later phases: saved sign-in state and secrets must never reach Git.)

**Step 6 — Your first TypeScript file.** Create `practice/01-hello.ts`:

*File: `e2e/practice/01-hello.ts`*

```ts
// My first TypeScript file
const appName: string = 'Book Library';
const bookCount: number = 3;

console.log(`Welcome to ${appName}. We have ${bookCount} books.`);
```

**Step 7 — Run it.**

```powershell
npx tsx practice/01-hello.ts
```

```text
Welcome to Book Library. We have 3 books.
```

`npx` runs a tool installed in `node_modules`. Line by line: `const` creates a name that cannot be re-pointed; `appName` is text, `bookCount` a number; the backticks with `${...}` build one text from pieces (a *template literal*, Lab 2.1); `console.log` prints to the terminal.

**Step 8 — See TypeScript protect you.** Temporarily change line 3 to:

```ts
const bookCount: number = 'three';
```

Run the checker:

```powershell
npm run typecheck
```

You should see an error similar to this (the file name is the one you edited):

```text
practice/01-hello.ts(3,7): error TS2322: Type 'string' is not assignable to type 'number'.
```

Read it like a sentence: *file (line, column): error code: you put text where a number is expected.* Now undo the change. **Notice:** `npx tsx practice/01-hello.ts` would still print `We have three books.` — `tsx` does not check. That is exactly why we have a separate checking command.

**Step 9 — (Optional, 3 minutes) See that TypeScript becomes JavaScript.**

```powershell
npx tsc --noEmit false --outDir dist-demo --rootDir .
type dist-demo\practice\01-hello.js
```

(`cat` instead of `type` on macOS/Linux.) The result is plain JavaScript with the types gone:

```js
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// My first TypeScript file
const appName = 'Book Library';
const bookCount = 3;
console.log(`Welcome to ${appName}. We have ${bookCount} books.`);
```

Delete the folder afterwards (`Remove-Item -Recurse dist-demo`). The folder is already in `.gitignore`.

### Common mistakes

* Creating `package.json` in the wrong folder → create it in `e2e/`, run every `npm` command **inside** `e2e/`.
* Running `npm install` before creating `package.json` → npm creates a different one. Do Step 2 first.
* Typing `tsx file.ts` without `npx` → "not recognized". Use `npx tsx …`, or use an `npm run` script.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `'node' is not recognized` | Node not installed or terminal not restarted | Install the LTS version; open a **new** terminal |
| `npm ERR! code ENOENT … package.json` | You are in the wrong folder | `cd` into `e2e` |
| `npm install` hangs or fails with a network error | Proxy or firewall | Ask your instructor; set the company proxy with `npm config set proxy …` |
| `error TS5011` or very strange errors in a single-file compile | Running `tsc file.ts` ignores `tsconfig.json` | Use project mode (`npx tsc --noEmit`) as shown |
| Nothing is red in VS Code | Editor uses another TypeScript | Open the **`e2e`** folder (not the parent) in VS Code |

### ✍️ Independent exercise

1. Add a second constant `baseUrl` with the value `'http://localhost:8000'` and print one sentence that includes it.
2. Create the mistake `const bookCount: number = true;`. Which error code do you get? (Hint: the same family, `TS2322`.) Fix it again.
3. Add a script `"hello": "tsx practice/01-hello.ts"` to `package.json` and run `npm run hello`.

<details><summary>Check yourself</summary>

```ts
const baseUrl = 'http://localhost:8000';
console.log(`${appName} is running at ${baseUrl}`);
```

The error for `true` is `TS2322: Type 'boolean' is not assignable to type 'number'.` For exercise 3, `npm run hello` prints the same welcome line as before.
</details>

### Knowledge check (Lab 2.0)

1. What is a "type"? *(A label that says what kind of value something holds.)*
2. Which command runs a TypeScript file, and which one checks the types? *(`npx tsx file.ts` / `npm run typecheck`.)*
3. Why is `strict: true` always on? *(It enables the checks that catch the most mistakes.)*

### Completion checklist

- [ ] `node --version` shows 20 or higher.
- [ ] `e2e/` contains `package.json`, `package-lock.json`, `tsconfig.json`, `.gitignore`, and the folders `practice/`, `utils/`, `data/`.
- [ ] `npx tsx practice/01-hello.ts` prints the welcome line.
- [ ] `npm run typecheck` is silent (no output = success) with the file correct, and shows `TS2322` when I break it.
- [ ] I can explain what `tsx` and `tsc` each do.

---

## Lab 2.1 — Variables, data types, strings and template literals 🧭 + ✍️

### Learning objectives

* Declare values with `const` and `let` and know which to choose.
* Use the basic types: `string`, `number`, `boolean`, `null`, `undefined`.
* Combine types with a **union** (`number | null`) and restrict values with **literal types**.
* Build text with **template literals** and use common string and number methods.

### Concepts in simple language

A **variable** is a named box holding a value.

* `const name = value` — the name always points to that value. **Use this by default.**
* `let name = value` — the name may be pointed at a new value later. Use only when the value really changes (a counter).
* Never use `var` (old and confusing; you may see it in old code).

**TypeScript infers types.** In `const year = 1965` it knows `year` is a number. You *may* write the type (`const year: number = 1965`); do so when it helps the reader or when the value is not obvious.

**"There is no value"** has two spellings: `null` ("deliberately empty", what the API sends for a missing year) and `undefined` ("never set"). A **union** lists the allowed alternatives: `number | null`.

**Template literal:** text between backticks `` ` ` `` where `${…}` inserts any value or calculation. It replaces clumsy `'a' + b + 'c'`.

### Why QA needs it

Test data is mostly values: URLs, usernames, years, titles. Wrong types are classic test bugs — for example the year `"1965"` (text) versus `1965` (number). The API returns a **number or `null`** for the year, and the form holds **text**; the types make that difference visible.

### Prerequisites

Lab 2.0 complete.

### Files

`practice/02-variables.ts` (create now)

### Step-by-step

**Step 1.** Create `practice/02-variables.ts` and type the code below.

*File: `e2e/practice/02-variables.ts`*

```ts
// Lab 2.1 - variables, types, strings

// const = a name that can never point to another value. Use it by default.
const appName = 'Book Library';
const baseUrl = 'http://localhost:8000';
const maxTitleLength = 200;
const isHeadless = true;

// let = a name whose value may change later.
let signedInUsers = 0;
signedInUsers = signedInUsers + 1;
signedInUsers += 1; // shorthand for the line above

// TypeScript infers the type from the value, but you may also write it.
const author: string = 'Frank Herbert';
const year: number = 1965;
const isOwner: boolean = false;

// null / undefined: "there is no value".
let publishedYear: number | null = null; // a union type: a number OR null
publishedYear = 1965;

// A union of fixed texts ("literal types") allows only those exact words.
type BrowserName = 'chromium' | 'firefox' | 'webkit';
const browser: BrowserName = 'chromium';

// unknown = "I do not know what this is yet", so check before you use it.
const fromServer: unknown = JSON.parse('{"status":"ok"}');
if (typeof fromServer === 'object' && fromServer !== null && 'status' in fromServer) {
  console.log('server says:', (fromServer as { status: string }).status);
}

console.log('--- strings ---');
const bookId = 7;
console.log(`${baseUrl}/books/${bookId}/`); // template literal: backticks + ${...}
console.log(`Title limit is ${maxTitleLength} characters`);
console.log(`${year + 1} is next year`); // any expression works inside ${}

const messy = '   Dune   ';
console.log('[' + messy.trim() + ']'); // the page trims titles too
console.log('DUNE'.toLowerCase(), 'dune'.toUpperCase());
console.log('Dune Messiah'.includes('Messiah'), 'Dune'.startsWith('Du'));
console.log('Frank Herbert'.slice(0, 5), 'Frank Herbert'.split(' '));
console.log('7'.padStart(3, '0'), 'ab'.repeat(3));

console.log('--- numbers ---');
console.log(Number('1965'), Number('abc'), Number.isInteger(1965.5));
console.log(parseInt('42px', 10), (0.1 + 0.2).toFixed(2));

console.log('--- summary ---');
console.log({ appName, signedInUsers, author, isOwner, publishedYear, browser, isHeadless });
```

**Step 2.** Run it, then check the types:

```powershell
npx tsx practice/02-variables.ts
npm run typecheck
```

### Expected output

```text
server says: ok
--- strings ---
http://localhost:8000/books/7/
Title limit is 200 characters
1966 is next year
[Dune]
dune DUNE
true true
Frank [ 'Frank', 'Herbert' ]
007 ababab
--- numbers ---
1965 NaN false
42 0.30
--- summary ---
{
  appName: 'Book Library',
  signedInUsers: 2,
  author: 'Frank Herbert',
  isOwner: false,
  publishedYear: 1965,
  browser: 'chromium',
  isHeadless: true
}
```

`npm run typecheck` prints nothing when everything is correct.

### Line-by-line explanation

| Code | Explanation |
|---|---|
| `const appName = 'Book Library'` | A text value. Single quotes are the project style |
| `let signedInUsers = 0` then `+= 1` | A number that changes. `x += 1` means `x = x + 1` |
| `const author: string = …` | The type is written out; same meaning as without |
| `let publishedYear: number \| null = null` | A union type. First empty, later a number — both allowed |
| `type BrowserName = 'chromium' \| 'firefox' \| 'webkit'` | A **literal union**: only these three words are valid. Playwright's browser names work like this |
| `const fromServer: unknown = JSON.parse(…)` | Data from outside is `unknown` until you check it |
| `typeof x === 'object' && x !== null && 'status' in x` | The check that makes `unknown` safe to use |
| `` `${baseUrl}/books/${bookId}/` `` | Template literal: builds a URL from parts |
| `.trim()`, `.toLowerCase()`, `.includes()`, `.startsWith()`, `.slice()`, `.split()`, `.padStart()`, `.repeat()` | The string helpers testers use most |
| `Number('abc')` is `NaN` | "Not a Number" — the result of a failed conversion |
| `(0.1 + 0.2).toFixed(2)` | `0.1 + 0.2` is `0.30000000000000004` in every language that uses floating point; `toFixed(2)` rounds for display |

### Try it: type errors you will really meet

Add each line at the end of the file, run `npm run typecheck`, read the error, then remove the line.

| You write | The compiler says (real output) | Meaning |
|---|---|---|
| `appName = 'Other'` | `error TS2588: Cannot assign to 'appName' because it is a constant.` | Use `let` if it must change |
| `const n: number = 'five'` | `error TS2322: Type 'string' is not assignable to type 'number'.` | Wrong kind of value |
| `const b: BrowserName = 'safari'` | `error TS2322: Type '"safari"' is not assignable to type 'BrowserName'.` | Not one of the allowed words |
| `const y = getYear(); y.toFixed(0)` where `getYear()` returns `number \| null` | `error TS18047: 'y' is possibly 'null'.` | You must check for `null` first |

### Common mistakes

* Using `==` instead of `===`. `===` compares value **and** type and is what you want (`1 == '1'` is `true`, `1 === '1'` is `false`).
* Writing quotes instead of backticks around `${…}` — the text then prints literally as `${year}`.
* Forgetting that `'5' + 3` is `'53'` (text joined), while `5 + 3` is `8`.
* Using `let` for everything. Prefer `const`; it tells the reader "this never changes".

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Output shows `${bookId}` literally | Quotes instead of backticks | Use the backtick key (top-left, below Esc) |
| `TS2322` on a value from JSON | Types disagree | Check whether the data is text or number |
| `NaN` printed | Converting text that is not a number | Validate the text first, as `yearError` does in Lab 2.3 |

### ✍️ Independent exercise

1. Declare `const bookTitle = 'Emma'` and `const rating = 4.5`. Print: `Emma is rated 4.5 out of 5`.
2. Declare a variable `searchText` of type `string | null`, set it to `null`, then to `'austen'`. Print its upper-case version **after** assigning.
3. Build the URL for book number 12 with a template literal, using `baseUrl`.
4. Create `type Role = 'owner' | 'visitor'` and a variable that is a `Role`. Try the value `'admin'` and read the error.

<details><summary>Answer</summary>

```ts
const bookTitle = 'Emma';
const rating = 4.5;
console.log(`${bookTitle} is rated ${rating} out of 5`);

let searchText: string | null = null;
searchText = 'austen';
console.log(searchText.toUpperCase()); // fine: TypeScript knows it is a string after the assignment

const bookUrl = `${baseUrl}/api/books/${12}/`;

type Role = 'owner' | 'visitor';
const role: Role = 'owner';
// const bad: Role = 'admin'; // error TS2322: Type '"admin"' is not assignable to type 'Role'.
```
</details>

### Knowledge check (Lab 2.1)

1. Which keyword is the default choice, `const` or `let`? *(`const`.)*
2. What does `number | null` mean? *(Either a number or no value.)*
3. What is `` `Hi ${name}` `` called? *(A template literal.)*
4. What is the value of `'5' + 3`? *(`'53'`.)*

### Completion checklist

- [ ] `02-variables.ts` runs and the typecheck is silent.
- [ ] I produced and read at least three compiler errors from the "Try it" table.
- [ ] I finished the independent exercise.
- [ ] I can explain `const` vs `let`, and `null` vs a number, using the Book Library year as the example.

---

## Lab 2.2 — Arrays, objects, conditions and loops 🧭 + ✍️

### Learning objectives

* Create and read **objects** and **arrays**; use destructuring and spread.
* Use the array methods `filter`, `map`, `find`, `some`, `every`, `sort`.
* Use `?.` (optional chaining) and `??` (fallback) safely.
* Write `if`, `switch`, the ternary `? :`, and the loops `for…of`, `for`, `forEach`, `while`.

### Concepts in simple language

* An **object** groups named values: `{ title: 'Dune', year: 1965 }` — one book.
* An **array** is an ordered list: `['Emma', 'Dune']` — the book list. Counting starts at **0**.
* **Array methods** work on the whole list without writing a loop: *filter* keeps some, *map* changes each, *find* returns the first match, *some/every* answer yes/no questions.
* `??` means "if the left side is `null` or `undefined`, use the right side". `?.` means "if the left side is missing, stop and give `undefined` instead of crashing".

### Why QA needs it

Every API list and every group of page elements you meet becomes an array of objects. "Does the list contain my book?", "How many rows?", "Is every title non-empty?" are one-line array methods. The Books page shows `—` for a missing year — that is `??`.

### Prerequisites

Lab 2.1 complete.

### Files

`practice/03-collections.ts`

### Step-by-step

Create `practice/03-collections.ts`, type the code, then run `npx tsx practice/03-collections.ts` and `npm run typecheck`.

*File: `e2e/practice/03-collections.ts`*

```ts
// Lab 2.2 - arrays, objects, conditions, loops

// An object groups related values (like one book in the list).
const dune = {
  title: 'Dune',
  author: 'Frank Herbert',
  published_year: 1965 as number | null,
  owner: 'anna',
};

console.log(dune.title, dune['author']); // two ways to read a property
dune.title = 'Dune (2nd edition)'; // properties can change even on a const object

// Destructuring and spread
const { title, author } = dune;
const copy = { ...dune, title: 'Dune Messiah', published_year: null as number | null };
console.log(title, '/', author, '/', copy.title);

// An array is an ordered list.
interface Row {
  title: string;
  author: string;
  published_year: number | null;
}
const rows: Row[] = [
  { title: 'Emma', author: 'Jane Austen', published_year: 1815 },
  { title: 'Persuasion', author: 'Jane Austen', published_year: 1817 },
  { title: 'Dune', author: 'Frank Herbert', published_year: 1965 },
  { title: 'Untitled Draft', author: 'Anonymous', published_year: null },
];

console.log('count:', rows.length, '| first:', rows[0].title, '| last:', rows[rows.length - 1].title);

console.log('--- array methods (you will use these on page and API data) ---');
const austen = rows.filter((r) => r.author.includes('Austen')); // keep some
const titles = rows.map((r) => r.title); // transform each
const firstOld = rows.find((r) => r.published_year !== null && r.published_year < 1900); // first match
const anyMissingYear = rows.some((r) => r.published_year === null); // at least one?
const allHaveAuthor = rows.every((r) => r.author !== ''); // every one?
console.log(austen.length, titles, firstOld?.title, anyMissingYear, allHaveAuthor);

const sorted = [...rows].sort((a, b) => a.title.localeCompare(b.title)); // copy first, then sort
console.log('sorted:', sorted.map((r) => r.title));
const byYearNewest = [...rows]
  .filter((r) => r.published_year !== null)
  .sort((a, b) => (b.published_year as number) - (a.published_year as number));
console.log('newest first:', byYearNewest.map((r) => `${r.title} (${r.published_year})`));

console.log('--- optional chaining and ?? ---');
for (const row of rows) {
  // ?? gives a fallback when the value is null/undefined - exactly what the Books page does.
  console.log(`${row.title}: ${row.published_year ?? '—'}`);
}
const missing: Row | undefined = rows.find((r) => r.title === 'Nope');
console.log('missing?.title =', missing?.title); // undefined instead of a crash

console.log('--- conditions ---');
function describeStatus(code: number): string {
  if (code >= 200 && code < 300) return 'success';
  if (code >= 400 && code < 500) return 'client error';
  if (code >= 500) return 'server error';
  return 'other';
}
for (const code of [200, 201, 204, 302, 400, 401, 403, 404, 500]) {
  console.log(code, '->', describeStatus(code));
}

function statusName(code: number): string {
  switch (code) {
    case 200:
      return 'OK';
    case 201:
      return 'Created';
    case 204:
      return 'No Content';
    case 401:
      return 'Unauthorized';
    case 403:
      return 'Forbidden';
    case 404:
      return 'Not Found';
    default:
      return 'Unknown';
  }
}
console.log(statusName(201), statusName(405));
const label = rows.length === 1 ? '1 book' : `${rows.length} books`; // ternary = a short if/else
console.log(label);

console.log('--- loops ---');
for (const row of rows) console.log('for...of      ', row.title);
for (let i = 0; i < 2; i++) console.log('for (counter)', i, rows[i].title);
rows.forEach((row, index) => console.log('forEach       ', index, row.title));
let attempts = 0;
while (attempts < 3) {
  attempts++;
}
console.log('while loop finished after', attempts, 'attempts');
for (const [index, row] of rows.entries()) {
  if (row.published_year === null) {
    console.log('first book without a year is at index', index);
    break; // stop the loop early
  }
}
```

### Expected output

```text
Dune Frank Herbert
Dune (2nd edition) / Frank Herbert / Dune Messiah
count: 4 | first: Emma | last: Untitled Draft
--- array methods (you will use these on page and API data) ---
2 [ 'Emma', 'Persuasion', 'Dune', 'Untitled Draft' ] Emma true true
sorted: [ 'Dune', 'Emma', 'Persuasion', 'Untitled Draft' ]
newest first: [ 'Dune (1965)', 'Persuasion (1817)', 'Emma (1815)' ]
--- optional chaining and ?? ---
Emma: 1815
Persuasion: 1817
Dune: 1965
Untitled Draft: —
missing?.title = undefined
--- conditions ---
200 -> success
201 -> success
204 -> success
302 -> other
400 -> client error
401 -> client error
403 -> client error
404 -> client error
500 -> server error
Created Unknown
4 books
--- loops ---
for...of       Emma
for...of       Persuasion
for...of       Dune
for...of       Untitled Draft
for (counter) 0 Emma
for (counter) 1 Persuasion
forEach        0 Emma
forEach        1 Persuasion
forEach        2 Dune
forEach        3 Untitled Draft
while loop finished after 3 attempts
first book without a year is at index 3
```

### Line-by-line explanation

| Code | Explanation |
|---|---|
| `dune.title` and `dune['author']` | Two ways to read a property. The dot is normal; the brackets help when the name is in a variable |
| `dune.title = '…'` on a `const` object | Allowed. `const` stops the **name** being re-pointed, not the object's contents changing |
| `const { title, author } = dune` | Destructuring: pull properties out into variables |
| `{ ...dune, title: 'Dune Messiah' }` | Spread: copy all properties, then override some. The original is untouched |
| `interface Row { … }` and `rows: Row[]` | A shape, and "an array of that shape" (Lab 2.4 explains interfaces) |
| `rows.filter(r => …)` | New array with only rows where the test is true |
| `rows.map(r => r.title)` | New array with one value per row |
| `rows.find(…)` | The first match, or `undefined` |
| `rows.some(…)` / `rows.every(…)` | Is at least one / is every row true? |
| `[...rows].sort(…)` | Sort changes the array it is called on, so **copy first** with `[...rows]` |
| `a.title.localeCompare(b.title)` | Alphabetical comparison of text |
| `row.published_year ?? '—'` | Show a dash when the year is missing |
| `missing?.title` | `undefined`, not a crash, when `missing` is `undefined` |
| `if / else if / switch / ? :` | Three ways to choose. Use `switch` for many fixed values |
| `for (const row of rows)` | "For each row" — the loop you will use most |
| `for (let i = 0; i < 2; i++)` | Counter loop, for when you need the position |
| `rows.forEach((row, index) => …)` | Same idea as a method |
| `while (attempts < 3)` | Repeat while a condition is true (retry logic) |
| `break` | Leave the loop early |

### Try it: real compiler errors

| You write | Real compiler output | Meaning |
|---|---|---|
| `const bad: Row = { title: 'X', author: 'Y' }` | `error TS2741: Property 'published_year' is missing in type '{ title: string; author: string; }' but required in type 'Row'.` | A required property is missing |
| `rows[0].titel` | `error TS2551: Property 'titel' does not exist on type 'Row'. Did you mean 'title'?` | Typo caught immediately, with a suggestion |
| `const first = rows.find(r => r.title === 'Nope'); first.title` | `error TS18048: 'first' is possibly 'undefined'.` | `find` may find nothing — use `first?.title` |

### Common mistakes

* **Sorting the original array** — `rows.sort(…)` reorders the very list you are using. Copy first.
* **`filter` when you want one item** — it returns an *array*; use `find` for a single match.
* **Using `forEach` with `await` inside** — it does not wait. Use `for…of` (Lab 2.7).
* **Off-by-one** — the last item is `rows[rows.length - 1]`, not `rows[rows.length]`.
* Using `||` instead of `??`: `0 || 5` is `5`, but `0 ?? 5` is `0`. For values that can legitimately be `0` or `''`, use `??`.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `TS18048 … possibly 'undefined'` | `find` can return nothing | Use `?.` or check with `if` |
| `Cannot read properties of undefined (reading 'title')` at run time | You indexed past the end of the array | Check `rows.length` first |
| The "sorted" and "original" lists are the same order | You sorted the original | `[...rows].sort(…)` |

### ✍️ Independent exercise

Using the `rows` array:

1. Print the titles of all books published **after 1816**.
2. Print how many books have **no** year.
3. Print the author names **without duplicates** (hint: `new Set(array)`).
4. Write `function describe(row: Row): string` that returns `Emma (1815) by Jane Austen`, or `Untitled Draft (no year) by Anonymous` when the year is `null`.

<details><summary>Answer</summary>

```ts
console.log(rows.filter((r) => r.published_year !== null && r.published_year > 1816).map((r) => r.title));
console.log(rows.filter((r) => r.published_year === null).length);
console.log([...new Set(rows.map((r) => r.author))]);

function describe(row: Row): string {
  const year = row.published_year === null ? 'no year' : String(row.published_year);
  return `${row.title} (${year}) by ${row.author}`;
}
console.log(rows.map(describe));
```
</details>

### Knowledge check (Lab 2.2)

1. Which method gives you *one* matching item? *(`find`.)*
2. Which one answers "is every title non-empty?" *(`every`.)*
3. What does `x ?? 'n/a'` do? *(Uses `'n/a'` only when `x` is `null` or `undefined`.)*
4. Why write `[...rows].sort(…)`? *(To avoid changing the original array.)*

### Completion checklist

- [ ] `03-collections.ts` runs; typecheck is silent.
- [ ] I can use `filter`, `map`, `find`, `some` and `every` without looking.
- [ ] I solved the four-part exercise.
- [ ] I can explain `?.` and `??` with the Books page "—" example.

---

## Lab 2.3 — Functions, arrow functions and a reusable utility 🧭 + ✍️

### Learning objectives

* Write functions with typed **parameters** and a typed **return value**.
* Write **arrow functions**; use default and optional parameters; understand `void`.
* Pass a function to another function (a **callback**).
* Build two helpers you will reuse all course: `uniqueUsername()` and the Book Library's validation rules.

### Concepts in simple language

A **function** is a named recipe: input in, result out. Writing the recipe once and calling it many times is the foundation of maintainable tests.

```ts
function add(a: number, b: number): number { return a + b; }
//        name  parameters (typed)          return type
const double = (n: number): number => n * 2;   // arrow function: same thing, shorter
```

A function can also be handed around like any value. `['dune','emma'].map(shout)` hands `shout` to `map`, which calls it for every item — a **callback**. Playwright uses this constantly (`test('name', async () => { … })`).

### Why QA needs it

* **Unique test data.** If two test runs both register `anna`, the second fails with "username taken". A helper that makes `qa_3fa9c2d1` removes that whole class of failure.
* **Rules as code.** The same limits you tested by hand in Lab 1.1 (title 1–200 characters, year 1000–2100) become functions you can call with dozens of inputs.

### Prerequisites

Lab 2.2 complete.

### Files

`practice/04-functions.ts`

### Step-by-step

Create `practice/04-functions.ts`, type it, and run `npx tsx practice/04-functions.ts`.

*File: `e2e/practice/04-functions.ts`*

```ts
// Lab 2.3 - functions
import { randomBytes } from 'node:crypto'; // (imports are explained properly in Lab 2.6)

// 1) A function declaration: name, typed parameters, typed return value.
function add(a: number, b: number): number {
  return a + b;
}

// 2) An arrow function: same idea, shorter. Often stored in a const or passed to another function.
const double = (n: number): number => n * 2;

// 3) Default and optional parameters.
function greet(name: string, greeting = 'Hello'): string {
  return `${greeting}, ${name}!`;
}
function describeBook(title: string, year?: number): string {
  return year === undefined ? title : `${title} (${year})`;
}

// 4) void = the function does something but returns nothing useful.
function logStep(step: number, text: string): void {
  console.log(`  step ${step}: ${text}`);
}

console.log(add(2, 3), double(21));
console.log(greet('Anna'), '|', greet('Anna', 'Welcome'));
console.log(describeBook('Dune'), '|', describeBook('Dune', 1965));
logStep(1, 'open /login/');

// 5) Functions are values: pass one into another ("callback").
const shout = (text: string): string => text.toUpperCase();
console.log(['dune', 'emma'].map(shout));
console.log([5, 12, 8].filter((n) => n > 7));

console.log('--- useful for test automation ---');

// 6) Unique text for test data: random hex, so two runs never collide.
function uid(): string {
  return randomBytes(4).toString('hex'); // e.g. "3fa9c2d1"
}
function uniqueUsername(prefix = 'qa'): string {
  return `${prefix}_${uid()}`;
}
console.log(uniqueUsername(), uniqueUsername('anna'));

// 7) The Book Library's input rules, written as functions.
//    Each returns an error message, or null when the value is fine.
function titleError(title: string): string | null {
  const trimmed = title.trim();
  if (trimmed === '') return 'Title is required.';
  if (trimmed.length > 200) return 'Title must have at most 200 characters.';
  return null;
}

function yearError(text: string): string | null {
  const trimmed = text.trim();
  if (trimmed === '') return null; // the year is optional
  if (!/^\d+$/.test(trimmed)) return 'Year must be a whole number.'; // browser-side rule
  const year = Number(trimmed);
  if (year < 1000 || year > 2100) return 'Year must be between 1000 and 2100.'; // server-side rule
  return null;
}

console.log(titleError(''), '|', titleError('   '), '|', titleError('Dune'));

// The boundary table from Lab 1.1, as code:
console.log('--- boundary values for the year ---');
for (const input of ['999', '1000', '2100', '2101', '', 'abc']) {
  const error = yearError(input);
  console.log(`${JSON.stringify(input).padEnd(7)} ->`, error === null ? 'valid' : error);
}

// 8) A function that returns a function (you will meet this shape in Playwright fixtures).
function makeCounter(): () => number {
  let count = 0;
  return () => ++count;
}
const next = makeCounter();
console.log('counter:', next(), next(), next());
```

### Expected output

The random parts (`uniqueUsername`) differ on your computer; everything else must match.

```text
5 42
Hello, Anna! | Welcome, Anna!
Dune | Dune (1965)
  step 1: open /login/
[ 'DUNE', 'EMMA' ]
[ 12, 8 ]
--- useful for test automation ---
qa_3d382993 anna_59807f1d
Title is required. | Title is required. | null
--- boundary values for the year ---
"999"   -> Year must be between 1000 and 2100.
"1000"  -> valid
"2100"  -> valid
"2101"  -> Year must be between 1000 and 2100.
""      -> valid
"abc"   -> Year must be a whole number.
counter: 1 2 3
```

### Line-by-line explanation

| Code | Explanation |
|---|---|
| `import { randomBytes } from 'node:crypto'` | Borrow Node's secure random generator. (Lab 2.6 explains imports) |
| `function add(a: number, b: number): number` | Parameters typed; `: number` after the brackets types the result |
| `const double = (n: number): number => n * 2` | Arrow function; for a one-expression body, `return` is implied |
| `greet(name: string, greeting = 'Hello')` | Default parameter: used when the caller passes nothing |
| `describeBook(title: string, year?: number)` | `?` makes a parameter optional; inside it is `number \| undefined` |
| `: void` | "Returns nothing useful" — typical for steps that only *do* something |
| `['dune','emma'].map(shout)` | Callback: `map` calls `shout` for each item |
| `uid()` | 4 random bytes as 8 hexadecimal characters, e.g. `3fa9c2d1` — 4 billion possibilities |
| `uniqueUsername(prefix = 'qa')` | `qa_3fa9c2d1`. Prefix lets you tell whose data it is |
| `titleError` returns `string \| null` | **A pattern to remember:** return the error message, or `null` when fine |
| `/^\d+$/.test(trimmed)` | Regular expression: "only digits, from start to end" |
| The boundary table loop | The same 6-line loop checks six inputs — data-driven thinking |
| `makeCounter()` | A function that returns a function that remembers `count` (a **closure**) |

### Try it: real compiler errors

| You write | Real compiler output | Meaning |
|---|---|---|
| `add(1)` | `error TS2554: Expected 2 arguments, but got 1.` | Missing argument |
| `add('1', 2)` | `error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.` | Wrong kind of argument |
| `function f(x) { return x; }` | `error TS7006: Parameter 'x' implicitly has an 'any' type.` | `strict` demands a type |

### Common mistakes

* Forgetting `return` in a function with braces `{ }` — it returns `undefined`.
* Calling a function without brackets: `uid` is the function; `uid()` is its result.
* Mixing up the two `year` ideas: `yearError` receives **text** (what the form holds), and converts with `Number(...)` only after checking it is digits.
* Putting random values in the expected result of a test. Random data belongs in the **input**, never in the expectation.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Output `undefined` instead of a value | Missing `return` | Add it |
| `TS7006 … implicitly has an 'any' type` | Parameter without a type | Add `: string`, `: number`, … |
| Two runs produce the same "random" name | You called `uid()` once and stored the result | Call it where you need a new value |

### ✍️ Independent exercise

1. Write `bookLabel(title: string, year: number | null): string` returning `Dune (1965)` or `Dune (year unknown)`.
2. Write `isStrongPassword(password: string): boolean` — true when the text has at least 12 characters, one digit and one capital letter. Test it with three passwords.
3. Write `authorError(author: string): string | null` following the same pattern as `titleError` (message `Author is required.`; limit **120** characters).

<details><summary>Answer</summary>

```ts
const bookLabel = (title: string, year: number | null): string =>
  year === null ? `${title} (year unknown)` : `${title} (${year})`;

function isStrongPassword(password: string): boolean {
  return password.length >= 12 && /\d/.test(password) && /[A-Z]/.test(password);
}
console.log(isStrongPassword('short1A'), isStrongPassword('S3cure-Lab-Passw0rd!'), isStrongPassword('nodigitsorcapitals'));

function authorError(author: string): string | null {
  const trimmed = author.trim();
  if (trimmed === '') return 'Author is required.';
  if (trimmed.length > 120) return 'Author must have at most 120 characters.';
  return null;
}
```
Expected for the password test: `false true false`.
</details>

### Knowledge check (Lab 2.3)

1. What is the difference between `uid` and `uid()`? *(The function itself vs its result.)*
2. When would you choose a default parameter vs an optional one? *(Default: a sensible value exists. Optional: it may truly be absent.)*
3. Why should test data be unique on every run? *(So repeated or parallel runs do not collide.)*

### Completion checklist

- [ ] `04-functions.ts` runs and the numbers in the output match.
- [ ] I solved the three-part exercise.
- [ ] I can read an arrow function and explain a callback.
- [ ] I can state the "return the error message or `null`" pattern.


---

## Lab 2.4 — Interfaces and types: describing a test user and a book 🧭 + ✍️

### Learning objectives

* Describe the shape of an object with an `interface` and with a `type`.
* Mark properties **optional** (`?`) and **read-only** (`readonly`).
* Derive new shapes with `Omit<T, …>` and `Partial<T>`.
* Use `as const` and `keyof typeof` for named constants.
* Create your first shared file, `utils/types.ts`.

### Concepts in simple language

An **interface** is a form with labelled fields: it lists which properties an object must have and what kind each is. A value that does not fill the form correctly is rejected by the compiler — **before** any test runs.

```ts
interface TestUser { username: string; password: string; displayName?: string }
//                                                   the ? = this field may be left out
```

A `type` can name anything: an object shape, a union (`'a' | 'b'`), a shortcut. For object shapes `interface` and `type` behave almost the same. **Course rule:** `interface` for objects, `type` for unions and for shapes derived from other shapes.

**Deriving shapes** saves repetition. A book as the server returns it has `id`, `owner` and `created_at`; a book you *send* does not. Instead of writing two almost-identical interfaces, write `type BookData = Omit<Book, 'id' | 'owner' | 'created_at'>` ("a Book without those three"). `Partial<BookData>` means "any subset of BookData".

### Why QA needs it

* An interface is **documentation the compiler enforces**: it states what `GET /api/books/` returns.
* A typo in a property name (`published_yaer`) is caught at once.
* In Phase 6 you will type API responses with `Book` so a changed API breaks the *typecheck* with a precise message.

### Prerequisites

Lab 2.3 complete.

### Files

`utils/types.ts` (new, shared with all later labs) and `practice/05-types.ts`

### Step-by-step

**Step 1.** Create `utils/types.ts`.

*File: `e2e/utils/types.ts`*

```ts
// Shared shapes (types) used by tests, helpers and page objects.
// The word `export` makes a name available to other files (Lab 2.6 explains).

/** A user account the tests sign in with. */
export interface TestUser {
  username: string;
  password: string;
  displayName?: string; // optional: the "?" means it may be missing
}

/** A book exactly as the server returns it (GET /api/books/). */
export interface Book {
  readonly id: number; // readonly: set once, never changed
  title: string;
  author: string;
  published_year: number | null;
  owner: string | null;
  created_at: string;
}

/** What we send when we create a book: a Book without the fields the SERVER fills in. */
export type BookData = Omit<Book, 'id' | 'owner' | 'created_at'>;
```

**Step 2.** Create `practice/05-types.ts`.

*File: `e2e/practice/05-types.ts`*

```ts
// Lab 2.4 - interfaces and types
import type { Book, BookData, TestUser } from '../utils/types';

// 1) Typed test data: the compiler checks every property for us.
const anna: TestUser = {
  username: 'qa_anna',
  password: 'S3cure-Lab-Passw0rd!',
};
const bob: TestUser = { username: 'qa_bob', password: 'S3cure-Lab-Passw0rd!', displayName: 'Bob' };
console.log(anna.username, bob.displayName ?? '(no display name)');

// 2) A valid book to send to the API.
const dune: BookData = {
  title: 'Dune',
  author: 'Frank Herbert',
  published_year: 1965,
};

// 3) A book as returned by the server (has the extra fields).
const stored: Book = { id: 4, ...dune, owner: anna.username, created_at: '2026-11-06T09:12:44Z' };
console.log(stored);
// stored.id = 5;  // <- compile error: id is read-only

// 4) Partial<T>: "any subset of the properties". Perfect for "defaults, with overrides".
function makeBook(overrides: Partial<BookData> = {}): BookData {
  return { title: 'Default Title', author: 'Default Author', published_year: 1999, ...overrides };
}
console.log(makeBook());
console.log(makeBook({ title: 'Emma', published_year: null }));

// 5) A list of typed test cases - "data-driven" thinking (more in Lab 2.8).
interface YearCase {
  name: string;
  input: string;
  valid: boolean;
}
const yearCases: YearCase[] = [
  { name: 'lowest valid year', input: '1000', valid: true },
  { name: 'just below the range', input: '999', valid: false },
  { name: 'not a number', input: 'abc', valid: false },
];
for (const c of yearCases) console.log(`${c.name}: ${c.input} should be ${c.valid ? 'accepted' : 'rejected'}`);

// 6) Named constants instead of "magic numbers". `as const` makes the values exact.
const STATUS = { OK: 200, CREATED: 201, NO_CONTENT: 204, UNAUTHORIZED: 401, FORBIDDEN: 403, NOT_FOUND: 404 } as const;
type StatusName = keyof typeof STATUS; // 'OK' | 'CREATED' | ...
const wanted: StatusName = 'CREATED';
console.log(wanted, '=', STATUS[wanted]);

// 7) interface vs type: for object shapes they are almost the same.
//    Rule of thumb for this course: interface for objects, type for unions and shortcuts.
type Role = 'owner' | 'visitor' | 'staff';
interface Viewer {
  name: string;
  role: Role;
}
const viewer: Viewer = { name: 'zoe', role: 'visitor' };
function canEdit(book: Book, who: Viewer): boolean {
  return who.role === 'staff' || (who.role === 'owner' && book.owner === who.name);
}
console.log('visitor can edit?', canEdit(stored, viewer));
```

**Step 3.** Run and check.

```powershell
npx tsx practice/05-types.ts
npm run typecheck
```

### Expected output

```text
qa_anna Bob
{
  id: 4,
  title: 'Dune',
  author: 'Frank Herbert',
  published_year: 1965,
  owner: 'qa_anna',
  created_at: '2026-11-06T09:12:44Z'
}
{
  title: 'Default Title',
  author: 'Default Author',
  published_year: 1999
}
{ title: 'Emma', author: 'Default Author', published_year: null }
lowest valid year: 1000 should be accepted
just below the range: 999 should be rejected
not a number: abc should be rejected
CREATED = 201
visitor can edit? false
```

### Line-by-line explanation

| Code | Explanation |
|---|---|
| `export interface TestUser` | `export` makes it available to other files (Lab 2.6) |
| `displayName?: string` | Optional; its type is `string \| undefined` |
| `readonly id: number` | Can be set when the object is created, never changed afterwards |
| `published_year: number \| null` | The API sends a number or `null`. The name uses `snake_case` because **the API** does; we copy it exactly |
| `Omit<Book, 'id' \| 'owner' \| 'created_at'>` | Everything in `Book` except those keys |
| `import type { … }` | The import exists only for the compiler and disappears at run time |
| `{ id: 4, ...dune, owner: …, created_at: … }` | Spread (Lab 2.2) builds a `Book` from a `BookData` |
| `Partial<BookData> = {}` | `overrides` may contain any subset; `{}` is the default |
| `{ …defaults, ...overrides }` | Later properties win: defaults first, overrides last |
| `interface YearCase` + `YearCase[]` | A typed list of test cases |
| `as const` | Freezes the object so `200` is the exact value `200`, not just "a number" |
| `keyof typeof STATUS` | The union of the object's keys: `'OK' \| 'CREATED' \| …` |
| `type Role = 'owner' \| 'visitor' \| 'staff'` | A literal union (Lab 2.1) |
| `canEdit(book, who)` | The same rule the application applies: only the owner sees Edit/Delete |

### Try it: real compiler errors

| You write | Real compiler output | Meaning |
|---|---|---|
| `const u: TestUser = { username: 'a' }` | `error TS2741: Property 'password' is missing in type '{ username: string; }' but required in type 'TestUser'.` | A required field is missing |
| `{ username: 'a', password: 'b', nickname: 'x' }` typed as `TestUser` | `error TS2353: Object literal may only specify known properties, and 'nickname' does not exist in type 'TestUser'.` | Unknown (probably misspelled) field |
| `stored.id = 5` | `error TS2540: Cannot assign to 'id' because it is a read-only property.` | `readonly` protects it |
| `makeBook({ colour: 'red' })` | `error TS2353: Object literal may only specify known properties, and 'colour' does not exist in type 'Partial<BookData>'.` | `Partial` still forbids unknown fields |

### Common mistakes

* Writing an interface **and** forgetting to use it (`const user = { … }` with no `: TestUser`) — the safety is only there when you attach the type.
* Making everything optional "to get rid of errors". That removes the protection. Mark a field optional only if it truly may be missing.
* Using `any`. It switches the checks off. If you do not know the type, use `unknown` and check (Lab 2.1).
* Confusing `?` (optional property) with `| null` (the property is present but empty): `published_year: number | null` is **always there**.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `TS2307: Cannot find module '../utils/types'` | Wrong path or file not saved | Paths are relative to the **current file**; `..` goes up one folder |
| `TS2741 … is missing` | Required field absent | Add it, or make it optional if appropriate |
| Interface changes and many files turn red | That is the feature working | Fix each place; it shows everything affected |

### ✍️ Independent exercise

1. Add `interface SearchCase { name: string; searchText: string; expectedTitles: string[] }` and a typed list of two search cases for the books in Lab 2.2 (`'austen'` → `Emma`, `Persuasion`; `'DUNE'` → `Dune`).
2. Add `export interface ApiErrorBody { detail: string }` to `utils/types.ts`.
3. Create the type `type NewUser = Pick<TestUser, 'username' | 'password'>` and a variable of that type. (`Pick` is the opposite of `Omit`.)

<details><summary>Answer</summary>

```ts
interface SearchCase { name: string; searchText: string; expectedTitles: string[] }
const searchCases: SearchCase[] = [
  { name: 'by author, any case', searchText: 'austen', expectedTitles: ['Emma', 'Persuasion'] },
  { name: 'by title, capitals', searchText: 'DUNE', expectedTitles: ['Dune'] },
];

// utils/types.ts
export interface ApiErrorBody { detail: string }

type NewUser = Pick<TestUser, 'username' | 'password'>;
const nu: NewUser = { username: 'qa_new', password: 'S3cure-Lab-Passw0rd!' };
```
</details>

### Knowledge check (Lab 2.4)

1. What does `?` after a property name mean? *(Optional.)*
2. What does `Omit<Book, 'id'>` produce? *(Book without `id`.)*
3. When do you choose `type` over `interface`? *(Unions, shortcuts, derived shapes.)*
4. Why is `any` discouraged? *(It turns off checking.)*

### Completion checklist

- [ ] `utils/types.ts` exists and `05-types.ts` runs.
- [ ] I produced the `TS2741`, `TS2353` and `TS2540` errors on purpose and fixed them.
- [ ] I solved the three-part exercise.
- [ ] I can explain `Omit`, `Partial` and `readonly` with a Book Library example.

---

## Lab 2.5 — Classes, objects and access modifiers 🧭 + ✍️

### Learning objectives

* Define a class with properties, a constructor and methods.
* Use `public`, `private`, `protected` and `readonly`.
* Create objects (instances) with `new`; use getters and `static` members.
* Use inheritance (`extends`, `super`, `override`).
* Recognise the shape of a **Page Object** (built for real in Phase 3 and Phase 5).

### Concepts in simple language

A **class** is a blueprint; an **object** (or *instance*) is one thing built from it with `new`. A class bundles **data** (properties) and **actions** (methods).

Think of a vending machine: you press buttons (**public** methods), but the coins box and the stock (**private** data) are locked inside. Giving outsiders only the buttons means nobody can reach in and break the machine.

| Modifier | Who can use it |
|---|---|
| `public` (default) | Anyone |
| `protected` | The class and classes that `extend` it |
| `private` | Only this class |
| `readonly` | Can be set once (in the constructor), never reassigned |

### Why QA needs it

A **Page Object** is a class that knows *one page*: which fields and buttons it has (`private`, so tests do not depend on them) and what a user can do (`public` methods like `login(...)`). When the page's HTML changes, you fix **one class** instead of 50 tests. This lab uses a small in-memory catalogue so you learn the syntax without a browser.

### Prerequisites

Labs 2.3 and 2.4 complete.

### Files

`practice/06-classes.ts`

### Step-by-step

Create `practice/06-classes.ts`, type it and run `npx tsx practice/06-classes.ts` then `npm run typecheck`.

*File: `e2e/practice/06-classes.ts`*

```ts
// Lab 2.5 - classes and access modifiers
import type { Book, BookData } from '../utils/types';

// A class bundles DATA (properties) and ACTIONS (methods).
// This one is a tiny in-memory model of the Book Library's list, search and delete rules.
class BookCatalog {
  // protected: this class and its children can use it, outsiders cannot.
  protected books: Book[] = [];
  private nextId = 1; // private: only this class can touch it

  // "Parameter properties": writing an access modifier in the constructor
  // declares AND fills the property in one go.
  constructor(
    public readonly name: string, // public = usable from anywhere; readonly = never reassigned
    private readonly owner: string,
  ) {}

  add(data: BookData): Book {
    const book: Book = {
      id: this.nextId++,
      ...data,
      owner: this.owner,
      created_at: new Date().toISOString(),
    };
    this.books.push(book);
    return book;
  }

  // Same rule as the page: title OR author, ignoring capitals, matching part of a word.
  search(text: string): Book[] {
    const needle = text.trim().toLowerCase();
    return this.books.filter(
      (b) => b.title.toLowerCase().includes(needle) || b.author.toLowerCase().includes(needle),
    );
  }

  remove(id: number): boolean {
    const before = this.books.length;
    this.books = this.books.filter((b) => b.id !== id);
    return this.books.length < before;
  }

  // A getter looks like a property when you use it: catalog.count
  get count(): number {
    return this.books.length;
  }

  // static: belongs to the class itself, not to one object.
  static withTitles(name: string, owner: string, titles: string[]): BookCatalog {
    const catalog = new BookCatalog(name, owner);
    for (const title of titles) catalog.add({ title, author: 'Unknown', published_year: null });
    return catalog;
  }
}

const library = new BookCatalog('Anna\'s books', 'anna'); // "new" creates an object (an instance)
library.add({ title: 'Dune', author: 'Frank Herbert', published_year: 1965 });
library.add({ title: 'Emma', author: 'Jane Austen', published_year: 1815 });
library.add({ title: 'Persuasion', author: 'Jane Austen', published_year: 1817 });

console.log(library.name, '->', library.count, 'books');
console.log('search "AUSTEN":', library.search('AUSTEN').map((b) => b.title));
console.log('search "zzz":', library.search('zzz').length, 'results');
console.log('remove 1:', library.remove(1), '| remove 99:', library.remove(99), '| count now', library.count);

// library.books;           // <- compile error: 'books' is protected
// library.nextId = 10;     // <- compile error: 'nextId' is private
// library.name = 'x';      // <- compile error: 'name' is read-only

// Inheritance: a class can extend another and add or change behaviour.
class LoggedCatalog extends BookCatalog {
  override add(data: BookData): Book {
    const book = super.add(data); // run the parent's version first
    console.log(`  [log] added #${book.id} "${book.title}" (now ${this.books.length} books)`);
    return book;
  }
}
const logged = new LoggedCatalog('Logged', 'bob');
logged.add({ title: 'Kindred', author: 'Octavia Butler', published_year: 1979 });
console.log(BookCatalog.withTitles('Quick', 'zoe', ['A', 'B', 'C']).count, 'books from a static helper');

// ---------------------------------------------------------------------------
// A preview of Phase 5: a "page object" is a class that knows ONE page.
// (Here it only describes steps as text - in Phase 3 the steps become real browser actions.)
class LoginPageSketch {
  private readonly usernameLabel = 'Username';
  private readonly passwordLabel = 'Password';
  private readonly buttonName = 'Sign in';

  constructor(private readonly url: string) {}

  loginSteps(username: string): string[] {
    return [
      `open ${this.url}`,
      `fill the "${this.usernameLabel}" box with ${username}`,
      `fill the "${this.passwordLabel}" box with ********`,
      `click the "${this.buttonName}" button`,
    ];
  }
}
new LoginPageSketch('http://localhost:8000/login/').loginSteps('qa_anna').forEach((s) => console.log(' -', s));
```

### Expected output

The timestamp is not printed, so your output must match exactly.

```text
Anna's books -> 3 books
search "AUSTEN": [ 'Emma', 'Persuasion' ]
search "zzz": 0 results
remove 1: true | remove 99: false | count now 2
  [log] added #1 "Kindred" (now 1 books)
3 books from a static helper
 - open http://localhost:8000/login/
 - fill the "Username" box with qa_anna
 - fill the "Password" box with ********
 - click the "Sign in" button
```

### Line-by-line explanation

| Code | Explanation |
|---|---|
| `class BookCatalog { … }` | The blueprint |
| `protected books: Book[] = []` | The data; children may use it, outsiders may not |
| `private nextId = 1` | An internal counter nobody else may touch |
| `constructor(public readonly name: string, private readonly owner: string) {}` | **Parameter properties**: the modifier in the constructor declares *and* fills the property — one line instead of four |
| `add(data: BookData): Book` | A method; returns the stored book with its new `id` |
| `this.nextId++` | `this` = "this object"; `++` adds 1 **after** using the value |
| `search(text)` | The same rule as the Books page: title or author, ignoring capitals, part of a word |
| `remove(id)` returns `boolean` | `true` if something was removed |
| `get count()` | A getter: used as `library.count` (no brackets) |
| `static withTitles(...)` | Belongs to the class: `BookCatalog.withTitles(...)`; no object needed |
| `new BookCatalog('Anna\'s books', 'anna')` | Creates an object. `\'` is an apostrophe inside single quotes |
| `class LoggedCatalog extends BookCatalog` | A child class: it inherits everything and may change parts |
| `override add(...)` + `super.add(data)` | Replace a method but still call the parent's version |
| `class LoginPageSketch` | A preview of a Page Object: `private` selectors, a `public` action |

### Try it: real compiler errors

Uncomment the three lines in the file (one at a time) or add them yourself.

| You write | Real compiler output | Meaning |
|---|---|---|
| `library.books` | `error TS2445: Property 'books' is protected and only accessible within class 'BookCatalog' and its subclasses.` | Locked for outsiders |
| `library.nextId = 10` | `error TS2341: Property 'nextId' is private and only accessible within class 'BookCatalog'.` | Locked for everyone but the class |
| `library.name = 'x'` | `error TS2540: Cannot assign to 'name' because it is a read-only property.` | Set once in the constructor |

### Common mistakes

* Forgetting `this.` inside a method: `books` alone is "not found"; write `this.books`.
* Forgetting `new`: `BookCatalog('x', 'y')` is an error; write `new BookCatalog('x', 'y')`.
* Making everything `public`. Hide what tests should not depend on (selectors, internal state).
* Using inheritance when two small classes would do. Prefer **composition** ("has a") over deep "is a" chains; Phase 5 returns to this.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `TS2445` / `TS2341` | Reaching into a locked property | Add a public method or getter instead |
| `Cannot read properties of undefined` inside a method | A callback lost `this` | Use an arrow function inside methods, as `search` does |
| `TS2416` … `Property 'add' in type … is not assignable to the same property in base type` | The child's method has a different signature than the parent's | Keep the same parameters and return type |

### ✍️ Independent exercise

1. Add a method `findById(id: number): Book | undefined` to `BookCatalog` and print the result for an existing and a missing id.
2. Add a getter `titles` that returns `string[]` of all titles.
3. Create `class ReadOnlyCatalog extends BookCatalog` whose `add` method **throws** `new Error('read only')`. Show that calling it fails.
4. Sketch `class BookFormSketch` with a `private` constructor parameter `url`, and a `public` method `fillSteps(title: string, author: string): string[]` that returns the text steps for filling the Add-book form.

<details><summary>Answer</summary>

```ts
// inside BookCatalog:
findById(id: number): Book | undefined {
  return this.books.find((b) => b.id === id);
}
get titles(): string[] {
  return this.books.map((b) => b.title);
}

class ReadOnlyCatalog extends BookCatalog {
  override add(_data: BookData): Book {
    throw new Error('read only');
  }
}
try { new ReadOnlyCatalog('ro', 'zoe').add({ title: 'x', author: 'y', published_year: null }); }
catch (e) { console.log((e as Error).message); } // read only

class BookFormSketch {
  constructor(private readonly url: string) {}
  fillSteps(title: string, author: string): string[] {
    return [`open ${this.url}`, `type "${title}" into Title`, `type "${author}" into Author`, 'click Add book'];
  }
}
```
</details>

### Knowledge check (Lab 2.5)

1. Which modifier lets child classes but not outsiders use a property? *(`protected`.)*
2. What does `constructor(private readonly url: string) {}` do? *(Declares a private read-only property `url` and stores the argument in it.)*
3. What is a static method? *(One that belongs to the class, called without an object.)*
4. Why do Page Objects keep selectors private? *(So tests depend on actions, not on page details.)*

### Completion checklist

- [ ] `06-classes.ts` runs; the output matches.
- [ ] I produced `TS2445`, `TS2341` and `TS2540` on purpose.
- [ ] I solved the four-part exercise.
- [ ] I can explain `public`, `private`, `protected`, `readonly`, `static`, and `extends`.

---

## Lab 2.6 — Imports and exports between files 🧭 + ✍️

### Learning objectives

* Export values, functions and types from one file and import them in another.
* Use named imports, renaming (`as`), namespace imports (`import * as`) and `import type`.
* Create the three shared helper files used in every later phase: `book-rules.ts`, `test-data.ts`, `env.ts`.
* Read configuration from environment variables in **one** place.

### Concepts in simple language

One huge file is unreadable. **Modules** split code into files; each file decides what it **exports** (shares) and other files **import** what they need. Everything not exported stays private to the file.

```
utils/book-rules.ts   export const MAX_TITLE_LENGTH …   ← shares
practice/07-modules.ts  import { MAX_TITLE_LENGTH } from '../utils/book-rules'   ← uses
```

**Paths:** `./x` = same folder, `../x` = one folder up. Leave out the `.ts` ending.

### Why QA needs it

Your future framework is nothing but modules: page objects, fixtures, data builders, configuration. If the maximum title length changes from 200 to 250, you edit **one line** in `book-rules.ts` and every test follows. Reading the base URL from the environment lets the same tests run on your laptop and in CI.

### Prerequisites

Labs 2.4 and 2.5 complete (`utils/types.ts` exists).

### Files

```
utils/book-rules.ts   the input rules, exported
utils/test-data.ts    uid(), uniqueUsername(), makeBook()
utils/env.ts          configuration from environment variables
practice/07-modules.ts  the file that imports them all
```

### Step-by-step

**Step 1.** Create `utils/book-rules.ts` (the rules from Lab 2.3, completed and exported):

*File: `e2e/utils/book-rules.ts`*

```ts
// The Book Library's input rules, written once and exported for every test to reuse.

export const MAX_TITLE_LENGTH = 200;
export const MAX_AUTHOR_LENGTH = 120;
export const MIN_YEAR = 1000;
export const MAX_YEAR = 2100;

/** What a person types into the "Add book" form (everything is text at first). */
export interface BookForm {
  title: string;
  author: string;
  year: string;
}

export function titleError(title: string): string | null {
  const trimmed = title.trim();
  if (trimmed === '') return 'Title is required.';
  if (trimmed.length > MAX_TITLE_LENGTH) return `Title must have at most ${MAX_TITLE_LENGTH} characters.`;
  return null;
}

export function authorError(author: string): string | null {
  const trimmed = author.trim();
  if (trimmed === '') return 'Author is required.';
  if (trimmed.length > MAX_AUTHOR_LENGTH) return `Author must have at most ${MAX_AUTHOR_LENGTH} characters.`;
  return null;
}

export function yearError(text: string): string | null {
  const trimmed = text.trim();
  if (trimmed === '') return null; // the year is optional
  if (!/^\d+$/.test(trimmed)) return 'Year must be a whole number.';
  const year = Number(trimmed);
  if (year < MIN_YEAR || year > MAX_YEAR) return `Year must be between ${MIN_YEAR} and ${MAX_YEAR}.`;
  return null;
}

/** All problems with a form, in the order the page would show them. Empty array = valid. */
export function validateBookForm(form: BookForm): string[] {
  return [titleError(form.title), authorError(form.author), yearError(form.year)].filter(
    (message): message is string => message !== null, // keep only the real messages
  );
}
```

**Step 2.** Create `utils/test-data.ts`:

*File: `e2e/utils/test-data.ts`*

```ts
import { randomBytes } from 'node:crypto';
import type { BookData } from './types';

/** Short random text such as "3fa9c2d1". Makes every run's data unique. */
export function uid(): string {
  return randomBytes(4).toString('hex');
}

export function uniqueUsername(prefix = 'qa'): string {
  return `${prefix}_${uid()}`;
}

/**
 * Valid book data that is UNIQUE on every call (the token is in the title and the author),
 * so a test can search for exactly its own books. Pass overrides to change any field.
 */
export function makeBook(overrides: Partial<BookData> = {}): BookData {
  const token = uid();
  return {
    title: `PW Book ${token}`,
    author: `Author ${token}`,
    published_year: 1999,
    ...overrides,
  };
}
```

**Step 3.** Create `utils/env.ts`:

*File: `e2e/utils/env.ts`*

```ts
import { randomBytes } from 'node:crypto';

/**
 * ONE place that reads environment variables. Everything else imports `env`,
 * so configuration is never scattered through the tests.
 */
export const env = {
  // Where the application under test is running.
  baseUrl: process.env.BASE_URL ?? 'http://localhost:8000',

  // A password for the test users. Use the environment variable when it is set;
  // otherwise make a strong random one for this run. Nothing secret lives in the code.
  testUserPassword: process.env.TEST_USER_PASSWORD || `Pw-${randomBytes(9).toString('hex')}-Aa1!`,
};
```

**Step 4.** Create `practice/07-modules.ts` and run it:

*File: `e2e/practice/07-modules.ts`*

```ts
// Lab 2.6 - imports and exports
import { env } from '../utils/env'; // a named import: the braces pick one export
import { makeBook, uniqueUsername, uid as randomId } from '../utils/test-data'; // "as" renames on import
import * as rules from '../utils/book-rules'; // everything from a file, under one name
import { validateBookForm, MAX_TITLE_LENGTH } from '../utils/book-rules';
import type { BookData } from '../utils/types'; // "import type": exists only for the compiler

console.log('base URL      :', env.baseUrl);
console.log('password set? :', env.testUserPassword.length > 10, '(never print real passwords)');
console.log('random id     :', randomId());
console.log('user          :', uniqueUsername('anna'));

const book: BookData = makeBook({ published_year: 1984 });
console.log('book          :', book);

console.log('--- rules, imported as one object ---');
console.log('limits        :', rules.MAX_TITLE_LENGTH, rules.MAX_AUTHOR_LENGTH, rules.MIN_YEAR, rules.MAX_YEAR);
console.log('same constant :', MAX_TITLE_LENGTH === rules.MAX_TITLE_LENGTH);

console.log('--- validating forms ---');
const good = validateBookForm({ title: book.title, author: book.author, year: String(book.published_year) });
const empty = validateBookForm({ title: '', author: '  ', year: 'abc' });
console.log('good form  ->', good);
console.log('empty form ->', empty);
```

```powershell
npx tsx practice/07-modules.ts
npm run typecheck
```

### Expected output

Random values (`random id`, usernames, titles) differ on your computer.

```text
base URL      : http://localhost:8000
password set? : true (never print real passwords)
random id     : d3510ae7
user          : anna_8c6f7787
book          : {
  title: 'PW Book 3433c986',
  author: 'Author 3433c986',
  published_year: 1984
}
--- rules, imported as one object ---
limits        : 200 120 1000 2100
same constant : true
--- validating forms ---
good form  -> []
empty form -> [
  'Title is required.',
  'Author is required.',
  'Year must be a whole number.'
]
```

Now run it again pointing to another server — **no code changes**:

```powershell
$env:BASE_URL = "http://127.0.0.1:8000"
npx tsx practice/07-modules.ts
Remove-Item Env:BASE_URL
```

(macOS/Linux: `BASE_URL=http://127.0.0.1:8000 npx tsx practice/07-modules.ts`.) The first output line now shows the new address.

### Line-by-line explanation

| Code | Explanation |
|---|---|
| `export const MAX_TITLE_LENGTH = 200` | Shared constant; UPPER_CASE by convention |
| `export interface BookForm` | Types can be exported too |
| `export function titleError` | A shared function |
| `.filter((message): message is string => message !== null)` | A **type guard**: tells TypeScript that after the filter the array holds only `string`s, not `string \| null` |
| `import { env } from '../utils/env'` | Named import: braces pick one export by its exact name |
| `import { …, uid as randomId } …` | `as` renames, handy for name clashes |
| `import * as rules from '…'` | Everything the file exports, as one object: `rules.MIN_YEAR` |
| `import type { BookData } …` | Type-only; erased at run time |
| `process.env.BASE_URL ?? 'http://localhost:8000'` | Use the environment variable if it exists, else a default |
| `process.env.TEST_USER_PASSWORD \|\| \`Pw-…\`` | Here `\|\|` is intended: an **empty** variable also falls back |
| `randomBytes(9).toString('hex')` | A fresh strong password per run; **nothing secret is written in the code** |
| `makeBook(overrides)` | A *data builder*: valid unique data by default, change only what the test cares about |

### Try it: real compiler errors

| You write | Real compiler output | Meaning |
|---|---|---|
| `import { nothing } from '../utils/missing'` | `error TS2307: Cannot find module '../utils/missing' or its corresponding type declarations.` | Wrong file name or path |
| `env.baseUrl.toFixed()` | `error TS2551: Property 'toFixed' does not exist on type 'string'. Did you mean 'fixed'?` | You used a number method on text |
| `makeBook({ colour: 'red' })` | `error TS2353: … 'colour' does not exist in type 'Partial<BookData>'.` | A data builder only accepts real fields |
| Remove `export` before `titleError`, then import it | `error TS2459: Module '"../utils/book-rules"' declares 'titleError' locally, but it is not exported.` | You forgot `export` |

### Common mistakes

* Forgetting `export` — the name exists in the file but nobody else can import it.
* Wrong relative path (`./utils/…` when the file is one folder up).
* A **circular import** (A imports B and B imports A). Keep helpers one-directional: `types` ← `book-rules`/`test-data` ← tests.
* Putting a real password in the source code. Use environment variables or generated values; never commit secrets.
* Importing from `node_modules` names with a typo — the error is the same `TS2307`.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `TS2307` | Path or name wrong | Check spelling and `./` vs `../`; the editor can auto-complete the path |
| `ERR_MODULE_NOT_FOUND` when running | Same, found at run time | Same fix |
| `$env:BASE_URL` stays set in later labs | PowerShell remembers it for the window | `Remove-Item Env:BASE_URL` |
| Two files import each other and values are `undefined` | Circular import | Move the shared piece to a third file |

### ✍️ Independent exercise

1. Create `utils/format.ts` that exports `function bookLabel(book: BookData): string` returning `Dune (1965)` or `Dune (no year)`; import and use it from a new file `practice/07b-exercise.ts`.
2. Decide where the `STATUS` constants from Lab 2.4 belong if many files need them. Move them into a new file `utils/http.ts`, export them, and import them from `05-types.ts`. Add a one-line comment explaining your choice.
3. In `env.ts`, add `headless: process.env.HEADED !== '1'` and print it from `07-modules.ts`.

<details><summary>Answer</summary>

```ts
// utils/format.ts
import type { BookData } from './types';
export function bookLabel(book: BookData): string {
  return book.published_year === null ? `${book.title} (no year)` : `${book.title} (${book.published_year})`;
}
// practice/07b-exercise.ts
import { bookLabel } from '../utils/format';
console.log(bookLabel({ title: 'Dune', author: 'Frank Herbert', published_year: 1965 }));
```

`types.ts` should hold **shapes** only (they disappear at run time); constants with values belong in a separate `utils/http.ts`. In `env.ts`: `headless: process.env.HEADED !== '1',` — set `HEADED=1` to see the browser later (Phase 3).
</details>

### Knowledge check (Lab 2.6)

1. What decides whether another file can use a name? *(Whether it is `export`ed.)*
2. What is the difference between `import { a }` and `import * as x`? *(Pick one export vs take them all under one name.)*
3. What does `import type` do? *(Imports only for the compiler; erased when the program runs.)*
4. Why read `BASE_URL` in one file? *(One place to change; same tests run anywhere.)*

### Completion checklist

- [ ] `book-rules.ts`, `test-data.ts`, `env.ts` and `07-modules.ts` exist; `npm run typecheck` is silent.
- [ ] I ran `07-modules.ts` with and without `BASE_URL`.
- [ ] I solved the exercise.
- [ ] I can explain `export`, named import, `as`, `import * as` and `import type`.


---

## Lab 2.7 — Promises, `async`/`await` and exception handling 🧭 + ✍️

### Learning objectives

* Explain what a **Promise** is and why browsers and networks need it.
* Write and call `async` functions with `await`; know what happens when `await` is forgotten.
* Run independent steps together with `Promise.all`.
* Handle failures with `try` / `catch` / `finally` and a custom error class.
* Call the Book Library API with `fetch` and read status, headers and body.

### Concepts in simple language

Some things take time: loading a page, waiting for the server's answer, a button becoming clickable. A program must not freeze while it waits, so such functions return a **Promise** — an IOU: *"I do not have the answer yet; I will hand it over later, or tell you it failed."*

* `async` before a function means "this function returns a Promise".
* `await` in front of a Promise means "pause **this function** here until the IOU is paid; give me the value".

```ts
const response = await fetch(url);   // wait for the server to answer
const body = await response.json();  // wait for the body to be read
```

**The golden rule for Playwright: every action that touches the browser or the network needs `await`.** Without it, the next line runs before the previous step has finished.

**Errors:** a failed step *throws*. `try { … } catch (error) { … } finally { … }` lets you handle it: `catch` runs on failure, `finally` always runs (clean-up).

### Why QA needs it

All of Playwright is `async`: `await page.goto(…)`, `await page.getByRole(…).click()`, `await expect(…)`. A forgotten `await` produces the nastiest kind of test: it passes sometimes and fails sometimes ("flaky"). Understanding this lab prevents most beginner flakiness. API calls (Phase 6) use exactly the `fetch`-like pattern shown here.

### Prerequisites

* Lab 2.6 complete (`utils/env.ts`).
* **The application running** for Part 3: `python manage.py runserver 127.0.0.1:8000` in the application folder, with at least the supplied sample data.

### Files

`practice/08-async.ts`

### Step-by-step

Create `practice/08-async.ts`, type it (take your time — it is the longest file so far) and run:

```powershell
npx tsx practice/08-async.ts
npm run typecheck
```

*File: `e2e/practice/08-async.ts`*

```ts
// Lab 2.7 - promises, async/await, errors, and a first look at the real API
import { env } from '../utils/env';

// ---------------------------------------------------------------------------
// Part 1 - Promises you can feel: a function that "finishes later"
// ---------------------------------------------------------------------------
function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms)); // resolve() = "I am done now"
}

async function slowAnswer(label: string, ms: number): Promise<string> {
  await sleep(ms); // "wait here until the promise is finished" - the program is NOT frozen
  return `${label} (took ${ms} ms)`;
}

function roughly(ms: number): number {
  return Math.round(ms / 100) * 100; // timings differ a little on every computer
}

async function promiseDemo(): Promise<void> {
  console.log('--- Part 1: promises ---');

  // The older style, with .then(): fine to recognise, rarely needed any more.
  await slowAnswer('old style', 50).then((text) => console.log('  .then ->', text));

  // The modern style: await.
  const text = await slowAnswer('await style', 50);
  console.log('  await ->', text);

  // One after the other: the times add up.
  let start = Date.now();
  await slowAnswer('A', 300);
  await slowAnswer('B', 300);
  await slowAnswer('C', 300);
  console.log(`  one after another: about ${roughly(Date.now() - start)} ms`);

  // All at the same time (only when the steps do not depend on each other).
  start = Date.now();
  const results = await Promise.all([slowAnswer('A', 300), slowAnswer('B', 300), slowAnswer('C', 300)]);
  console.log(`  Promise.all:       about ${roughly(Date.now() - start)} ms ->`, results.length, 'results');
}

// ---------------------------------------------------------------------------
// Part 2 - Errors: throw, try / catch / finally, your own error type
// ---------------------------------------------------------------------------
class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly url: string,
    message: string,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function mayFail(shouldFail: boolean): Promise<string> {
  await sleep(10);
  if (shouldFail) throw new Error('Something went wrong');
  return 'worked';
}

async function errorDemo(): Promise<void> {
  console.log('--- Part 2: errors ---');
  for (const shouldFail of [false, true]) {
    try {
      console.log('  result:', await mayFail(shouldFail));
    } catch (error) {
      // In TypeScript the caught value is `unknown`, so check what it is first.
      const message = error instanceof Error ? error.message : String(error);
      console.log('  caught:', message);
    } finally {
      console.log('  (finally always runs - good for cleanup)');
    }
  }
}

// ---------------------------------------------------------------------------
// Part 3 - The real thing: talking to the Book Library API with fetch
// ---------------------------------------------------------------------------
interface HealthReply {
  status: string;
}
interface BookRow {
  id: number;
  title: string;
  author: string;
}

// <T> is a placeholder: "the caller tells me what type the JSON has".
async function getJson<T>(path: string): Promise<T> {
  const url = `${env.baseUrl}${path}`;
  const response = await fetch(url); // 1) wait for the response headers
  if (!response.ok) {
    throw new ApiError(response.status, url, `GET ${path} answered ${response.status}`);
  }
  return (await response.json()) as T; // 2) wait for the body to be read and parsed
}

async function apiDemo(): Promise<void> {
  console.log('--- Part 3: the real API ---');

  const health = await getJson<HealthReply>('/api/health/');
  console.log('  health   :', health);

  const books = await getJson<BookRow[]>('/api/books/');
  console.log('  books    :', books.length, 'in the library', books.length > 0 ? `(first: "${books[0].title}")` : '');

  // A failure we EXPECT: handle it instead of crashing.
  try {
    await getJson('/api/books/999999999/');
  } catch (error) {
    if (error instanceof ApiError) console.log(`  expected : ${error.message} (status ${error.status})`);
    else throw error; // not ours - do not hide it
  }

  // Looking at status, headers and body directly:
  const response = await fetch(`${env.baseUrl}/api/me/`);
  console.log('  /api/me/ :', response.status, '| WWW-Authenticate =', response.headers.get('www-authenticate'));
  console.log('             body =', await response.json());

  // A write WITHOUT a CSRF token is refused. (Lab 1.6: unsafe requests need the token.)
  const refused = await fetch(`${env.baseUrl}/api/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'nobody', password: 'S3cure-Lab-Passw0rd!' }),
  });
  console.log('  register without token:', refused.status, await refused.json());
}

// ---------------------------------------------------------------------------
async function main(): Promise<void> {
  await promiseDemo();
  await errorDemo();
  await apiDemo();
}

main().catch((error: unknown) => {
  // Top-level safety net: print a helpful message, set a failing exit code.
  const reason = error instanceof Error && error.cause instanceof Error ? error.cause.message : String(error);
  console.error(`\nFAILED: ${reason}`);
  console.error(`Is the application running at ${env.baseUrl}? (python manage.py runserver)`);
  process.exitCode = 1;
});
```

### Expected output

Timings are approximate (they differ slightly on every computer); the book count and first title depend on your data.

```text
--- Part 1: promises ---
  .then -> old style (took 50 ms)
  await -> await style (took 50 ms)
  one after another: about 900 ms
  Promise.all:       about 300 ms -> 3 results
--- Part 2: errors ---
  result: worked
  (finally always runs - good for cleanup)
  caught: Something went wrong
  (finally always runs - good for cleanup)
--- Part 3: the real API ---
  health   : { status: 'ok' }
  books    : 1 in the library (first: "Dune")
  expected : GET /api/books/999999999/ answered 404 (status 404)
  /api/me/ : 401 | WWW-Authenticate = Session
             body = { detail: 'Authentication credentials were not provided.' }
  register without token: 403 { detail: 'CSRF Failed: CSRF cookie not set.' }
```

Stop the application and run the file again. You should see a friendly failure message and exit code 1 (the `main().catch` safety net at the bottom of the file):

```text
FAILED: connect ECONNREFUSED 127.0.0.1:8000
Is the application running at http://localhost:8000? (python manage.py runserver)
```

### Line-by-line explanation

| Code | Explanation |
|---|---|
| `function sleep(ms): Promise<void>` | Returns a Promise that is paid after `ms` milliseconds; `void` = no value inside |
| `new Promise((resolve) => setTimeout(resolve, ms))` | `resolve()` means "I am done" |
| `async function slowAnswer(...): Promise<string>` | An async function always returns a Promise; the `string` is what it will contain |
| `await sleep(ms)` | Pause here, not the whole program |
| `.then((text) => …)` | The older way; you will see it in other people's code |
| 3 × `await slowAnswer(…, 300)` ≈ **900 ms** | One after another: times add up |
| `await Promise.all([…])` ≈ **300 ms** | All at once; result is an array in the same order. Use only for independent steps |
| `class ApiError extends Error` | Your own error type with extra data (`status`, `url`) |
| `catch (error)` → `error instanceof Error` | In TypeScript a caught value is `unknown`; check before using `.message` |
| `finally { … }` | Runs after success **and** after failure |
| `getJson<T>(path): Promise<T>` | `<T>` is a **generic**: the caller says what type the JSON has |
| `if (!response.ok) throw new ApiError(…)` | `ok` is true for status 200–299 |
| `(await response.json()) as T` | "Trust me, this is a `T`" — a promise to the compiler, not proof (Lab 2.8 adds a real check) |
| `error instanceof ApiError … else throw error` | Handle **expected** errors; re-throw anything unexpected |
| `response.headers.get('www-authenticate')` | Read one response header (`null` if absent) |
| register **without** a CSRF token → `403` | Lab 1.6: unsafe requests must carry the token |
| `main().catch(…)` + `process.exitCode = 1` | A top-level safety net: prints a helpful message and tells the shell "this failed" |

### Try it: what a forgotten `await` really does

Add these lines to a scratch file (`practice/scratch.ts`) and run it:

```ts
async function one(): Promise<number> { return 1; }
async function demo(): Promise<void> {
  const n = one();            // forgot await
  console.log('n is', n);     // n is Promise { 1 }
  console.log(`${n}1`);       // [object Promise]1
}
demo();
```

Real output:

```text
n is Promise { 1 }
[object Promise]1
```

And the compiler catches the common ones:

| You write | Real compiler output | Meaning |
|---|---|---|
| `const response = fetch(url); response.status` | `error TS2339: Property 'status' does not exist on type 'Promise<Response>'.` | You hold the IOU, not the response — add `await` |
| `const n = one(); n + 1` | `error TS2365: Operator '+' cannot be applied to types 'Promise<number>' and 'number'.` | Same cause |
| `await` at the top of a file | `error TS1309: The current file is a CommonJS module and cannot use 'await' at the top level.` (and `tsx`: `Top-level await is currently not supported with the "cjs" output format`) | Put it in `async function main()` and call `main()` |
| A promise that fails and nobody `catch`es it | The program crashes, printing `Error: boom` and a stack trace (exit code 1) | Add `try/catch`, or `.catch()` on `main()` |

### Common mistakes

* **Forgetting `await`** (above). In Playwright this is the single most common beginner error.
* **`await` inside `forEach`** — `forEach` does not wait. Use `for (const x of list) { await … }` or `Promise.all(list.map(…))`.
* **Swallowing errors** — `catch (e) {}` with an empty body hides the real problem. Print, re-throw, or fail.
* **Using `Promise.all` for steps that depend on each other** (create a book, *then* delete it) — they must be sequential.
* **Marking a function `async` but never using `await`** — harmless but misleading.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `fetch failed` / `ECONNREFUSED` | The application is not running (or wrong port) | Start it; check `BASE_URL` |
| Output stops after a line, no error | A rejected Promise nobody awaited | Make sure the call is `await`ed and the chain ends in `.catch` |
| `TS2339 … on type 'Promise<…>'` | Missing `await` | Add it |
| `register without token: 403` is expected | CSRF protection works | This is the *correct* result in this lab |
| `SyntaxError: Cannot use import statement` | Running `.ts` with plain `node` | Use `npx tsx` |

### ✍️ Independent exercise

1. Write `async function countBooks(): Promise<number>` using `getJson<BookRow[]>('/api/books/')`. Print the count.
2. Fetch `/api/health/`, `/api/books/` and `/api/me/` **at the same time** with `Promise.all` and print the three status codes. (`/api/me/` answers 401 for an anonymous caller; that is fine because you read `status`, not `.ok`.)
3. Write `async function expectStatus(path: string, expected: number): Promise<void>` that throws an error `GET <path>: expected <n> but got <m>` when the status differs, and call it three times inside `try/catch`, printing `ok` or the error message.

<details><summary>Answer</summary>

```ts
async function countBooks(): Promise<number> {
  const books = await getJson<BookRow[]>('/api/books/');
  return books.length;
}
countBooks().then((n) => console.log('books:', n));

async function statuses(): Promise<void> {
  const paths = ['/api/health/', '/api/books/', '/api/me/'];
  const responses = await Promise.all(paths.map((p) => fetch(`${env.baseUrl}${p}`)));
  console.log(responses.map((r) => r.status)); // [ 200, 200, 401 ]
}
statuses();

async function expectStatus(path: string, expected: number): Promise<void> {
  const res = await fetch(`${env.baseUrl}${path}`);
  if (res.status !== expected) throw new Error(`GET ${path}: expected ${expected} but got ${res.status}`);
}
for (const [path, code] of [['/api/health/', 200], ['/api/me/', 401], ['/api/books/999999999/', 200]] as const) {
  try { await expectStatus(path, code); console.log('ok', path); }
  catch (e) { console.log((e as Error).message); }   // last one prints: expected 200 but got 404
}
```
(Put the loop inside an `async function main()`; top-level `await` is not allowed in this project.)
</details>

### Knowledge check (Lab 2.7)

1. What does `async` do to a function? *(Makes it return a Promise.)*
2. What does `await` do? *(Pauses that function until the Promise has a value or fails.)*
3. What is wrong with `const r = fetch(url); console.log(r.status)`? *(Missing `await`.)*
4. When is `Promise.all` appropriate? *(When steps are independent.)*
5. What does `finally` do? *(Runs after success or failure — clean-up.)*

### Completion checklist

- [ ] `08-async.ts` runs against the live app; I saw the 900 ms vs 300 ms difference.
- [ ] I saw the failure message with the application stopped.
- [ ] I reproduced `n is Promise { 1 }` and the `TS2339` error.
- [ ] I solved the three-part exercise.
- [ ] I can explain Promise, `async`, `await`, `try/catch/finally` to a colleague.

---

## Lab 2.8 — Working with JSON test data 🧭 + ✍️

### Learning objectives

* Read and write JSON; know how it differs from a TypeScript object.
* Keep test data in `.json` files, separate from code.
* Load JSON two ways (`import` and `readFileSync`) and understand the typing risk.
* Check data at run time with a **type guard**.
* Drive many checks from one data file (**data-driven** testing) and report a non-zero exit code on failure.

### Concepts in simple language

**JSON** is plain text for structured data: objects `{}`, arrays `[]`, text in **double** quotes, numbers, `true`/`false`, `null`. No comments, no trailing commas. It looks like a TypeScript object but is only *text* until parsed (`JSON.parse`) — and any text can be put in a `.json` file, including nonsense.

**Data-driven testing:** write the check once, put the cases in a table. Adding a case = adding a line of data, not code. This is how testers cover many boundaries cheaply (the table from Lab 1.1).

### Why QA needs it

* Test data is easier to read, review and extend in a data file; non-programmers can add cases.
* API requests and responses **are** JSON (Lab 1.6), so you handle it daily.
* `as SomeType` on parsed JSON is a promise, not a proof. Knowing the risk — and the guard that closes it — separates reliable tests from tests that fail with confusing messages.

### Prerequisites

Lab 2.7 complete; `utils/book-rules.ts` exists.

### Files

```
data/year-cases.json        nine year inputs with the expected message
data/book-form-cases.json   five whole-form cases
practice/09-json-data.ts    loads both, checks them, reports
```

### Step-by-step

**Step 1.** Create `data/year-cases.json`:

*File: `e2e/data/year-cases.json`*

```json
[
  { "name": "lowest valid year",       "input": "1000", "expected": null },
  { "name": "highest valid year",      "input": "2100", "expected": null },
  { "name": "just below the range",    "input": "999",  "expected": "Year must be between 1000 and 2100." },
  { "name": "just above the range",    "input": "2101", "expected": "Year must be between 1000 and 2100." },
  { "name": "empty is allowed",        "input": "",     "expected": null },
  { "name": "spaces only are allowed", "input": "   ",  "expected": null },
  { "name": "letters",                 "input": "abc",  "expected": "Year must be a whole number." },
  { "name": "decimal number",          "input": "19.5", "expected": "Year must be a whole number." },
  { "name": "negative number",         "input": "-5",   "expected": "Year must be a whole number." }
]
```

**Step 2.** Create `data/book-form-cases.json`:

*File: `e2e/data/book-form-cases.json`*

```json
[
  {
    "name": "valid book",
    "form": { "title": "Dune", "author": "Frank Herbert", "year": "1965" },
    "expectedErrors": []
  },
  {
    "name": "valid book without a year",
    "form": { "title": "Dune", "author": "Frank Herbert", "year": "" },
    "expectedErrors": []
  },
  {
    "name": "empty form",
    "form": { "title": "", "author": "", "year": "" },
    "expectedErrors": ["Title is required.", "Author is required."]
  },
  {
    "name": "title with spaces only",
    "form": { "title": "   ", "author": "Frank Herbert", "year": "1965" },
    "expectedErrors": ["Title is required."]
  },
  {
    "name": "everything wrong at once",
    "form": { "title": "", "author": "", "year": "abc" },
    "expectedErrors": ["Title is required.", "Author is required.", "Year must be a whole number."]
  }
]
```

**Step 3.** Create `practice/09-json-data.ts`:

*File: `e2e/practice/09-json-data.ts`*

```ts
// Lab 2.8 - JSON test data and a tiny hand-made test runner
import { readFileSync } from 'node:fs';
import { yearError, validateBookForm, type BookForm, MAX_TITLE_LENGTH } from '../utils/book-rules';
import yearCasesFile from '../data/year-cases.json'; // allowed by "resolveJsonModule" in tsconfig.json

// ---------------------------------------------------------------------------
// 1) The shape we EXPECT the data to have
// ---------------------------------------------------------------------------
interface YearCase {
  name: string;
  input: string;
  expected: string | null; // the error message, or null when the year is fine
}
interface FormCase {
  name: string;
  form: BookForm;
  expectedErrors: string[];
}

// ---------------------------------------------------------------------------
// 2) Two ways to load JSON
// ---------------------------------------------------------------------------
const yearCases: YearCase[] = yearCasesFile; // (a) import: TypeScript checks the shape for us

const formCases = JSON.parse( // (b) read the file at run time: the result is untyped...
  readFileSync(`${__dirname}/../data/book-form-cases.json`, 'utf8'),
) as FormCase[]; // ...so we TELL TypeScript what it is. A promise we must keep!

// "as" is trust, not proof. At run time JSON can be anything, so a type guard checks for real.
function isFormCase(value: unknown): value is FormCase {
  if (typeof value !== 'object' || value === null) return false;
  const v = value as Record<string, unknown>;
  return typeof v.name === 'string' && typeof v.form === 'object' && Array.isArray(v.expectedErrors);
}

const brokenJson = JSON.parse('[{"name":"oops","expectedErrors":"not a list"}]') as unknown[];
console.log('guard accepts the good data:', formCases.every(isFormCase));
console.log('guard rejects the broken data:', !brokenJson.every(isFormCase));

// ---------------------------------------------------------------------------
// 3) Data-driven checks: ONE piece of logic, MANY data rows
// ---------------------------------------------------------------------------
let passed = 0;
let failed = 0;

function check(name: string, actual: unknown, expected: unknown): void {
  const same = JSON.stringify(actual) === JSON.stringify(expected);
  if (same) passed++;
  else failed++;
  console.log(`${same ? 'PASS' : 'FAIL'}  ${name}`);
  if (!same) console.log(`      expected ${JSON.stringify(expected)}\n      actual   ${JSON.stringify(actual)}`);
}

console.log('\n--- year rule, from year-cases.json ---');
for (const c of yearCases) check(`year "${c.input}" (${c.name})`, yearError(c.input), c.expected);

console.log('\n--- form rules, from book-form-cases.json ---');
for (const c of formCases) check(c.name, validateBookForm(c.form), c.expectedErrors);

// Some data is easier to GENERATE than to write in a file:
console.log('\n--- generated data ---');
const longTitle = 'x'.repeat(MAX_TITLE_LENGTH + 1);
check('title of 201 characters', validateBookForm({ title: longTitle, author: 'A', year: '' }), [
  `Title must have at most ${MAX_TITLE_LENGTH} characters.`,
]);
check('title of exactly 200 characters', validateBookForm({ title: 'x'.repeat(200), author: 'A', year: '' }), []);

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exitCode = 1; // a non-zero exit code tells other tools "something failed"
```

**Step 4.** Run it and look at the **exit code**:

```powershell
npx tsx practice/09-json-data.ts
echo $LASTEXITCODE
```

(`echo $?` on macOS/Linux.)

### Expected output

```text
guard accepts the good data: true
guard rejects the broken data: true

--- year rule, from year-cases.json ---
PASS  year "1000" (lowest valid year)
PASS  year "2100" (highest valid year)
PASS  year "999" (just below the range)
PASS  year "2101" (just above the range)
PASS  year "" (empty is allowed)
PASS  year "   " (spaces only are allowed)
PASS  year "abc" (letters)
PASS  year "19.5" (decimal number)
PASS  year "-5" (negative number)

--- form rules, from book-form-cases.json ---
PASS  valid book
PASS  valid book without a year
PASS  empty form
PASS  title with spaces only
PASS  everything wrong at once

--- generated data ---
PASS  title of 201 characters
PASS  title of exactly 200 characters

16 passed, 0 failed
```

`echo $LASTEXITCODE` prints `0`.

**Step 5 — Make it fail on purpose.** In `year-cases.json`, change the `expected` of the `"just below the range"` row to `"Year must be between 1 and 2100."` and run again. One row fails, the others still pass, and the exit code becomes `1`:

```text
FAIL  year "999" (just below the range)
      expected "Year must be between 1 and 2100."
      actual   "Year must be between 1000 and 2100."
...
15 passed, 1 failed
```

Undo the change.

### Line-by-line explanation

| Code | Explanation |
|---|---|
| `import yearCasesFile from '../data/year-cases.json'` | Needs `resolveJsonModule` (from Lab 2.0). TypeScript infers the shape and checks it matches `YearCase[]` — a wrong file shape is a compile error |
| `readFileSync(\`${__dirname}/../data/…\`, 'utf8')` | Reads the text at run time; `__dirname` = folder of this file |
| `JSON.parse(text) as FormCase[]` | The result is untyped; `as` tells the compiler what we **believe** it is |
| `function isFormCase(value: unknown): value is FormCase` | A **type guard**: really inspects the data and tells TypeScript "if true, it is a `FormCase`" |
| `formCases.every(isFormCase)` | True only if every row passes the guard |
| `brokenJson` | Deliberately wrong data; the guard rejects it — proof the guard works |
| `JSON.stringify(a) === JSON.stringify(b)` | A simple way to compare two arrays/objects by content |
| `check(name, actual, expected)` | Our own mini test runner: print PASS/FAIL and count |
| `for (const c of yearCases) check(…)` | ONE piece of logic, many data rows |
| `'x'.repeat(MAX_TITLE_LENGTH + 1)` | **Generated** data: easier than a 201-character line in a file |
| `process.exitCode = 1` | The program's "result" for other tools: 0 = success, anything else = failure. CI uses this |

### Try it: JSON mistakes

JSON is stricter than TypeScript. Introduce each mistake, run, then undo:

| Mistake in the `.json` file | Real error |
|---|---|
| A trailing comma after the last item, e.g. `[1,]` | `SyntaxError: Unexpected token ']', "[1,]" is not valid JSON` |
| Single quotes, e.g. `['abc']` | `SyntaxError: Unexpected token ''', "['abc']" is not valid JSON` |
| A comment after the data, e.g. `[1] // note` | `SyntaxError: Unexpected non-whitespace character after JSON at position 4 (line 1 column 5)` |
| `"expected": "none"` where the code returns `null` | `FAIL` row: `expected "none"` / `actual null` — a **test-data** bug, not an application bug |

### Common mistakes

* Trusting `as` — "it compiled, so the data is right." It is not checked at run time.
* Editing a JSON file with a trailing comma or comments.
* Putting secrets (real passwords, tokens) into data files that go to Git.
* Mixing **data** and **logic**: the `.json` holds inputs and expectations only; decisions stay in code.
* Expecting `expected: null` to equal `"null"` — one is the value, the other is text.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Cannot find module '../data/year-cases.json'` (TS2307) | `resolveJsonModule` missing, or wrong path | Check `tsconfig.json` and the path |
| `ENOENT … no such file` from `readFileSync` | Path built from the wrong folder | Use `${__dirname}/…` as shown, not a path relative to where you typed the command |
| `SyntaxError: … in JSON at position N` | The file is not valid JSON | Open it in VS Code — it underlines the problem — or paste into a JSON validator |
| Exit code 0 but a `FAIL` was printed | `process.exitCode` line removed | Restore the last line |

### ✍️ Independent exercise

1. Add three new rows to `year-cases.json`: `"0001"` (leading zeros, 1 — below range), `"1999.5"` (decimal), `"+2000"` (plus sign). Predict each expected result **before** running. Then run and adjust the data **only if the code is right**.
2. Create `data/search-cases.json` (use your `SearchCase` shape from Lab 2.4) with three cases, write `practice/09b-search.ts` that loads it and checks each case against `new BookCatalog(...)`-style filtering. (Hint: copy `search` logic into a small function, or move `BookCatalog` into `utils/` and `export` it.)
3. Add a form case where the title is exactly 200 characters of `x` — and explain why generating it in code is better than typing it in JSON.

<details><summary>Answer</summary>

1. `"0001"` → `"Year must be between 1000 and 2100."` (1 is below 1000); `"1999.5"` → `"Year must be a whole number."`; `"+2000"` → `"Year must be a whole number."`
2. Export the class: `export class BookCatalog …` in `utils/catalog.ts`. Then loop over the cases: `check(c.name, catalog.search(c.searchText).map(b => b.title), c.expectedTitles)`.
3. JSON has no way to say "repeat x 200 times"; a 200-character line is unreadable and error-prone. Generate it: `'x'.repeat(200)`.
</details>

### Knowledge check (Lab 2.8)

1. Name two JSON rules that differ from TypeScript objects. *(Double quotes only for text and keys; no comments / no trailing commas.)*
2. Why is `JSON.parse(text) as Foo` risky? *(Nothing checks the data at run time.)*
3. What does a type guard do? *(Checks real data and narrows the compile-time type.)*
4. What is an exit code of 1 for? *(Tells other tools that the program failed.)*

### Completion checklist

- [ ] Both JSON files exist; `09-json-data.ts` reports **16 passed, 0 failed**, exit code 0.
- [ ] I made one row fail on purpose, saw `FAIL`, exit code 1, and restored it.
- [ ] I triggered at least two JSON syntax errors on purpose.
- [ ] I solved the exercise (or can explain the answers).
- [ ] I can explain data-driven testing in two sentences.

---

## Lab 2.9 — Capstone: a smoke check of the live application ✍️

### Learning objectives

Use **everything** from Phase 2 together, working mostly alone: types, functions, modules, `async`/`await`, error handling, and a clear report with an exit code.

### What a "smoke check" is

A quick test that answers "is the application basically alive and behaving?" — like switching on a device and checking that no smoke comes out. It runs in seconds and is the first thing a team runs after a deployment. In Phase 3 you will write the browser version with Playwright Test; here you write the skeleton by hand so you know what Playwright does for you.

### Prerequisites

Labs 2.1–2.8 complete; application running.

### Files

`practice/10-smoke-check.ts` — and `docs/labs/phase-2/typescript-notes.md` (your deliverable).

### Part A — 🧭 Read first (10 minutes)

Create `practice/10-smoke-check.ts`. Type it **slowly**, and before each block, say aloud what it does.

*File: `e2e/practice/10-smoke-check.ts`*

```ts
// Lab 2.9 - capstone: a hand-made smoke check of the live application.
// It uses everything from Phase 2. In Phase 3 Playwright Test will do the boring parts for us.
import { env } from '../utils/env';
import type { Book } from '../utils/types';

interface CheckResult {
  name: string;
  ok: boolean;
  detail: string;
}

/** Runs one check. Never throws: a crash inside a check becomes a failed result. */
async function check(name: string, body: () => Promise<string>): Promise<CheckResult> {
  try {
    return { name, ok: true, detail: await body() };
  } catch (error) {
    return { name, ok: false, detail: error instanceof Error ? error.message : String(error) };
  }
}

/** Throws a clear message when two values differ - a tiny version of expect(...).toBe(...). */
function expectEqual<T>(label: string, actual: T, expected: T): void {
  if (actual !== expected) {
    throw new Error(`${label}: expected ${JSON.stringify(expected)} but got ${JSON.stringify(actual)}`);
  }
}

const url = (path: string): string => `${env.baseUrl}${path}`;

async function main(): Promise<void> {
  const results: CheckResult[] = [];

  results.push(
    await check('health endpoint answers 200 {"status":"ok"}', async () => {
      const res = await fetch(url('/api/health/'));
      expectEqual('status', res.status, 200);
      expectEqual('body.status', ((await res.json()) as { status: string }).status, 'ok');
      return 'ok';
    }),
  );

  results.push(
    await check('book list is a JSON array of well-formed books', async () => {
      const res = await fetch(url('/api/books/'));
      expectEqual('status', res.status, 200);
      expectEqual('content-type is JSON', res.headers.get('content-type')?.includes('application/json'), true);
      const books = (await res.json()) as Book[];
      expectEqual('is an array', Array.isArray(books), true);
      for (const book of books) {
        for (const key of ['id', 'title', 'author', 'published_year', 'owner', 'created_at']) {
          if (!(key in book)) throw new Error(`book ${book.id} has no "${key}"`);
        }
      }
      return `${books.length} book(s)`;
    }),
  );

  results.push(
    await check('unknown book returns 404 with a message', async () => {
      const res = await fetch(url('/api/books/999999999/'));
      expectEqual('status', res.status, 404);
      expectEqual('detail', ((await res.json()) as { detail: string }).detail, 'No Book matches the given query.');
      return '404';
    }),
  );

  results.push(
    await check('anonymous /api/me/ is 401 with a challenge header', async () => {
      const res = await fetch(url('/api/me/'));
      expectEqual('status', res.status, 401);
      expectEqual('WWW-Authenticate', res.headers.get('www-authenticate'), 'Session');
      return '401';
    }),
  );

  results.push(
    await check('a write without a CSRF token is refused (403)', async () => {
      const res = await fetch(url('/api/register/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'nobody', password: 'S3cure-Lab-Passw0rd!' }),
      });
      expectEqual('status', res.status, 403);
      return '403';
    }),
  );

  results.push(
    await check('the login page is HTML and contains "Sign in"', async () => {
      const res = await fetch(url('/login/'));
      expectEqual('status', res.status, 200);
      expectEqual('content-type is HTML', res.headers.get('content-type')?.includes('text/html'), true);
      expectEqual('page mentions Sign in', (await res.text()).includes('Sign in'), true);
      return 'HTML';
    }),
  );

  // ---- report ----
  console.log(`Smoke check of ${env.baseUrl}\n`);
  for (const r of results) console.log(`${r.ok ? '✓' : '✗'} ${r.name}${r.ok ? '' : `\n    -> ${r.detail}`}`);
  const failed = results.filter((r) => !r.ok).length;
  console.log(`\n${results.length - failed} passed, ${failed} failed`);
  if (failed > 0) process.exitCode = 1;
}

main().catch((error: unknown) => {
  console.error('Could not run the smoke check:', error instanceof Error ? error.message : error);
  console.error(`Is the application running at ${env.baseUrl}?`);
  process.exitCode = 1;
});
```

```powershell
npx tsx practice/10-smoke-check.ts
```

### Expected output

```text
Smoke check of http://localhost:8000

✓ health endpoint answers 200 {"status":"ok"}
✓ book list is a JSON array of well-formed books
✓ unknown book returns 404 with a message
✓ anonymous /api/me/ is 401 with a challenge header
✓ a write without a CSRF token is refused (403)
✓ the login page is HTML and contains "Sign in"

6 passed, 0 failed
```

Stop the application and run it again. Every check should fail with a clear message and the exit code is 1:

```text
Smoke check of http://localhost:8000

✗ health endpoint answers 200 {"status":"ok"}
    -> fetch failed
…
0 passed, 6 failed
```

### How it is built — read the design, not just the lines

| Piece | Why it is built this way |
|---|---|
| `interface CheckResult` | One shape for every check's outcome |
| `check(name, body)` | Runs a check **and never throws**; a crash becomes a failed result, so one broken check does not hide the others |
| `expectEqual<T>(label, actual, expected)` | A tiny `expect(...).toBe(...)`; the generic `<T>` makes sure both sides have the same type; the message names *what* was compared |
| `url(path)` | One helper builds every address from `env.baseUrl` |
| The six checks | Each is `async`, `await`s the network, asserts, and returns a short note |
| Reporting after all checks | Results are collected first, printed after |
| `process.exitCode = 1` on failure | CI can fail the pipeline |

### Part B — ✍️ Independent tasks (25 minutes)

Work alone; use the hints only after trying.

1. **New check.** Add: *"the book list can be searched"* — request `/api/books/?search=zzzzzzzz`, expect status 200 and an **empty array**.
2. **New check.** Add: *"book list shows newest/oldest order when asked"* — request `/api/books/?ordering=title` and verify the titles come back in alphabetical order (use `localeCompare`; compare the list with a sorted copy). If you have fewer than 2 books the check should still pass.
3. **Better failure messages.** When the server is down the message is just `fetch failed`. Improve the `catch` in `check()` so it adds the *reason*: for an unreachable server, the real reason is on `error.cause`. Goal output: `fetch failed (connect ECONNREFUSED 127.0.0.1:8999)`. Test it with `BASE_URL=http://127.0.0.1:8999` (a port with nothing on it).
4. **Data-driven.** Replace the 404 check by a loop over a list `[{path, status}]` of three paths: a missing book (404), the health endpoint (200), and `/api/me/` (401). One loop, three results.

<details><summary>Hints</summary>

* Task 1: `const list = (await res.json()) as Book[]; expectEqual('length', list.length, 0);`
* Task 2: `const titles = list.map(b => b.title); const sorted = [...titles].sort((a, b) => a.localeCompare(b));` then compare with `JSON.stringify`. Note the server's ordering and `localeCompare` may treat capitals differently; if it fails, print both arrays and decide who is "right".
* Task 3: in the `catch`, `const cause = error instanceof Error && error.cause instanceof Error ? ` (${error.cause.message})` : '';`. Port 9 is blocked by `fetch` itself ("bad port"), so use 8999 or similar.
* Task 4: `for (const c of cases) results.push(await check(\`GET ${c.path} → ${c.status}\`, async () => { … }))`
</details>

<details><summary>Reference solution for task 3 (open after trying)</summary>

```ts
async function check(name: string, body: () => Promise<string>): Promise<CheckResult> {
  try {
    return { name, ok: true, detail: await body() };
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    const cause = error instanceof Error && error.cause instanceof Error ? ` (${error.cause.message})` : '';
    return { name, ok: false, detail: reason + cause };
  }
}
```
Result with nothing listening on port 8999: `fetch failed (connect ECONNREFUSED 127.0.0.1:8999)`.
</details>

### Part C — ✍️ Your own TypeScript notes (deliverable, 10 minutes)

Create `docs/labs/phase-2/typescript-notes.md` — a one-page cheat sheet **in your own words**, with a short example from *your* code for each heading:

```markdown
# My TypeScript notes — Phase 2

## const / let and types
## Strings and template literals
## Arrays and objects (the five array methods I use)
## Functions and arrow functions
## Interfaces and types (Omit, Partial, readonly)
## Classes and access modifiers
## Imports and exports
## async / await / Promise.all / try-catch
## JSON test data and data-driven checks
## The 5 compiler errors I met and what they meant
## Three things I will always remember in Playwright code
```

Review table (instructor or pair):

| Check | ✓ |
|---|---|
| Every heading has an example from my own code, not copied text | ☐ |
| "5 compiler errors" lists real error codes with a one-line cause | ☐ |
| "Three things" includes the rule about `await` | ☐ |

### 🏆 Optional challenge — a cookie jar and a full API session

*Skip freely — nothing in Phase 3 depends on it.* Browsers keep cookies automatically; `fetch` in Node does **not**. Write a small `CookieJar` class that remembers cookies from `Set-Cookie` headers (`response.headers.getSetCookie()`), sends them back in a `Cookie` header, and use it to run the whole API story by hand: **register → login → /me → create a book → delete it → logout → /me is 401 again**.

The write requests need the CSRF token from the `csrftoken` cookie in an `X-CSRFToken` header, plus an `Origin` header (Lab 1.6). Because the Book Library's sign-in flow was already traced in Lab 1.5, you know the order of requests.

<details><summary>Reference solution — `practice/11-challenge-cookie-flow.ts` (open after trying)</summary>

*File: `e2e/practice/11-challenge-cookie-flow.ts`*

```ts
// Lab 2.9 - OPTIONAL CHALLENGE (solution): register, sign in and add a book with plain fetch.
// Node's fetch has no cookie jar, so we keep the cookies ourselves - exactly the job that
// Playwright's APIRequestContext will do for us from Phase 3 on.
import { env } from '../utils/env';
import { makeBook, uniqueUsername } from '../utils/test-data';
import type { Book } from '../utils/types';

class CookieJar {
  private readonly cookies = new Map<string, string>();

  /** Remember every cookie the server set in a response. */
  store(response: Response): void {
    for (const line of response.headers.getSetCookie()) {
      const [pair] = line.split(';'); // "sessionid=abc123; HttpOnly; Path=/" -> "sessionid=abc123"
      const separator = pair.indexOf('=');
      this.cookies.set(pair.slice(0, separator), pair.slice(separator + 1));
    }
  }

  header(): string {
    return [...this.cookies].map(([name, value]) => `${name}=${value}`).join('; ');
  }

  names(): string[] {
    return [...this.cookies.keys()];
  }
}

const jar = new CookieJar();

async function csrfToken(): Promise<string> {
  const response = await fetch(`${env.baseUrl}/api/csrf/`, { headers: { Cookie: jar.header() } });
  jar.store(response);
  return ((await response.json()) as { csrfToken: string }).csrfToken;
}

/** POST/PATCH/DELETE: fetch a fresh token first, then send token + cookies. */
async function send(method: string, path: string, body?: unknown): Promise<Response> {
  const token = await csrfToken();
  const response = await fetch(`${env.baseUrl}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': token,
      Cookie: jar.header(),
      Origin: env.baseUrl,
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  jar.store(response);
  return response;
}

async function main(): Promise<void> {
  const username = uniqueUsername('flow');
  const password = env.testUserPassword;

  const register = await send('POST', '/api/register/', { username, password });
  console.log('register     :', register.status);

  const login = await send('POST', '/api/login/', { username, password });
  console.log('login        :', login.status, '| cookies:', jar.names());

  const me = await fetch(`${env.baseUrl}/api/me/`, { headers: { Cookie: jar.header() } });
  console.log('me           :', me.status, await me.json());

  const created = await send('POST', '/api/books/', makeBook());
  const book = (await created.json()) as Book;
  console.log('create book  :', created.status, `"${book.title}" owned by ${book.owner}`);

  const removed = await send('DELETE', `/api/books/${book.id}/`);
  console.log('delete book  :', removed.status);

  const logout = await send('POST', '/api/logout/');
  const after = await fetch(`${env.baseUrl}/api/me/`, { headers: { Cookie: jar.header() } });
  console.log('logout       :', logout.status, '| me afterwards:', after.status);
}

main().catch((error: unknown) => {
  console.error('FAILED:', error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
```

Output of the reference solution:

```text
register     : 201
login        : 200 | cookies: [ 'csrftoken', 'sessionid' ]
me           : 200 { id: 5, username: 'flow_b3688d1d' }
create book  : 201 "PW Book db43b40e" owned by flow_b3688d1d
delete book  : 204
logout       : 204 | me afterwards: 401
```

</details>

> **What you just rebuilt by hand** is what the browser does for you, and what Playwright's `request` and `context` objects do for you in Phases 3 and 6. Knowing the mechanics makes their behaviour unsurprising.

### Completion checklist (Lab 2.9)

- [ ] The six checks pass against the running application (6 passed, 0 failed).
- [ ] With the app stopped, all fail with readable messages and the exit code is 1.
- [ ] I added tasks 1–4 (at least 1, 3 and 4).
- [ ] `docs/labs/phase-2/typescript-notes.md` exists and passes the review table.

---

## Phase 2 — Mixed knowledge check (15 questions)

Answer without looking back, then check the answers. Aim for **12 or more**.

1. In one sentence: what does TypeScript add to JavaScript?
2. Which command runs a `.ts` file? Which one checks types without running?
3. `const` or `let` for a value that never changes?
4. What is the type of the Book Library year as returned by the API?
5. `rows.find(…)` vs `rows.filter(…)` — which returns an array?
6. What does `user?.profile?.name ?? 'anonymous'` do when `user` is `undefined`?
7. What is the result of `'5' + 3`, and of `5 + 3`?
8. Why does `yearError('abc')` return a message but `yearError('')` return `null`?
9. What does `Omit<Book, 'id'>` give you?
10. What access modifier lets child classes but not outsiders use a property?
11. How do you make a helper in one file usable in another?
12. What does a missing `await` before `fetch(url)` cause?
13. When is `Promise.all` wrong to use?
14. Why is `JSON.parse(text) as Foo` not proof that the data is a `Foo`?
15. What exit code means success, and why do automation tools care?

<details><summary>Answers</summary>

1. Types (labels) that the compiler checks before the program runs.
2. `npx tsx file.ts` runs; `npm run typecheck` (`tsc --noEmit`) checks.
3. `const`.
4. `number | null`.
5. `filter`.
6. It returns `'anonymous'` instead of crashing.
7. `'53'` and `8`.
8. The year is optional: an empty value is allowed, but non-digits are not.
9. A copy of the `Book` shape without the `id` property.
10. `protected`.
11. `export` it from the first file and `import` it in the second.
12. You get a Promise instead of the response; later lines run too early or fail (`TS2339`).
13. When the steps depend on each other (e.g. create, then delete).
14. `as` is not checked at run time; any text can be in the file.
15. `0` means success; non-zero tells CI that something failed.
</details>

---

### ✅ Phase 2 checkpoint — do not start Phase 3 until all boxes are ticked

- [ ] `npm run typecheck` in `e2e/` prints **nothing** (no errors).
- [ ] All of these run successfully: `npx tsx practice/02-variables.ts` … `09-json-data.ts` (16 passed), `10-smoke-check.ts` (6 passed).
- [ ] The helper files `utils/types.ts`, `book-rules.ts`, `test-data.ts`, `env.ts` exist and I can say what each is for.
- [ ] `docs/labs/phase-2/typescript-notes.md` exists and passes the review table.
- [ ] I scored at least **12/15** on the knowledge check.
- [ ] I can explain, without notes: the golden rule about `await`; why `strict` stays on; why test data must be unique; what `import type` does.
- [ ] I can read the Playwright snippet below and explain every line.

```ts
import { test, expect } from '@playwright/test';

test('shows the sign-in heading', async ({ page }) => {
  await page.goto('/login/');
  await expect(page.getByRole('heading', { name: 'Sign in' })).toBeVisible();
});
```

<details><summary>Explanation</summary>

`import { test, expect } from …` — named imports from a package. `test('name', async ({ page }) => { … })` — calling a function with a text and an **async arrow function** as a callback; `{ page }` is destructuring (Lab 2.2). `await page.goto(…)` — navigation takes time, so `await`. `page.getByRole('heading', { name: 'Sign in' })` — a function call with an object argument. `await expect(…).toBeVisible()` — an assertion that also waits. Everything in it is something you now know.
</details>

### Glossary (Phase 2)

| Term | Meaning |
|---|---|
| **Type** | A label for what kind of value something is |
| **Interface** | A named shape for an object |
| **Union type** | One of several allowed types, `A \| B` |
| **Literal type** | A type that allows exact values only, `'chromium' \| 'firefox'` |
| **Generic `<T>`** | A placeholder type the caller fills in |
| **Type guard** | A function that checks data at run time and narrows its type |
| **Template literal** | Backtick text with `${…}` inserted values |
| **Destructuring / spread** | Pulling properties out / copying and overriding properties |
| **Callback** | A function passed into another function |
| **Closure** | A function that remembers the variables around where it was created |
| **Class / instance** | Blueprint / one object made from it |
| **Access modifier** | `public`, `protected`, `private`, `readonly` |
| **Module** | A file that exports and imports code |
| **Promise** | An IOU for a value that will arrive later |
| **`async` / `await`** | Declare a function that returns a Promise / wait for one |
| **Exception** | An error thrown with `throw` and handled with `try/catch` |
| **JSON** | A text format for structured data |
| **Data-driven test** | One check, many data rows |
| **Exit code** | The number a program returns: 0 = success |
| **`tsx` / `tsc`** | Runs TypeScript / checks TypeScript |

### Phase 2 deliverables

| Deliverable | Location |
|---|---|
| Practice files `01`–`10` (and optionally `11`) | `e2e/practice/` |
| Shared helpers | `e2e/utils/` (`types.ts`, `book-rules.ts`, `test-data.ts`, `env.ts`) |
| Test data | `e2e/data/*.json` |
| Your TypeScript notes | `docs/labs/phase-2/typescript-notes.md` |

> **Next — Phase 3: Playwright fundamentals.** You will install Playwright Test, write your first browser test, learn locators, auto-waiting, assertions, `test.describe`/hooks, and run tests headed, with the UI mode and with traces. Everything you built in this phase is used there. When your checkpoint passes, say **"Phase 2 complete"** and ask for Phase 3.

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

**Phase 2 verified by execution** (Node 22, TypeScript 7.0.2, tsx 4.23): `npm run typecheck` passes with no errors on all files; practice files `01`–`10` run with the output shown; `09-json-data.ts` reports 16 passed / 0 failed (exit 0) and, with one expected value changed, reports a failure and exits 1; `10-smoke-check.ts` passes 6/6 against the running app and reports 6 failures with exit code 1 when the app is stopped; the optional `11-challenge-cookie-flow.ts` runs the complete register → login → create → delete → logout flow over a hand-made cookie jar. Every compiler error code quoted in Phase 2 was captured from the real compiler. The code in the exercise answers was run where it produces output (the rest follows the same patterns).

**Pacing, Phase 2:** Lab 2.0 (45 min) · 2.1 (40) · 2.2 (50) · 2.3 (45) · 2.4 (40) · 2.5 (45) · 2.6 (40) · 2.7 (60) · 2.8 (45) · 2.9 (45) · optional challenge (30).

**Suggested Phase 2 grading:** practice files run and typecheck clean 30% · capstone smoke check with tasks 1, 3, 4 25% · TypeScript notes 20% · knowledge check 15% · explanation of `await` and `strict` 10%.

**Pacing, Phase 1:** Lab 1.0 (45 min) · 1.1 (45) · 1.2 (45) · 1.3 (60) · 1.4 (60) · 1.5 (60) · 1.6 (45) · 1.7 (30).

**Suggested Phase 1 grading:** feature inventory 20% · manual scenarios 30% · locator notes 15% · UI→API map 15% · knowledge check 10% · explanation of the sign-in flow 10%.
