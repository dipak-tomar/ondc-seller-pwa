# ONDC Seller PWA Architecture

## Overview

The ONDC Seller PWA is a full-stack application that enables sellers to manage their products, orders, and inventory on the ONDC network.

## Technology Stack

### Backend
- **Framework:** FastAPI (Python 3.12)
- **Database:** PostgreSQL 16
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Cache/Queue:** Redis 7
- **Task Queue:** Celery
- **Storage:** S3/MinIO
- **Authentication:** JWT with OTP

### Frontend
- **Framework:** React 18 with Vite
- **UI Library:** shadcn/ui + Tailwind CSS
- **State Management:** React Context + LocalForage
- **PWA:** Service Worker with offline support
- **Charts:** Recharts

### Infrastructure
- **Containerization:** Docker Compose
- **CI/CD:** GitHub Actions
- **Monitoring:** Sentry
- **Metrics:** Prometheus (optional)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (PWA)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Products │  │  Orders  │  │Inventory │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Service Worker (Offline Support)             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend API (FastAPI)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │ Products │  │  Orders  │  │  Images  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Webhooks  │  │Analytics │  │  Billing │  │  Notify  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │PostgreSQL│  │  Redis   │  │  MinIO   │
         │          │  │          │  │   (S3)   │
         └──────────┘  └──────────┘  └──────────┘
                              │
                              ▼
                       ┌──────────┐
                       │  Celery  │
                       │  Worker  │
                       └──────────┘
```

## Database Schema

### Users
- id (UUID, PK)
- email (String, unique)
- phone (String, unique)
- name (String)
- plan (String)
- is_active (Boolean)
- created_at (DateTime)
- updated_at (DateTime)

### Stores
- id (UUID, PK)
- user_id (UUID, FK)
- name (String)
- address (Text)
- created_at (DateTime)

### Products
- id (UUID, PK)
- store_id (UUID, FK)
- name (String)
- description (Text)
- sku (String, unique)
- hsn_code (String)
- price (Float)
- mrp (Float)
- stock (Integer)
- category (String)
- is_active (Boolean)
- created_at (DateTime)
- updated_at (DateTime)

### ProductImages
- id (UUID, PK)
- product_id (UUID, FK)
- url (String)
- is_primary (Boolean)
- created_at (DateTime)

### Orders
- id (UUID, PK)
- store_id (UUID, FK)
- customer_name (String)
- customer_phone (String)
- customer_email (String)
- total_amount (Float)
- status (Enum)
- items (JSON)
- created_at (DateTime)
- updated_at (DateTime)

### InventoryEvents
- id (UUID, PK)
- product_id (UUID, FK)
- quantity_change (Integer)
- reason (String)
- created_at (DateTime)

### PricingRules
- id (UUID, PK)
- store_id (UUID, FK)
- name (String)
- rule_type (String)
- discount_percentage (Float)
- conditions (JSON)
- is_active (Boolean)
- created_at (DateTime)

### WebhookEvents
- id (UUID, PK)
- source (String)
- event_type (String)
- payload (JSON)
- processed (Boolean)
- created_at (DateTime)

## API Flow

### Authentication Flow
1. User requests OTP via email/phone
2. OTP stored in OTPStore table with expiration
3. User verifies OTP
4. JWT token generated and returned
5. Token used for subsequent API calls

### Product Upload Flow
1. User creates product via API
2. Product stored in database
3. User requests presigned URL for image upload
4. Image uploaded directly to S3/MinIO
5. Image URL stored in ProductImages table
6. Product synced to ONDC (background job)

### Order Flow
1. Order received via ONDC webhook
2. Webhook stored in WebhookEvents table
3. Background job processes webhook
4. Order created in database
5. Seller confirms order via API
6. Inventory updated
7. Notification sent to customer (WhatsApp/Email)

## Background Jobs (Celery)

- **sync_products_to_ondc:** Sync products to ONDC network
- **process_bulk_upload:** Process CSV bulk uploads
- **send_order_notification:** Send order notifications

## Monitoring

- **Sentry:** Error tracking and performance monitoring
- **Prometheus:** Metrics collection (optional)
- **OpenTelemetry:** Distributed tracing (optional)

## Security

- JWT-based authentication
- CORS enabled for frontend
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy
- Presigned URLs for secure file uploads
- Environment-based secrets management
