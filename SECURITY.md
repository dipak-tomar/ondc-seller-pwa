# Security Guidelines

## Development vs Production

This repository contains **development defaults** for local testing. These are NOT secure for production use.

### Development Defaults (DO NOT USE IN PRODUCTION)

The following files contain development defaults:
- `apps/ondc-api/app/core/config.py` - Default configuration values
- `infra/docker-compose.yml` - Local development services

These defaults include:
- PostgreSQL: `ondc` / `ondc_dev_password`
- MinIO: `minioadmin` / `minioadmin123`
- Secret Key: `your-secret-key-change-in-production`

### Production Deployment

**REQUIRED:** Override ALL sensitive values via environment variables:

1. Generate a strong SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. Use secure database credentials:
```bash
export DATABASE_URL="postgresql+psycopg://user:secure_password@host:5432/db"
```

3. Use production S3/R2 credentials:
```bash
export S3_ACCESS_KEY="your-production-key"
export S3_SECRET_KEY="your-production-secret"
```

4. Set all other credentials via environment variables (see `.env.example`)

### Environment Variables

All sensitive configuration is loaded from environment variables via Pydantic Settings.

Create a `.env` file (NOT committed to git) with production values:
```bash
cp apps/ondc-api/.env.example apps/ondc-api/.env
# Edit .env with your production values
```

### CI/CD

Store secrets in your CI/CD platform's secret management:
- GitHub Actions: Repository Secrets
- GitLab CI: CI/CD Variables
- Other platforms: Use their secret management features

### Never Commit

- `.env` files with real credentials
- API keys or tokens
- Database passwords
- Private keys

The `.gitignore` file is configured to exclude `.env` files.
