#!/bin/bash
nginx
cd /app && nohup ./venv/bin/python app.py run > /tmp/log.txt 2>&1 &
tail -f /var/log/nginx/access.log & tail -f /var/log/nginx/error.log & tail -f /tmp/log.txt