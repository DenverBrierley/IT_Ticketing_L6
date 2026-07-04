# EVRi IT Helpdesk

A secure IT support ticketing web application built with Django, created for the
**L6M5 Software Engineering and DevOps** portfolio. Internal staff raise IT tickets
(handheld scanner faults, courier-app issues, depot WMS problems, and so on),
support agents triage and resolve them, and administrators manage users, categories,
and the wider system.

**Live demo:** https://evri-helpdesk.onrender.com/
*(Hosted on Render's free tier — the service sleeps after inactivity, so the first
request may take 30–60 seconds to wake.)*

**Repository:** https://github.com/DenverBrierley/IT_Ticketing_L6

---

## Demo accounts

The database is seeded with demonstration accounts (all share the same password).
These are demo-only credentials with no access to anything sensitive.

| Username        | Role          | Password       |
|-----------------|---------------|----------------|
| `admin_denver`  | Administrator | `DemoPass123!` |
| `agent_sam`     | Support Agent | `DemoPass123!` |
| `agent_priya`   | Support Agent | `DemoPass123!` |
| `user_leeds`    | End User      | `DemoPass123!` |
| `user_courier`  | End User      | `DemoPass123!` |

Log in as `admin_denver` to see the full feature set, or as `user_leeds` to see the
restricted end-user view.

---

## Features

- **Three user roles** — End User, Support Agent, Administrator — with distinct
  capabilities enforced at the view and query level.
- **Ticket management** — create, view, update, and delete tickets, with status and
  priority workflows and confirm-before-delete.
- **Conversation threads** — comments on each ticket, including internal notes that
  are visible only to agents and administrators.
- **Category management** — administrators manage the list of ticket categories.
- **User management** — administrators change user roles, departments, and active
  status through the app (not just the Django admin).
- **Role-aware dashboard** — a landing page with summary counts tailored to each role.
- **Custom error pages** — branded 403, 404, and 500 pages in production.

---

## Security

The application demonstrably defends against three OWASP Top 10 categories, with
additional hardening beyond that.

- **A01 – Broken Access Control.** Reusable access-control mixins enforce
  authentication, role restrictions, and object-level ownership. A logged-in user
  cannot open, edit, or delete another user's ticket by manipulating the URL
  (returns 403), and non-admins are blocked from management pages.
- **A03 – Injection (SQL injection & XSS).** All database access goes through the
  Django ORM, which parameterises queries. Templates auto-escape output, so
  user-supplied content containing HTML/script is rendered as inert text.
- **A07 – Identification & Authentication Failures.** Passwords are hashed with
  PBKDF2 and validated against Django's password-strength rules. `django-axes`
  locks out repeated failed logins to defend against brute-force attacks.

Additional hardening: CSRF protection on all forms, `SECRET_KEY` and other secrets
loaded from environment variables (never committed), production security headers
(HTTPS redirect, secure cookies, HSTS, clickjacking protection), and a clean
`python manage.py check --deploy` audit.

---

## Tech stack

- **Language / framework:** Python, Django
- **Database:** SQLite
- **Frontend:** Django templates with Bootstrap 5 (CDN)
- **Security:** django-axes
- **Production server:** Gunicorn with WhiteNoise for static files
- **Testing:** pytest, pytest-django, pytest-cov
- **CI/CD:** GitHub Actions
- **Containerisation:** Docker
- **Hosting:** Render

---

## Running locally

### Prerequisites
- Python 3.12+ and Git installed.

### 1. Clone and enter the project
```bash
git clone https://github.com/DenverBrierley/IT_Ticketing_L6.git
cd IT_Ticketing_L6
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root
This file holds local secrets and is not committed to the repository.
```
DJANGO_SECRET_KEY=your-generated-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```
Generate a secret key with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Set up the database and seed demo data
```bash
python manage.py migrate
python manage.py seed_demo
```

### 6. Run the development server
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ and log in with one of the demo accounts above.

> A pre-seeded `db.sqlite3` is included in the repository for convenience. Running
> `migrate` and `seed_demo` will populate a fresh database with the same data if you
> prefer to start clean.

---

## Running the tests

The suite covers models, views, permissions, and three security-focused tests that
map directly to the OWASP defences above.

```bash
pytest
```

With a coverage report:
```bash
pytest --cov=tickets --cov=accounts --cov=dashboard --cov-report=term-missing
```

---

## Running with Docker

Build and run the containerised application:
```bash
docker build -t evri-helpdesk .
docker run -p 8000:8000 --env DJANGO_SECRET_KEY=dev-key --env DJANGO_DEBUG=True evri-helpdesk
```

---

## Project structure

```
IT_Ticketing_L6/
├── config/          # Project settings, URLs, WSGI
├── accounts/        # Custom user model, auth, roles, user management
├── tickets/         # Tickets, categories, comments (core domain)
├── dashboard/       # Role-aware landing page
├── templates/       # Base layout + per-app templates
├── .github/workflows/ci.yml   # Continuous integration pipeline
├── Dockerfile
├── build.sh         # Render build script
├── requirements.txt
└── manage.py
```

---

## Continuous integration

Every push and pull request to `main` triggers the GitHub Actions workflow, which
installs dependencies and runs the full test suite in a clean environment. The build
status is visible on the repository's **Actions** tab.
