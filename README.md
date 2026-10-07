# Vinay Docker Expense Dashboard

A personal expense dashboard built with Flask, PostgreSQL,
Nginx, and Docker Compose.

Developed and tested locally in Parrot OS running in VMware.

## Features

- Dashboard layout with sidebar navigation
- Built-in SVG finance illustration
- Monthly spending total
- All-time expense count and spending total
- Expense entry form and history table
- PostgreSQL persistent storage
- Local HTTPS using a self-signed certificate
- Database backup and restore workflow

## Architecture

Browser → HTTPS Nginx → Flask/Gunicorn → PostgreSQL

## Requirements

- Docker Engine
- Docker Compose
- OpenSSL
- Git

## Local setup

Clone this repository and enter its directory.

Create the environment file:

```bash
cp .env.example .env
```

Edit .env and replace the placeholder password:

```bash
nano .env
chmod 600 .env
```

Generate a local certificate:

```bash
mkdir -p nginx/certs

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/certs/localhost.key \
  -out nginx/certs/localhost.crt \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

chmod 600 nginx/certs/localhost.key
```

Validate and start:

```bash
sudo docker compose config --quiet
sudo docker compose up -d --build
```

Open https://localhost:8443 in a browser on the Docker host.

The certificate is self-signed, so a browser warning may appear.
Only accept an exception for your own local test certificate.

HTTP at http://localhost:8080 redirects to the HTTPS address.

## Service checks

```bash
sudo docker compose ps
sudo docker compose logs --tail=50 app nginx
```

## Persistence test

Add an expense, then recreate the containers:

```bash
sudo docker compose down
sudo docker compose up -d
```

Refresh the dashboard and confirm the expense remains.

Do not use down --volumes unless you intend to delete the database data.

## Database backup

```bash
sudo docker compose exec -T db pg_dump -U expenseuser -d expenses > expenses-backup.sql
```

## Restore test

Create a separate test database once:

```bash
sudo docker compose exec db createdb -U expenseuser expenses_restore_test
```

Restore the backup:

```bash
sudo docker compose exec -T db psql -v ON_ERROR_STOP=1 -U expenseuser -d expenses_restore_test < expenses-backup.sql
```

Check the restored data:

```bash
sudo docker compose exec db psql -P pager=off -U expenseuser -d expenses_restore_test -c "SELECT * FROM expenses;"
```

## Security and limitations

- This is a local learning project, not a production application.
- Host ports are bound to 127.0.0.1.
- HTTPS uses a self-signed certificate, not a publicly trusted certificate.
- Authentication and CSRF protection are not implemented.
- .env, certificate files, and SQL backups are excluded from Git.
- The sidebar links navigate to sections on the same page.

## Credits

Built by Vinay with AI-assisted starter code and design,
followed by hands-on deployment and testing.
