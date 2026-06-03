FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only what we need first to leverage Docker layer caching
COPY pyproject.toml requirements-enterprise.txt /app/
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements-enterprise.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

COPY . /app
EXPOSE 8000
CMD ["uvicorn", "passive_aggressive_reminder_bot.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
