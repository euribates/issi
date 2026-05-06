#!/usr/bin/env bash

source .venv/bin/activate
git pull
just check
sudo systemctl restart nginx gunicorn
