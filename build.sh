#!/usr/bin/env bash
# Render build script: install dependencies, gather static files, set up the
# database, and seed demo data so the live site always has content.
set -o errexit  # Stop immediately if any command fails.

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_demo   # Idempotent: repopulates EVRi data on each deploy.