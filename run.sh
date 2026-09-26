#!/usr/bin/env bash
set -e
export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)"
python -m uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8000}"
