# Expense Dashboard

A containerized expense-tracking web application with PostgreSQL,
local HTTPS, and a temporary public demo through Cloudflare Tunnel.

## Features

- Add expenses with an amount and category.
- View expense history.
- View expense totals on the dashboard.
- Access the application through a local HTTPS endpoint.

## Components

- Application served using Gunicorn.
- PostgreSQL database.
- Container services managed using Compose.
- Podman socket used for Docker-compatible Compose commands.
- Cloudflare Tunnel used for a temporary public demo.

## Architecture

Browser → HTTPS service → Application → PostgreSQL

Public demo:
Browser → Cloudflare Tunnel → Local HTTPS service → Application → PostgreSQL

## Run Locally

From the project folder:

    docker compose up -d --build
    docker compose ps

For the local configuration demonstrated in this project:

- HTTP: http://127.0.0.1:8080
- HTTPS: https://127.0.0.1:8443

The HTTP endpoint redirects to HTTPS.

## Local HTTPS

The browser displayed a certificate warning during local testing.
A certificate exception was accepted for the local demonstration.

## Public Demo

The application was tested through a temporary Cloudflare Quick Tunnel.

The demo depends on the local machine, containers, and tunnel
remaining running. It is not permanent cloud hosting.

Use sample data only.

## Testing

- Dashboard loaded successfully in Firefox.
- A ₹150 food expense appeared in the dashboard and expense history.
- Public access was tested through the tunnel URL.

## Troubleshooting

### Compose could not connect to the Podman socket

The issue was resolved by starting the user-level socket and
setting the socket address in the terminal:

    systemctl --user start podman.socket
    export DOCKER_HOST="unix://$XDG_RUNTIME_DIR/podman/podman.sock"

The Compose startup command was then retried.

## Screenshots

Add screenshots showing:


- ### Dashboard overview
- 
  **Screenshot 2026-10-07 at 08-41-40 Vinay Expense Dashboard.png**

### Add expense
**Screenshot 2026-10-07 at 10-13-21 add-expense.png**


### Expense history
**Screenshot 2026-10-07 at 10-14-18 Vinay Expens-history.png**

Remove personal information before publishing screenshots.

## Planned Improvements

- Monthly budget tracking.
- Category charts.
- Edit and delete expense controls.
- CSV export.
- Demo-data mode.
