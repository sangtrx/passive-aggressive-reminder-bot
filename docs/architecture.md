# Architecture Overview (Enterprise)

This project is intentionally small and modular. For enterprise deployments we
recommend the following architecture decisions implemented in the repo:

- Containerize the CLI/API with the provided `Dockerfile` and orchestrate via
  `docker-compose.yml` for local testing.
- Provide an ASGI `FastAPI` factory (`passive_aggressive_reminder_bot.api`) to
  expose reminder generation over HTTP when `requirements-enterprise.txt` is
  installed.
- Optional SQL storage via `passive_aggressive_reminder_bot.enterprise_storage`.
- Centralized logging configuration via `passive_aggressive_reminder_bot.logging_config`.
