# superset_config.py

import os

# Define a strong SECRET_KEY
# You MUST change this in production. Use a strong, random key.
# Example: openssl rand -base64 42
SECRET_KEY = 'WK9dTYj8Q074zukBzDyYmMnQ6+4W24glBzLXFFXjAf+qk0reVhYfNycv'

# The SQLAlchemy URI for Superset's metadata database (using your 'postgres' service)
SQLALCHEMY_DATABASE_URI = 'postgresql://airflow:airflow@postgres:5432/superset_metadata_db'


# Other common Superset configurations (optional, but good to have a base)
# Feature flags (uncomment and set to True to enable features)
# FEATURE_FLAGS = {
#     "EMBEDDING": True,
#     "ALERT_REPORTS": True,
#     "DASHBOARD_CROSS_FILTERS": True,
# }

# Default timezone for the web server
# TIME_GRAIN_TEXT_LABELS = True
# FLASK_APP_LOCALE = "en"
# FLASK_APP_LANG = "en"

# Celery (if you use a Celery broker for async tasks, e.g., for alerts/reports)
# from celery.schedules import crontab
# CELERY_CONFIG = {
#     'broker_url': 'redis://redis:6379/0', # Example if you have a Redis service
#     'result_backend': 'redis://redis:6379/0',
#     'worker_prefetch_multiplier': 1,
#     'task_acks_late': True,
#     'beat_schedule': {
#         'reports.digest_email_hourly': {
#             'task': 'reports.digest_email_hourly',
#             'schedule': crontab(minute='0', hour='*'),
#         },
#     },
# }

# Cache configuration (optional)
# CACHE_CONFIG = {
#     'CACHE_TYPE': 'RedisCache',
#     'CACHE_DEFAULT_TIMEOUT': 300,
#     'CACHE_KEY_PREFIX': 'superset_cache',
#     'CACHE_REDIS_HOST': 'redis',
#     'CACHE_REDIS_PORT': 6379,
#     'CACHE_REDIS_DB': 1,
# }

# CORS settings (if you need to allow cross-origin requests)
# CORS_OPTIONS = {
#   'origins': ['http://localhost:3000'], # Replace with your frontend origin
#   'supports_credentials': True,
#   'allow_headers': ['*']
# }

# Default role for new users
# AUTH_USER_REGISTRATION_ROLE = "Public"