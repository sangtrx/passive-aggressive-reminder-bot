Enterprise expansion notes

- Added optional FastAPI app factory (`passive_aggressive_reminder_bot.api`) to
  serve reminders via HTTP.
- Added `requirements-enterprise.txt` for optional deps (FastAPI, SQLAlchemy,
  Prometheus client) to avoid changing base install.
- Added Dockerfile and docker-compose for containerized deployments.

To opt-in to enterprise features:

1. pip install -r requirements-enterprise.txt
2. run `python -m passive_aggressive_reminder_bot.api` via an ASGI server
