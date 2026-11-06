# Django Book Library API — Authentication, HTTPS and API Testing Lab

A small, beginner-friendly API for learning how **user authentication, sessions, cookies, CSRF
protection, HTTPS certificates and API testing** fit together.

> For learning only. See [Security limitations](#17-security-limitations-and-production-considerations).

## 1. Purpose and learning objectives

After working through this project you can explain and test:
* authentication vs authorization, cookies vs server-side sessions, CSRF vs CORS
* how HTTPS/TLS and certificates work, and why HTTPS does not replace login
* HTTP status codes (200, 201, 204, 400, 401, 403, 404) and headers/bodies
* backend unit tests (Django) and API tests (Playwright + TypeScript, HTTP only)

## 2. Architecture and request flow

```text
client (browser / curl / Playwright)
   │  HTTPS (TLS terminated by uvicorn)
   ▼
uvicorn ─▶ Django middleware (sessions, CSRF, auth) ─▶ DRF view ─▶ permissions
        ─▶ serializer (validation) ─▶ model ─▶ SQLite
```

Login flow: `POST /api/login/` → Django checks the password hash → creates a server-side session
→ `Set-Cookie: sessionid=…` → the client sends the cookie on every request → Django attaches
`request.user` → permissions are checked → `POST /api/logout/` deletes the session.

Books are a **shared public catalogue**: anyone can read; logged-in users can add; only the owner
(or a staff user) can delete.

## 3. Tools and technologies

Python · Django · Django REST Framework · SQLite · uvicorn (HTTPS) · OpenSSL (certificate) ·
Node.js · Playwright (`APIRequestContext` only) · TypeScript

## 4. Folder structure

```text
book-library-lab/
├── config/            Django project settings and URLs
├── books/             the Book API app (models, serializers, views, permissions)
├── backend_tests/     Django unit and API-behaviour tests
├── api-tests/         Playwright + TypeScript API tests (separate Node project)
├── certs/             local development certificate (generated, git-ignored)
├── docs/              workbook and notes
├── manage.py  requirements.txt  .gitignore  README.md
```

## 5. Prerequisites

Python 3.12+ (3.10+ works), Node.js 20+, OpenSSL (Git for Windows includes it), Windows PowerShell.

## 6. Virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 7. Install dependencies

```powershell
pip install -r requirements.txt
cd api-tests
npm install --save-dev @playwright/test typescript @types/node cross-env
cd ..
```

(Playwright needs **no browser download** for API tests.)

## 8. Database migrations

```powershell
python manage.py migrate
```

## 9. Create a test user

```powershell
python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_user('alice', password='S3cure-Lab-Passw0rd!')"
```

or call `POST /api/register/` (see section 12).

## 10. Generate and trust the local HTTPS certificate

```powershell
openssl req -x509 -newkey rsa:2048 -nodes -keyout certs/localhost-key.pem -out certs/localhost-cert.pem -days 365 -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost" -addext "basicConstraints=critical,CA:FALSE"
```

Trust it **explicitly**, never by disabling verification:
* curl: `--cacert certs/localhost-cert.pem` (add `--ssl-no-revoke` on Windows)
* Playwright/Node: `NODE_EXTRA_CA_CERTS=../certs/localhost-cert.pem` (already set by `npm test`)
* Browser (optional): `certutil -addstore -user Root certs\localhost-cert.pem`
  — remove later with `certutil -delstore -user Root localhost`

Never commit anything in `certs/` except its README.

## 11. Start the HTTPS server

Django's `runserver` does **not** support HTTPS. Use uvicorn:

```powershell
python -m uvicorn config.asgi:application --host 127.0.0.1 --port 8443 --ssl-keyfile certs/localhost-key.pem --ssl-certfile certs/localhost-cert.pem --lifespan off
```

## 12. Try each endpoint

Set up helpers (PowerShell, project root). Every POST/DELETE needs `X-CSRFToken` **and** `Origin`.

```powershell
$BASE = "https://localhost:8443"
$TLS  = @("--ssl-no-revoke", "--cacert", "certs/localhost-cert.pem")
$JAR  = "scratch\jar.txt"
mkdir scratch -ErrorAction SilentlyContinue
function Get-Csrf { (curl.exe @TLS -s -c $JAR -b $JAR "$BASE/api/csrf/" | ConvertFrom-Json).csrfToken }
Set-Content scratch\alice.json -Encoding ascii -Value '{"username":"alice","password":"S3cure-Lab-Passw0rd!"}'
Set-Content scratch\book.json  -Encoding ascii -Value '{"title":"Dune","author":"Frank Herbert","published_year":1965}'
```

| Request | Example |
|---|---|
| Health | `curl.exe @TLS "$BASE/api/health/"` |
| Register | `$T=Get-Csrf; curl.exe @TLS -i -c $JAR -b $JAR -H "Content-Type: application/json" -H "X-CSRFToken: $T" -H "Origin: $BASE" --data "@scratch/alice.json" "$BASE/api/register/"` |
| Login | same as register with `/api/login/` (get a **new** token first) |
| Who am I | `curl.exe @TLS -b $JAR "$BASE/api/me/"` |
| List books | `curl.exe @TLS "$BASE/api/books/"` |
| One book | `curl.exe @TLS "$BASE/api/books/1/"` |
| Add book | login, `$T=Get-Csrf`, then POST `scratch/book.json` to `/api/books/` with the same headers |
| Delete book | `$T=Get-Csrf; curl.exe @TLS -i -X DELETE -c $JAR -b $JAR -H "X-CSRFToken: $T" -H "Origin: $BASE" "$BASE/api/books/1/"` |
| Logout | `$T=Get-Csrf; curl.exe @TLS -i -X POST -c $JAR -b $JAR -H "X-CSRFToken: $T" -H "Origin: $BASE" "$BASE/api/logout/"` |

Example bodies and statuses:

```text
POST /api/register/   {"username":"alice","password":"S3cure-Lab-Passw0rd!"}
 -> 201 {"id":2,"username":"alice"}
POST /api/login/      {"username":"alice","password":"S3cure-Lab-Passw0rd!"}
 -> 200 {"id":2,"username":"alice"}      Set-Cookie: sessionid=…; HttpOnly; Secure; SameSite=Lax
POST /api/login/      wrong password      -> 401 {"detail":"Invalid username or password."}
POST /api/books/      {"title":"Dune","author":"Frank Herbert","published_year":1965}
 -> 201 {"id":3,"title":"Dune","author":"Frank Herbert","published_year":1965,"owner":"alice","created_at":"…"}
POST /api/books/      {"author":"x"}      -> 400 {"title":["This field is required."]}
POST /api/books/      not logged in       -> 401 {"detail":"Authentication credentials were not provided."}
POST /api/books/      no CSRF token       -> 403 {"detail":"CSRF Failed: CSRF token missing."}
DELETE /api/books/3/  someone else's book -> 403
DELETE /api/books/999/                    -> 404 {"detail":"No Book matches the given query."}
DELETE /api/books/3/  owner               -> 204 (no body)
```

## 13. Run the backend tests

```powershell
python manage.py test backend_tests -v 2
```

## 14. Run the Playwright TypeScript API tests

Terminal A (separate throw-away database):

```powershell
$env:LAB_DB_PATH = "$PWD\test-api.sqlite3"
python manage.py migrate
python -m uvicorn config.asgi:application --host 127.0.0.1 --port 8443 --ssl-keyfile certs/localhost-key.pem --ssl-certfile certs/localhost-cert.pem --lifespan off
```

Terminal B:

```powershell
cd api-tests
npm test
```

## 15. Debugging authentication, cookies, CSRF and TLS

| Symptom | Likely cause and fix |
|---|---|
| `401` on a write | Not logged in, or the cookie jar wasn't passed (`-b $JAR`) |
| `403 CSRF token missing/incorrect` | Fetch a **fresh** token right before each POST (login rotates it) |
| `403 Referer checking failed` / `Origin checking failed` | Add `-H "Origin: https://localhost:8443"`; match `CSRF_TRUSTED_ORIGINS` |
| `403` deleting a book | You are not the owner |
| `self-signed certificate` | The tool doesn't trust `localhost-cert.pem` (see section 10) |
| name mismatch error | Use `https://localhost:8443`, not `127.0.0.1` |
| `certificate has expired` | Regenerate the certificate |

## 16. Common Windows PowerShell problems

| Problem | Fix |
|---|---|
| `Activate.ps1` / `npm.ps1` cannot be loaded | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `curl` behaves oddly | Use `curl.exe` (PowerShell's `curl` is an alias) |
| JSON parse error / quotes lost | Put JSON in a file; write with `-Encoding ascii`; use `--data "@file.json"` |
| `pip freeze > requirements.txt` produces a broken file (UTF-16) | Edit `requirements.txt` by hand, or `pip freeze \| Out-File requirements.txt -Encoding ascii` |
| `openssl` not found | `$env:Path += ";C:\Program Files\Git\usr\bin"` |
| `/CN=localhost` becomes a file path | Don't use Git Bash for OpenSSL; use PowerShell |
| `CRYPT_E_NO_REVOCATION_CHECK` | add `--ssl-no-revoke` |

## 17. Security limitations and production considerations

This is a **learning setup**. In particular:
* `DEBUG = True`, a hard-coded `SECRET_KEY`, SQLite and a self-signed certificate are for local use only.
* No login throttling/lockout, no email verification, no password reset, no audit log.
* Registration reveals whether a username exists.
* No CORS configuration (not needed for same-origin clients).
* No HSTS or HTTP→HTTPS redirect.

For production: a public CA certificate (e.g. Let's Encrypt) and a reverse proxy that terminates
TLS (then set `SECURE_PROXY_SSL_HEADER`), `DEBUG=False`, secrets from the environment, a real
`ALLOWED_HOSTS`, PostgreSQL, rate limiting, HSTS, logging/monitoring, and run
`python manage.py check --deploy`.

## Glossary

| Term | Meaning |
|---|---|
| **Authentication** | Proving who you are |
| **Authorization** | Deciding what you may do |
| **Session** | Server-side record of a logged-in user |
| **Session cookie** | Cookie holding the random session ID |
| **CSRF** | Forged request using your logged-in browser; stopped with a secret token |
| **CORS** | Browser rule about reading cross-origin responses |
| **TLS / SSL** | Protocol that encrypts HTTP (SSL is the obsolete predecessor) |
| **Certificate** | Signed statement binding a public key to a host name |
| **CA** | Certificate authority — a trusted signer |
| **SAN** | Subject Alternative Name — the host names a certificate covers |
| **ETag** | Fingerprint of a response, used for conditional requests |
