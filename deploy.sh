#!/usr/bin/env bash

source .venv/bin/activate
git pull
just check
just test
just migrate
sudo systemctl restart nginx gunicorn
