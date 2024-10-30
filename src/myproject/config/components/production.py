import os

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
