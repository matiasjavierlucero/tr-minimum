#!/bin/sh

gunicorn --log-level=debug --timeout 300 --workers 3 --bind 0.0.0.0:80 -m 007 wsgi:app
