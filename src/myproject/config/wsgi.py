# myproject/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

# Set the settings module for your Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create the WSGI application callable
application = get_wsgi_application()
