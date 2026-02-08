# Deployment Guide

## Table of Contents
- Docker Deployment (Included in Production Template)
- Docker Compose
- Cloud Deployment (AWS, GCP, Azure)
- Environment Configuration
- Production Checklist

## Docker Deployment (Production Template)

The production template includes complete Docker setup:

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build image
docker build -t my-fastapi-app .

# Run container
docker run -p 8000:8000 my-fastapi-app

# Run with environment file
docker run -p 8000:8000 --env-file .env my-fastapi-app
```

## Docker Compose

### docker-compose.yml (Included)

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/appdb
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Usage

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build
```

## Cloud Deployment

### AWS Elastic Beanstalk

**1. Install EB CLI:**
```bash
pip install awsebcli
```

**2. Initialize:**
```bash
eb init -p python-3.11 my-app
```

**3. Create environment:**
```bash
eb create my-env
```

**4. Deploy:**
```bash
eb deploy
```

### AWS ECS (Fargate)

**1. Create ECR repository:**
```bash
aws ecr create-repository --repository-name my-fastapi-app
```

**2. Build and push:**
```bash
docker build -t my-fastapi-app .
docker tag my-fastapi-app:latest {account-id}.dkr.ecr.{region}.amazonaws.com/my-fastapi-app:latest
docker push {account-id}.dkr.ecr.{region}.amazonaws.com/my-fastapi-app:latest
```

**3. Create ECS task definition** (via AWS Console or CLI)

**4. Create ECS service** with load balancer

### Google Cloud Run

```bash
# Build and deploy in one command
gcloud run deploy my-fastapi-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Container Apps

```bash
# Create container app
az containerapp up \
  --name my-fastapi-app \
  --source . \
  --target-port 8000 \
  --ingress external
```

### Heroku

**1. Create Procfile:**
```
web: fastapi run main.py --host 0.0.0.0 --port $PORT
```

**2. Deploy:**
```bash
heroku login
heroku create my-fastapi-app
git push heroku main
```

## Environment Configuration

### Production .env

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security
SECRET_KEY=your-super-secret-key-here-generate-with-openssl-rand-hex-32

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Environment
ENVIRONMENT=production
DEBUG=false

# Optional: External services
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### Secrets Management

**AWS Secrets Manager:**
```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Use in app
secrets = get_secret('my-app-secrets')
SECRET_KEY = secrets['SECRET_KEY']
```

**Google Secret Manager:**
```python
from google.cloud import secretmanager

def get_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')
```

## HTTPS & SSL

### Using Let's Encrypt with Nginx

**docker-compose.yml:**
```yaml
services:
  app:
    # ... your app service

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - app

  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
```

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Load Balancing

### Nginx Load Balancer

```nginx
upstream fastapi_backend {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}

server {
    listen 80;

    location / {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring

### Health Check Endpoint

```python
from fastapi import FastAPI, status

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    # Check database connection
    try:
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
        return {"status": "unhealthy", "database": db_status}

    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0"
    }
```

### Application Monitoring

**Sentry (Error Tracking):**
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment="production",
    traces_sample_rate=1.0
)
```

**Prometheus Metrics:**
```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

## Production Checklist

### Security
- [ ] Use HTTPS in production
- [ ] Set strong SECRET_KEY (32+ random bytes)
- [ ] Configure CORS properly (no `allow_origins=["*"]`)
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Implement request validation
- [ ] Use security headers (helmet.js equivalent)
- [ ] Keep dependencies updated

### Performance
- [ ] Enable database connection pooling
- [ ] Add caching (Redis)
- [ ] Use CDN for static assets
- [ ] Optimize database queries
- [ ] Add database indexes
- [ ] Enable gzip compression
- [ ] Use async operations where appropriate

### Reliability
- [ ] Implement health checks
- [ ] Set up monitoring and alerting
- [ ] Configure logging
- [ ] Add error tracking (Sentry)
- [ ] Implement graceful shutdown
- [ ] Add database migrations
- [ ] Set up backups
- [ ] Configure auto-scaling

### Documentation
- [ ] API documentation (automatically generated at /docs)
- [ ] README with setup instructions
- [ ] Environment variable documentation
- [ ] Deployment guide

### Testing
- [ ] 80%+ test coverage
- [ ] CI/CD pipeline
- [ ] Staging environment
- [ ] Load testing

## CI/CD Example (GitHub Actions)

**.github/workflows/deploy.yml:**
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker image
        run: |
          docker build -t my-app .
          docker push my-registry/my-app:latest
      - name: Deploy to production
        run: |
          # Your deployment commands
```

## Performance Optimization

1. **Use Gunicorn with Uvicorn workers:**
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

2. **Enable HTTP/2**
3. **Use database connection pooling**
4. **Implement caching** (Redis, Memcached)
5. **Add CDN** for static files
6. **Optimize database queries**
7. **Use async** for I/O operations
