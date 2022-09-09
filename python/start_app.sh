#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:5001 --workers 4 --threads 1 app.api.application
