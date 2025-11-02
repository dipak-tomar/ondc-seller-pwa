# Setup Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Node.js 20+
- Poetry (Python package manager)

## Backend Setup

1. Navigate to the backend directory:
```bash
cd apps/ondc-api
```

2. Install dependencies:
```bash
poetry install
```

3. Start infrastructure services:
```bash
cd ../../infra
docker compose up -d
```

4. Run database migrations:
```bash
cd ../apps/ondc-api
poetry run alembic upgrade head
```

5. Start the backend server:
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd apps/ondc-web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql+psycopg://ondc:ondc_dev_password@localhost:5432/ondc_seller
REDIS_URL=redis://localhost:6379/0

S3_ENDPOINT_URL=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin123
S3_BUCKET_NAME=ondc-products

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_FROM=+14155238886

POSTMARK_API_KEY=your_postmark_key
POSTMARK_FROM_EMAIL=noreply@ondcseller.com

RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

SENTRY_DSN=your_sentry_dsn
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Accessing Services

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **MinIO Console:** http://localhost:9001 (minioadmin / minioadmin123)
- **PostgreSQL:** localhost:5432 (ondc / ondc_dev_password)
- **Redis:** localhost:6379

## Running Celery Worker

```bash
cd apps/ondc-api
poetry run celery -A app.services.celery_app worker --loglevel=info
```

## Running Tests

### Backend
```bash
cd apps/ondc-api
poetry run pytest
```

### Frontend
```bash
cd apps/ondc-web
npm run test
```

## Linting

### Backend
```bash
cd apps/ondc-api
poetry run ruff check .
```

### Frontend
```bash
cd apps/ondc-web
npm run lint
npm run typecheck
```

## Building for Production

### Backend
```bash
cd apps/ondc-api
poetry build
```

### Frontend
```bash
cd apps/ondc-web
npm run build
```

## Troubleshooting

### Database connection issues
- Ensure PostgreSQL is running: `docker compose ps`
- Check database credentials in .env file
- Verify database exists: `docker compose exec postgres psql -U ondc -d ondc_seller`

### MinIO connection issues
- Ensure MinIO is running: `docker compose ps`
- Access MinIO console at http://localhost:9001
- Create bucket manually if needed

### Redis connection issues
- Ensure Redis is running: `docker compose ps`
- Test connection: `redis-cli ping`
