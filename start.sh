#!/usr/bin/env bash
# Iniciar panel manualmente con python3
CURRENT_DIR=$(dirname "$(readlink -f "$0")")
cd "$CURRENT_DIR"

if [ -d "venv" ]; then
    ./venv/bin/python3 app.py
else
    python3 app.py
fi
