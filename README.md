# ONDC Seller Booster PWA

A complete Progressive Web App for ONDC sellers to manage their online store.

## Features

- **Authentication**: Email/Phone OTP-based login
- **Product Management**: Manual entry + CSV bulk upload
- **Inventory Tracking**: Real-time stock management with adjustments
- **Order Management**: Order confirmation with automatic stock deduction
- **Analytics Dashboard**: Sales trends and top products with charts
- **PWA Support**: Offline drafts, service worker, installable app
- **Notifications**: WhatsApp & Email notifications (stubs)
- **ONDC Integration**: Catalog sync (stub)
- **Subscription Plans**: Razorpay integration (stub)

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite
- Tailwind CSS + shadcn/ui
- React Router
- TanStack Query
- Zustand (state management)
- Recharts (analytics)
- LocalForage (offline storage)

### Backend
- FastAPI (Python)
- In-memory database (data resets on restart)
- JWT authentication
- Pydantic validation

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.12+
- Poetry (Python package manager)

### Backend Setup

```bash
cd apps/ondc-api
poetry install
poetry run fastapi dev app/main.py
```

Backend will run on http://localhost:8000

### Frontend Setup

```bash
cd apps/ondc-web
npm install
npm run dev
```

Frontend will run on http://localhost:5173

### Test Credentials

The app uses OTP-based authentication. You can use any email or phone number to test:

1. **Email Login:**
   - Enter any email (e.g., `test@example.com`)
   - Click "Send OTP"
   - Check the backend terminal logs for the generated OTP
   - Enter the OTP to login

2. **Phone Login:**
   - Enter any phone number (e.g., `+919876543210`)
   - Click "Send OTP"
   - Check the backend terminal logs for the generated OTP
   - Enter the OTP to login

**Note:** The OTP is printed in the backend console logs since this is a development/demo environment. In production, OTPs would be sent via SMS/Email services.

**Example:**
```
Backend logs will show:
INFO:     Generated OTP for test@example.com: 123456
```

The OTP expires after 10 minutes.

## Project Structure

```
/apps
  /ondc-api     - FastAPI backend
  /ondc-web     - React PWA frontend
/docs           - Documentation
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## Database

This is a proof of concept using an in-memory database. Data will be lost when the backend restarts. For production, integrate with PostgreSQL or another persistent database.

## Deployment

### Backend
Deploy to Fly.io, Railway, or any FastAPI-compatible hosting platform.

### Frontend
Build and deploy to Vercel, Netlify, or any static hosting:

```bash
cd apps/ondc-web
npm run build
# Deploy the dist/ folder
```

## Environment Variables

### Backend (.env in apps/ondc-api)
```
SECRET_KEY=your-secret-key
```

### Frontend (.env in apps/ondc-web)
```
VITE_API_URL=http://localhost:8000/api/v1
```

For production, update VITE_API_URL to your deployed backend URL.

## License

MIT
