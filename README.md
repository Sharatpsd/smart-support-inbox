# Smart Customer Support Inbox Engine

A backend system for managing customer support conversations, built with Django and Django REST Framework. This project includes JWT authentication, conversation management, message history, AI-based reply suggestions, conversation locking, and asynchronous sentiment analysis using Celery.

---

## Tech Stack

- Python 3.11
- Django 5
- Django REST Framework
- JWT Authentication (Simple JWT)
- Celery
- Redis
- SQLite (Development)
- Docker (Redis)

---

## Features

### Authentication

- JWT Authentication
- Protected API endpoints

---

### Conversation Management

- List conversations
- Pagination
- Search by customer name
- Filter by conversation status

Example:

```
GET /api/conversations/?search=John&status=open
```

---

### Message History

Retrieve all messages for a conversation.

```
GET /api/conversations/<id>/messages/
```

---

### Reply API

Send an agent reply to a conversation.

```
POST /api/conversations/<id>/reply/
```

Example Request

```json
{
    "message": "We are reviewing your request."
}
```

---

### Mock AI Reply Suggestion

Generate a rule-based reply suggestion.

```
POST /api/conversations/<id>/suggest-reply/
```

Example Request

```json
{
    "message": "Customer wants refund"
}
```

---

### Conversation Locking

Prevent multiple agents from replying simultaneously.

Endpoints

```
POST /api/conversations/<id>/lock/

POST /api/conversations/<id>/unlock/

GET /api/conversations/<id>/lock-status/
```

---

### Background Sentiment Analysis

Every new reply triggers a Celery task that analyzes conversation sentiment.

Possible values

- Positive
- Neutral
- Negative

---

## Installation

Clone the repository

```bash
git clone https://github.com/Sharatpsd/smart-support-inbox.git

cd smart-support-inbox
```

Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database

Run migrations

```bash
python manage.py migrate
```

Seed sample data

```bash
python manage.py seed_data
```

---

## Run Project

```bash
python manage.py runserver
```

---

## Run Tests

```bash
python manage.py test
```

---

## Celery

Start Redis

```bash
docker run -d --name support-redis -p 6379:6379 redis:7-alpine
```

Run Celery Worker

```bash
celery -A config worker -l info --pool=solo
```

---

## API Endpoints

| Method | Endpoint |
|---------|----------|
| POST | /api/token/ |
| POST | /api/token/refresh/ |
| GET | /api/conversations/ |
| GET | /api/conversations/<id>/messages/ |
| POST | /api/conversations/<id>/reply/ |
| POST | /api/conversations/<id>/suggest-reply/ |
| POST | /api/conversations/<id>/lock/ |
| POST | /api/conversations/<id>/unlock/ |
| GET | /api/conversations/<id>/lock-status/ |

---

## Default Admin User

```
Username: admin
Email: admin@test.com
Password: admin123
```

---

## Project Structure

```
config/
conversations/
messaging/
locks/
analytics/
ai_engine/
manage.py
requirements.txt
README.md
```

---

## Running Notes

- Redis is required for asynchronous background tasks.
- During automated tests, Celery executes tasks eagerly to avoid requiring a running Redis instance.
- SQLite is used for development. PostgreSQL can be configured by updating the database settings.

---

## Author

**Sharat Acharja**

GitHub:
https://github.com/Sharatpsd
