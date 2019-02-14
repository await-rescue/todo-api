#!/bin/sh
# might not use this unless doing migrations 
source venv/bin/activate
flask db upgrade
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - todo:app