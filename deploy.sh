#!/usr/bin/env bash

source .venv/bin/activate
git pull
just check
systemctl restart nginx gunicorn
