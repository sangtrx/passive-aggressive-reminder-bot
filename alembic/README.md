Alembic integration for SQLModel

Usage:

1. Install alembic and SQLModel dependencies:

```bash
pip install alembic sqlmodel asyncpg
```

2. Configure DATABASE_URL env var (example uses sqlite aiosqlite):

```bash
export DATABASE_URL=sqlite+aiosqlite:///./enterprise.db
```

3. Create a migration (autogenerate):

```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

Note: This env is a minimal scaffold to support SQLModel metadata autogeneration
for async engines. Review generated migrations before applying to production.
