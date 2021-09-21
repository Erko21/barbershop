#!/bin/bash
echo Migrations starting
aerich upgrade
echo Migrations finished
echo Starting server
poetry run uvicorn app.main:app --workers 1 --host 0.0.0.0 --port 8089
