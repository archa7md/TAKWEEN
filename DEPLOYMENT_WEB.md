# TAKWEEN Web Deployment

## Local
Docker Desktop: `docker compose up --build`
Open: `http://localhost:8000`

## Production
Deploy this folder to a container host supporting Docker (for example a managed container service). Expose port 8000 and configure HTTPS at the platform/reverse proxy layer. Point `app.takween.ai` DNS to the deployment endpoint.

The current MVP has no production authentication, billing, database persistence, secrets management, or multi-tenant isolation. Those are required before public commercial launch.
