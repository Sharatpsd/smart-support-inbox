# Smart Customer Support Inbox Engine

Backend Technical Assessment built with **Django**, **Django REST Framework**, **JWT Authentication**, **Celery**, and **Redis**.

---

# Features

- JWT Authentication (Login & Refresh Token)
- Conversation Listing with Pagination
- Search and Status Filtering
- Conversation Message History
- Agent Reply API
- Rule-Based Mock AI Reply Suggestion
- Conversation Locking System
- Redis Cache-Based Lock Management
- Celery Background Task Processing
- Sentiment Analysis Pipeline
- Swagger / OpenAPI Documentation
- Unit & API Testing

---

# Tech Stack

- Python 3.11
- Django 5
- Django REST Framework
- Simple JWT
- Celery
- Redis
- SQLite
- drf-spectacular (Swagger)

---

# Authentication

### Default Admin User

```
Email:
admin@test.com

Password:
admin123
```

### Generate Access Token

```
POST /api/token/
```

### Refresh Token

```
POST /api/token/refresh/
```

---

# API Endpoints

## Authentication

| Method | Endpoint |
|----------|---------------------------|
| POST | /api/token/ |
| POST | /api/token/refresh/ |

---

## Conversations

| Method | Endpoint |
|----------|--------------------------------|
| GET | /api/conversations/ |
| GET | /api/conversations/{id}/messages/ |
| POST | /api/conversations/{id}/reply/ |

---

## AI Suggestion

| Method | Endpoint |
|----------|-----------------------------------------|
| POST | /api/conversations/{id}/suggest-reply/ |

---

## Conversation Lock

| Method | Endpoint |
|----------|--------------------------------------|
| POST | /api/conversations/{id}/lock/ |
| GET | /api/conversations/{id}/lock-status/ |
| POST | /api/conversations/{id}/unlock/ |

---

# Project Architecture

```
                 Client
                    │
                    ▼
            Django REST API
                    │
     ┌──────────────┼──────────────┐
     │              │              │
Conversation     AI Engine      Lock Service
     │                             │
     │                         Redis Cache
     │
 Save Reply
     │
     ▼
 Celery Background Task
     │
 Sentiment Analysis
     │
 Update Conversation
```

---

# Real-Time Strategy

The current implementation uses REST APIs.

For production deployment, Django Channels with Redis Pub/Sub can be integrated to provide real-time WebSocket communication without changing the existing application architecture.

---

# Background Processing

When an agent submits a reply:

1. Reply is stored instantly.
2. API returns the response immediately.
3. Celery background task starts.
4. Sentiment analysis runs asynchronously.
5. Conversation sentiment gets updated.

---

# Database

SQLite is used for simplicity and easy project evaluation.

For production deployment, PostgreSQL is recommended because it provides:

- Better concurrency
- Better indexing
- ACID transactions
- Improved scalability

---

# API Documentation

Swagger

```
http://127.0.0.1:8000/swagger/
```

Redoc

```
http://127.0.0.1:8000/redoc/
```

---

# Screenshots

## 1. Swagger UI

![Swagger UI](screenshots/swigger_ui.png)

---

## 2. JWT Authentication

![JWT Authentication](screenshots/Authentication%20(JWT).png)

---

## 3. Conversation Management

![Conversation Management](screenshots/Conversation%20Management.png)

---

## 4. Customer Support Conversation

![Customer Support Conversation](screenshots/customer%20support%20conversation.png)

---

# Installation

Clone the repository

```bash
git clone https://github.com/Sharatpsd/smart-support-inbox.git
```

Move into the project

```bash
cd smart-support-inbox
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
python manage.py migrate
```

Seed default admin

```bash
python manage.py seed_data
```

Run the development server

```bash
python manage.py runserver
```

Start Redis

```bash
redis-server
```

Run Celery Worker

```bash
celery -A support_inbox worker -l info
```

---

# Running Tests

```bash
python manage.py test
```

---

# Future Improvements

- PostgreSQL
- Docker
- Docker Compose
- Django Channels (WebSockets)
- Server-Sent Events (SSE)
- OpenTelemetry Monitoring
- CI/CD Pipeline
- Kubernetes Deployment

---

# Author

**Sharat Acharja**

Backend Developer Technical Assessment
