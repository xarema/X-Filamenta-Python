---
Purpose: Complete deployment guide for X-Filamenta-Python
Description: Comprehensive deployment instructions for cPanel, VPS, and Docker environments

File: docs/guides/DEPLOYMENT.md | Repository: X-Filamenta-Python
Created: 2025-12-30
Last modified: 2025-12-30

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public
---

# X-Filamenta-Python Deployment Guide

**Version:** 0.1.0-Beta  
**Last Updated:** 2025-12-30  
**Audience:** System Administrators, DevOps Engineers

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [cPanel Deployment](#cpanel-deployment)
5. [VPS Deployment](#vps-deployment)
6. [Docker Deployment](#docker-deployment)
7. [Environment Variables](#environment-variables)
8. [Production Configuration](#production-configuration)
9. [Post-Deployment](#post-deployment)
10. [Troubleshooting](#troubleshooting)

---

## Overview

X-Filamenta-Python is a Flask-based web application that can be deployed on various hosting environments. This guide covers three primary deployment methods:

- **cPanel**: Shared hosting with Python support
- **VPS**: Virtual Private Server (Ubuntu/Debian/CentOS)
- **Docker**: Containerized deployment

**Choose Your Deployment Path:**
- **For shared hosting users:** [cPanel Deployment](#cpanel-deployment)
- **For VPS/dedicated server users:** [VPS Deployment](#vps-deployment)
- **For containerized environments:** [Docker Deployment](#docker-deployment)

---

## Prerequisites

### General Requirements

**Software:**
- Python 3.11 or higher
- pip (Python package manager)
- Git (for cloning repository)

**Database:**
- SQLite 3.x (included with Python)
- OR PostgreSQL 12+ (recommended for production)
- OR MySQL 8.0+

**Optional but Recommended:**
- Redis (for caching - if available)
- Nginx or Apache (web server)
- SSL certificate

### System Resources

**Minimum:**
- CPU: 1 core
- RAM: 512 MB
- Storage: 1 GB

**Recommended:**
- CPU: 2+ cores
- RAM: 2 GB+
- Storage: 5 GB+

---

## Deployment Options

### Quick Comparison

| Feature | cPanel | VPS | Docker |
|---------|--------|-----|--------|
| **Difficulty** | Easy | Medium | Medium |
| **Control** | Limited | Full | Full |
| **Performance** | Good | Excellent | Excellent |
| **Scalability** | Limited | High | Very High |
| **Maintenance** | Low | Medium | Low |
| **Cost** | Low-Medium | Medium-High | Low-Medium |

---

## cPanel Deployment

### Prerequisites for cPanel

- cPanel account with Python support
- SSH access (recommended)
- Domain or subdomain configured

### Step 1: Access Your cPanel

1. Log in to your cPanel account
2. Navigate to **Setup Python App** (or similar)
3. Verify Python 3.11+ is available

### Step 2: Create Python Application

1. Click **Create Application**
2. Configure:
   - **Python Version:** 3.11+
   - **Application Root:** `/home/username/x-filamenta`
   - **Application URL:** Your domain
   - **Application Startup File:** `run_prod.py`
   - **Application Entry Point:** `app`

### Step 3: Upload Application Files

**Option A: Git (Recommended)**

```bash
# SSH into your server
cd /home/username
git clone https://github.com/yourusername/X-Filamenta-Python.git x-filamenta
cd x-filamenta
```

**Option B: File Manager**

1. Upload ZIP file via cPanel File Manager
2. Extract to `/home/username/x-filamenta`

### Step 4: Install Dependencies

```bash
# Activate virtual environment (created by cPanel)
source /home/username/virtualenv/x-filamenta/3.11/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 5: Configure Environment

Create `.env` file:

```bash
cd /home/username/x-filamenta
nano .env
```

Add configuration (see [Environment Variables](#environment-variables))

### Step 6: Initialize Database

```bash
# Run installation wizard OR manual setup
python -c "from backend.src.extensions import db; db.create_all()"
```

### Step 7: Configure Cache (Optional)

**If Redis is available via cPanel:**

1. Check **Redis** section in cPanel
2. Enable Redis
3. Note connection details
4. Update `.env`:
   ```
   CACHE_TYPE=redis
   CACHE_REDIS_HOST=localhost
   CACHE_REDIS_PORT=6379
   ```

**If Redis is not available:**

```
CACHE_TYPE=filesystem
CACHE_DIR=instance/cache
```

### Step 8: Start Application

1. Return to **Setup Python App**
2. Click **Restart** button
3. Application should now be running

### Step 9: SSL Configuration

1. In cPanel, go to **SSL/TLS**
2. Install SSL certificate (Let's Encrypt recommended)
3. Enable **Force HTTPS Redirect**

### cPanel Troubleshooting

**Application won't start:**
- Check Python version compatibility
- Verify all dependencies installed
- Check error logs in cPanel

**Database connection errors:**
- Verify database exists
- Check database credentials in `.env`
- Ensure SQLite file has write permissions

**Static files not loading:**
- Check `.htaccess` file
- Verify static file paths
- Enable CGI if needed

---

## VPS Deployment

### Prerequisites for VPS

- Ubuntu 22.04 LTS (or similar)
- Root or sudo access
- Domain name pointed to server IP

### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Required Packages

```bash
# Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip -y

# Git
sudo apt install git -y

# Nginx
sudo apt install nginx -y

# Redis (optional)
sudo apt install redis-server -y

# PostgreSQL (optional, recommended)
sudo apt install postgresql postgresql-contrib -y
```

### Step 3: Create Application User

```bash
sudo adduser --system --group --home /var/www/x-filamenta xfilamenta
```

### Step 4: Clone Repository

```bash
sudo -u xfilamenta git clone https://github.com/yourusername/X-Filamenta-Python.git /var/www/x-filamenta/app
```

### Step 5: Create Virtual Environment

```bash
cd /var/www/x-filamenta/app
sudo -u xfilamenta python3.11 -m venv venv
sudo -u xfilamenta venv/bin/pip install -r requirements.txt
```

### Step 6: Configure Database (PostgreSQL)

```bash
# Create database and user
sudo -u postgres psql
CREATE DATABASE x_filamenta;
CREATE USER x_filamenta_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE x_filamenta TO x_filamenta_user;
\q
```

### Step 7: Configure Environment

```bash
sudo -u xfilamenta nano /var/www/x-filamenta/app/.env
```

Add production configuration (see [Environment Variables](#environment-variables))

### Step 8: Create Systemd Service

Create `/etc/systemd/system/x-filamenta.service`:

```ini
[Unit]
Description=X-Filamenta Python Web Application
After=network.target

[Service]
Type=simple
User=xfilamenta
Group=xfilamenta
WorkingDirectory=/var/www/x-filamenta/app
Environment="PATH=/var/www/x-filamenta/app/venv/bin"
ExecStart=/var/www/x-filamenta/app/venv/bin/python run_prod.py

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable x-filamenta
sudo systemctl start x-filamenta
sudo systemctl status x-filamenta
```

### Step 9: Configure Nginx

Create `/etc/nginx/sites-available/x-filamenta`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/x-filamenta/app/frontend/static;
        expires 30d;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/x-filamenta /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 10: Install SSL Certificate

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### VPS Troubleshooting

**Service won't start:**
```bash
# Check logs
sudo journalctl -u x-filamenta -n 50

# Check permissions
ls -la /var/www/x-filamenta/app
```

**Nginx errors:**
```bash
# Check nginx logs
sudo tail -f /var/log/nginx/error.log

# Test config
sudo nginx -t
```

**Database connection issues:**
```bash
# Test PostgreSQL connection
sudo -u postgres psql -c "\l"

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

---

## Docker Deployment

### Prerequisites for Docker

- Docker 20.10+
- Docker Compose 2.0+

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/X-Filamenta-Python.git
cd X-Filamenta-Python
```

### Step 2: Configure Environment

Create `.env` file:

```bash
cp .env.example .env
nano .env
```

Add production values (see [Environment Variables](#environment-variables))

### Step 3: Build and Run

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Step 4: Initialize Database

```bash
# Run migrations
docker-compose exec web flask db upgrade

# Or use installation wizard
# Navigate to http://localhost:5000/install
```

### Step 5: Production Docker Compose

For production, use `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    env_file:
      - .env
    volumes:
      - ./instance:/app/instance
    depends_on:
      - db
      - redis
    restart: always

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: x_filamenta
      POSTGRES_USER: xfilamenta
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    secrets:
      - db_password
    restart: always

  redis:
    image: redis:7-alpine
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/static:/var/www/static:ro
      - certbot_data:/etc/letsencrypt
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
  certbot_data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

Run production:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Docker Troubleshooting

**Container won't start:**
```bash
# Check logs
docker-compose logs web

# Inspect container
docker-compose exec web bash
```

**Database connection:**
```bash
# Check if database is running
docker-compose ps

# Test connection
docker-compose exec db psql -U xfilamenta -d x_filamenta
```

**Network issues:**
```bash
# Inspect network
docker network inspect x-filamenta-python_default

# Restart all services
docker-compose down
docker-compose up -d
```

---

## Environment Variables

### Required Variables

```bash
# Application
SECRET_KEY=generate-secure-random-key-here
FLASK_ENV=production

# Database
DATABASE_URL=sqlite:///instance/x-filamenta_python.db
# OR for PostgreSQL:
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

### Optional Variables

```bash
# Cache (if Redis available)
CACHE_TYPE=redis
CACHE_REDIS_HOST=localhost
CACHE_REDIS_PORT=6379

# Email (for production)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Performance
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### Generating Secure Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate database encryption key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## Production Configuration

### Security Checklist

- [ ] SECRET_KEY is random and secure
- [ ] Database credentials are strong
- [ ] HTTPS/SSL enabled
- [ ] Debug mode disabled (`FLASK_ENV=production`)
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] File upload restrictions set
- [ ] Security headers configured

### Performance Optimization

**Web Server:**
- Use Nginx or Apache as reverse proxy
- Enable gzip compression
- Configure caching headers
- Serve static files directly

**Database:**
- Enable connection pooling
- Add database indexes
- Regular backups
- Query optimization

**Caching:**
- Use Redis if available
- Configure cache expiration
- Cache frequently accessed data

### Monitoring

**Application Logs:**
```bash
# Location varies by deployment
/var/log/x-filamenta/app.log  # VPS
~/x-filamenta/logs/app.log    # cPanel
docker-compose logs web       # Docker
```

**Health Check Endpoint:**
```
GET /health
```

**Metrics to Monitor:**
- Response times
- Error rates
- Database connections
- Memory usage
- Disk space

---

## Post-Deployment

### 1. Run Installation Wizard

Navigate to: `https://yourdomain.com/install`

Follow on-screen instructions:
1. Language selection
2. System requirements check
3. Database configuration
4. Cache configuration (if Redis)
5. Admin user creation
6. Backup restoration (optional)

### 2. Verify Installation

**Check:**
- [ ] Homepage loads correctly
- [ ] Login functionality works
- [ ] Admin panel accessible
- [ ] Static files load
- [ ] Database queries work
- [ ] Email sending works (if configured)

### 3. Configure Backups

**Automated Backup Script:**

```bash
#!/bin/bash
# /var/www/x-filamenta/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/var/backups/x-filamenta
APP_DIR=/var/www/x-filamenta/app

mkdir -p $BACKUP_DIR

# Backup database
sqlite3 $APP_DIR/instance/x-filamenta_python.db ".backup $BACKUP_DIR/db_$DATE.db"

# Backup instance folder
tar -czf $BACKUP_DIR/instance_$DATE.tar.gz -C $APP_DIR instance/

# Remove old backups (keep last 30 days)
find $BACKUP_DIR -type f -mtime +30 -delete
```

**Cron Job:**
```bash
# Run daily at 2 AM
0 2 * * * /var/www/x-filamenta/backup.sh
```

### 4. Set Up Monitoring

**Simple Uptime Monitoring:**
- Use services like UptimeRobot, Pingdom, or StatusCake
- Monitor: `https://yourdomain.com/health`

**Advanced Monitoring:**
- Application Performance Monitoring (APM)
- Log aggregation (ELK stack, Graylog)
- Error tracking (Sentry)

---

## Troubleshooting

### Common Issues

#### 1. Application Won't Start

**Symptoms:** Server returns 502 or 503 errors

**Solutions:**
```bash
# Check application logs
tail -f logs/app.log

# Verify Python version
python --version

# Check dependencies
pip list

# Restart service
sudo systemctl restart x-filamenta  # VPS
# OR restart from cPanel Python App manager
```

#### 2. Database Connection Errors

**Symptoms:** "OperationalError: unable to open database file"

**Solutions:**
```bash
# Check file permissions
ls -la instance/

# Fix permissions
chmod 664 instance/x-filamenta_python.db
chmod 775 instance/

# Verify database URI
echo $DATABASE_URL
```

#### 3. Static Files Not Loading

**Symptoms:** CSS/JS not loading, 404 errors

**Solutions:**
```bash
# Verify static file path
ls -la frontend/static/

# Check nginx configuration
sudo nginx -t

# Collect static files
python -c "from backend.src.app import create_app; create_app()"
```

#### 4. Permission Errors

**Symptoms:** "Permission denied" errors

**Solutions:**
```bash
# Fix ownership (VPS)
sudo chown -R xfilamenta:xfilamenta /var/www/x-filamenta

# Fix permissions
chmod 755 /var/www/x-filamenta/app
chmod 644 /var/www/x-filamenta/app/.env
```

#### 5. High Memory Usage

**Symptoms:** Application slow or crashes

**Solutions:**
- Reduce worker processes in `run_prod.py`
- Enable database connection pooling
- Optimize queries (check with performance benchmarks)
- Add more RAM or upgrade hosting plan

#### 6. HTTPS/SSL Issues

**Symptoms:** "Your connection is not private" warnings

**Solutions:**
```bash
# Renew certificate
sudo certbot renew

# Check certificate expiry
sudo certbot certificates

# Force HTTPS redirect in .env
SESSION_COOKIE_SECURE=True
```

### Getting Help

**Documentation:**
- Project README: `/README.md`
- API Documentation: `/docs/api/`
- Technical Docs: `/docs/technical/`

**Support Channels:**
- GitHub Issues: [Project Issues Page]
- Documentation: [Project Wiki]

**Debug Mode (Development Only):**

```bash
# NEVER use in production!
FLASK_ENV=development
FLASK_DEBUG=True
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor application logs
- Check disk space
- Verify backups

**Weekly:**
- Review error logs
- Check for security updates
- Test backup restoration

**Monthly:**
- Update dependencies
- Review performance metrics
- Security audit

### Updating the Application

```bash
# Backup first!
./backup.sh

# Pull latest code
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations (if any)
flask db upgrade

# Restart application
sudo systemctl restart x-filamenta
```

---

## Appendix

### A. Sample .env File

See `/docs/guides/ENV_TEMPLATE.md`

### B. Nginx Configuration

See `/nginx.conf`

### C. Systemd Service File

See above in VPS deployment section

### D. Docker Compose Production

See above in Docker deployment section

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-12-30  
**Maintained By:** XAREMA Development Team

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

