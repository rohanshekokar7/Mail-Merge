# Mail Merge Platform

A production-quality web-based Mail Merge and Email Campaign Automation platform.

## Overview
This platform replicates the traditional mail merge workflow, modernized into a SaaS-style web application. It features campaign management, spreadsheet-based personalization, scheduled sending, throttling, reply detection, automated follow-ups, email tracking, analytics, and role-based administration.

## Tech Stack
* **Frontend:** Next.js (App Router), React, TypeScript, Tailwind CSS, shadcn/ui
* **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Redis, Celery
* **Email:** Abstraction supporting SMTP (Mailpit for local dev), SES, SendGrid, etc.
* **Infrastructure:** Docker, Docker Compose

## Folder Structure
* `frontend/`: Next.js web application
* `backend/`: FastAPI application and Celery workers
* `infrastructure/`: Infrastructure configurations (Docker)
* `docs/`: Documentation and architecture diagrams
* `scripts/`: Development and deployment scripts

## Prerequisites
* Docker and Docker Compose

## Environment Setup
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Update the `.env` file with your specific configuration if necessary.

## Docker Setup
To start the entire platform locally:
```bash
docker compose up --build
```

To stop the platform:
```bash
docker compose down
```

## Services & URLs
* **Frontend:** http://localhost:3000
* **Backend API / Health Check:** http://localhost:8000/health
* **Backend API Docs:** http://localhost:8000/docs
* **Mailpit (Local Email Testing UI):** http://localhost:8025
