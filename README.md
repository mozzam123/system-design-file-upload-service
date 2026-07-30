# File Upload Service — Learning System Design Through Implementation

A production-inspired **File Upload Service** built to learn **System Design** by implementing real-world architectural patterns instead of just reading about them.

This project intentionally keeps the business logic simple while focusing on the infrastructure and architectural decisions used in scalable backend systems.

The service accepts an image upload, stores it, creates a processing job, publishes that job to a message queue, and processes it asynchronously using background workers.

---

## 🎯 Goal

The purpose of this project is **learning**, not building a feature-rich application.

Instead of implementing authentication, cloud storage, or a frontend, the focus is on understanding **how large-scale systems are designed** and **why these design patterns exist**.

---

## 🏗️ System Architecture

```text
                   POST /upload
                        │
                        ▼
                  +-------------+
                  |   FastAPI   |
                  +------+------+ 
                         │
         Save File + Create Job
                         │
                         ▼
                  +-------------+
                  | PostgreSQL  |
                  +------+------+ 
                         │
                  Publish Task
                         │
                         ▼
                  +-------------+
                  |  RabbitMQ   |
                  +------+------+ 
                         │
                  Background Worker
                         │
                         ▼
                  +-------------+
                  |   Celery    |
                  +------+------+ 
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
Generate Thumbnail               Compress Image
        │                                 │
        └────────────────┬────────────────┘
                         ▼
                 Update Job Status
```

---

## 🚀 Features

- Upload image via REST API
- Store original image locally
- Generate unique filenames using UUID
- Create asynchronous processing jobs
- Background image processing using Celery
- Thumbnail generation
- Job status tracking
- Automatic retry on transient failures
- Parallel processing using multiple workers

---

## 🧠 System Design Patterns Implemented

### 1. Queue-Based Load Leveling

Instead of processing uploaded images inside the API request, jobs are published to RabbitMQ and processed asynchronously.

**Why?**

- Faster API response
- Better scalability
- Handles traffic spikes efficiently

---

### 2. Background Workers

Image processing runs in separate Celery workers rather than inside the FastAPI application.

**Benefits**

- API remains responsive
- Long-running tasks don't block incoming requests
- Independent scaling of workers

---

### 3. Retry Pattern

Transient failures are automatically retried with exponential backoff.

Example:

```
Attempt 1 ❌

↓

Retry

↓

Attempt 2 ❌

↓

Retry

↓

Attempt 3 ✅
```

This improves reliability without requiring user intervention.

---

### 4. Competing Consumers

Multiple Celery workers consume jobs from the same RabbitMQ queue.

```
RabbitMQ

├── Worker 1

├── Worker 2

└── Worker 3
```

Benefits:

- Increased throughput
- Horizontal scalability
- Better resource utilization

---

### 5. Asynchronous Processing

The API immediately returns a response after publishing the task instead of waiting for image processing to finish.

Traditional approach:

```
Client

↓

Upload

↓

Process Image

↓

Return Response
```

Implemented approach:

```
Client

↓

Upload

↓

Publish Task

↓

Return Response

↓

Background Processing
```

---

## 📂 Project Structure

```
file-upload-service/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   ├── workers/
│   └── main.py
│
├── uploads/
├── thumbnails/
│
├── alembic/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- RabbitMQ
- Celery
- Pillow
- Docker Compose

---

## 📡 API Endpoints

### Upload Image

```
POST /upload
```

Uploads an image and creates an asynchronous processing job.

Example Response

```json
{
    "job_id": 1,
    "status": "queued"
}
```

---

### Get Job Status

```
GET /jobs/{job_id}
```

Returns the current processing status of a job.

Possible statuses:

- queued
- processing
- completed
- failed

---

## ⚙️ How It Works

```
Upload Image
      │
      ▼
Save File
      │
      ▼
Create Database Record
      │
      ▼
Publish Task to RabbitMQ
      │
      ▼
Celery Worker Consumes Task
      │
      ▼
Generate Thumbnail
      │
      ▼
Compress Image
      │
      ▼
Update Job Status
```

---

## ▶️ Running the Project

### Clone Repository

```bash
git clone <repository-url>
cd file-upload-service
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Infrastructure

```bash
docker compose up -d
```

### Run Database Migrations

```bash
alembic upgrade head
```

### Start FastAPI

```bash
uvicorn app.main:app --reload
```

### Start Celery Worker

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

---

## 📖 What I Learned

While building this project, I gained hands-on experience with:

- Designing asynchronous APIs
- Message queues and task distribution
- RabbitMQ fundamentals
- Background workers using Celery
- Queue-Based Load Leveling
- Retry mechanisms
- Competing Consumers
- Database migrations with Alembic
- Separation of responsibilities in backend architecture
- Building production-inspired backend services

---

## 🎯 Why This Project Exists

This repository is part of my journey to learn **System Design through implementation**.

Rather than only studying architectural patterns theoretically, I'm building small, focused projects where each project demonstrates one or more design patterns commonly used in production systems.

Current learning roadmap:

- ✅ URL Shortener — Cache-Aside Pattern
- ✅ File Upload Service — Queue-Based Load Leveling, Background Workers, Retry Pattern, Competing Consumers
- ⏳ Notification System — Publisher/Subscriber, Event-Driven Architecture, Bulkhead
- ⏳ AI Chatbot — Saga, CQRS, Circuit Breaker, Sidecar, Ambassador

Each project intentionally stays small so the focus remains on understanding the architecture rather than implementing unnecessary features.

---

## 📜 License

This project is intended for educational purposes and to demonstrate practical System Design concepts through implementation.
