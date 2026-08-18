# KanMind Backend

![Python](https://img.shields.io/badge/python-3.14-blue)
![Django](https://img.shields.io/badge/django-6.0-092E20)
![DRF](https://img.shields.io/badge/DRF-3.17-A30000)
![License](https://img.shields.io/badge/license-educational-lightgrey)

A Django REST Framework backend for KanMind, a Kanban-style project management tool. It handles user authentication, boards, tasks, and comments, and is built to be consumed by a separate frontend application.

## Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [API Overview](#api-overview)
- [Notes for Local Development](#notes-for-local-development)

## Tech Stack

| | |
|---|---|
| Language | Python 3.14 |
| Framework | Django 6.0.8 |
| API | Django REST Framework 3.17.1 |
| Auth | Token-based (`rest_framework.authtoken`) |
| Database | SQLite (local development) |
| CORS | django-cors-headers |

## Project Structure

```
KanMind/
├── core/            project settings, root URL config
├── auth_app/        registration and login
│   └── api/         serializers, views, urls
├── kanban_app/      boards, tasks, comments
│   └── api/         serializers, views, urls, permissions
├── manage.py
└── requirements.txt
```

## Getting Started

Quick version, if you just want to get it running:

```bash
git clone https://github.com/JensBaumannDev/KanMind.git
cd KanMind
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/api/`.

### Step by step

**1. Clone the repository**

```bash
git clone https://github.com/JensBaumannDev/KanMind.git
cd KanMind
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
```

| OS | Command |
|---|---|
| Windows | `.venv\Scripts\activate` |
| macOS/Linux | `source .venv/bin/activate` |

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Copy the example file and fill in your own secret key:

```bash
cp .env.example .env
```

Generate a key however you like, e.g. with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**5. Apply migrations**

```bash
python manage.py migrate
```

**6. Create a superuser (optional, for the admin site)**

```bash
python manage.py createsuperuser
```

**7. Run the development server**

```bash
python manage.py runserver
```

## Authentication

Registration and login return an auth token. Send it with every authenticated request as:

```
Authorization: Token <your-token>
```

## API Overview

**Auth**

| Method | Endpoint |
|---|---|
| POST | `/api/registration/` |
| POST | `/api/login/` |

**Boards**

| Method | Endpoint |
|---|---|
| GET, POST | `/api/boards/` |
| GET, PATCH, DELETE | `/api/boards/<id>/` |
| GET | `/api/email-check/?email=` |

**Tasks**

| Method | Endpoint |
|---|---|
| POST | `/api/tasks/` |
| PATCH, DELETE | `/api/tasks/<id>/` |
| GET | `/api/tasks/assigned-to-me/` |
| GET | `/api/tasks/reviewing/` |

**Comments**

| Method | Endpoint |
|---|---|
| GET, POST | `/api/tasks/<task_id>/comments/` |
| DELETE | `/api/tasks/<task_id>/comments/<comment_id>/` |

## Notes for Local Development

- The database (`db.sqlite3`) is not tracked in version control. Running the migrations above will create a fresh one.
- `CORS_ALLOWED_ORIGINS` in `core/settings.py` is currently set to `http://127.0.0.1:5500`, which matches the default port used by VS Code's Live Server extension when serving the frontend locally. Adjust it if your frontend runs elsewhere.
- This backend is meant to be used together with the [KanMind frontend](https://github.com/Developer-Akademie-Backendkurs/project.KanMind), which lives in its own repository and is not part of this one.
- Django admin is available at `/admin/` once a superuser has been created.
