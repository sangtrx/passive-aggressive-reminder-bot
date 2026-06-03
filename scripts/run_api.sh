#!/usr/bin/env bash
# Simple helper to run the FastAPI app with uvicorn when enterprise deps are installed
set -euo pipefail

UVICORN=${UVICORN:-uvicorn}
$UVICORN passive_aggressive_reminder_bot.api:create_app --host 0.0.0.0 --port 8000
