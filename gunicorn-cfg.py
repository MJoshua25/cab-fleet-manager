# -*- encoding: utf-8 -*-

import os
import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1

# Logging configuration
# You can override defaults via env vars:
# - GUNICORN_LOG_DIR: directory for log files
# - GUNICORN_ACCESS_LOG: full path to access log
# - GUNICORN_ERROR_LOG: full path to error log
LOG_DIR = os.getenv('GUNICORN_LOG_DIR', os.path.abspath(os.path.join(os.getcwd(), 'logs')))
try:
    os.makedirs(LOG_DIR, exist_ok=True)
except Exception:
    # Fallback to /tmp if logs directory cannot be created
    LOG_DIR = '/tmp'

accesslog = os.getenv('GUNICORN_ACCESS_LOG', os.path.join(LOG_DIR, 'gunicorn.access.log'))
errorlog = os.getenv('GUNICORN_ERROR_LOG', os.path.join(LOG_DIR, 'gunicorn.error.log'))

timeout = 300
loglevel = 'info'
capture_output = True
enable_stdio_inheritance = True
