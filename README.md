# Smart Customer Support Inbox Engine

Backend Technical Assessment built with **Django**, **Django REST Framework**, **JWT Authentication**, **Celery**, and **Redis**.

## Features

- JWT Authentication
- Conversation Listing with Pagination
- Search & Status Filter
- Conversation Message History
- Agent Reply API
- Rule-Based Mock AI Suggestion Engine
- Distributed Conversation Locking
- Redis Cache Lock
- Celery Background Task
- Sentiment Analysis Pipeline
- Swagger / OpenAPI Documentation
- Unit & API Tests

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

Default Admin User

```
Email:
admin@test.com

Password:
admin123
```

Generate Access Token

```
POST /api/token/
```

Refresh Token

```
POST /api/token/refresh/
```

---

# API Endpoints

## Authentication

| Method | Endpoint |
|---------|-----------|
| POST | /api/token/ |
| POST | /api/token/refresh/ |

## Conversations

| Method | Endpoint |
|---------|-----------|
| GET | /api/conversations/ |
| GET | /api/conversations/{id}/messages/ |
| POST | /api/conversations/{id}/reply/ |

## AI

| Method | Endpoint |
|---------|-----------|
| POST | /api/conversations/{id}/suggest-reply/ |

## Conversation Lock

| Method | Endpoint |
|---------|-----------|
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

This assessment allows either implementing or documenting a real-time communication strategy.

The current implementation uses REST APIs.

For production deployment, Django Channels with Redis Pub/Sub would be used to provide real-time WebSocket communication without changing the application architecture.

---

# Background Processing

After an agent submits a reply:

1. Reply is stored immediately.
2. HTTP response is returned.
3. Celery task is triggered.
4. Background sentiment analysis runs.
5. Conversation sentiment is updated.

---

# Database

SQLite was used to keep the project lightweight and easy to evaluate.

For production, PostgreSQL would be preferred because it offers:

- Better concurrency
- Better transactions
- Better indexing
- Better scalability

---

# Swagger Documentation

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

![Swagger](screenshots/01-swagger-ui.png)

---

## 2. JWT Authentication

![JWT](screenshots/02-jwt-authentication.png)

---

## 3. Conversation Management

![Conversation](screenshots/03-conversation-management.png)

---

## 4. Customer Support Conversation

![Conversation History](screenshots/04-customer-support-conversation.png)

---

## 5. AI Suggestion API

![AI](screenshots/05-ai-suggestion.png)

---

# Running Project

Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-support-inbox.git
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Seed default admin

```bash
python manage.py seed_data
```

Run server

```bash
python manage.py runserver
```

Run Redis

```bash
redis-server
```

Run Celery

```bash
celery -A support_inbox worker -l info
```

---

# Testing

Run all tests

```bash
python manage.py test
```

---

# Future Improvements

- PostgreSQL
- Docker
- Docker Compose
- Django Channels (WebSockets)
- Server-Sent Events
- OpenTelemetry Monitoring
- CI/CD Pipeline

---

# Author

Sharat Acharja

Backend Developer Technical Assessment
