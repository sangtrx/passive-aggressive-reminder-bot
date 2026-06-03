FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY passive_aggressive_reminder_bot /app/passive_aggressive_reminder_bot
COPY requirements-enterprise.txt /app/
RUN python -m pip install --upgrade pip && \
    pip install -r requirements-enterprise.txt || true
CMD ["python", "-m", "passive_aggressive_reminder_bot.cli"]
