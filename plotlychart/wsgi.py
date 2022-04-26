"""
WSGI config for plotlychart project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
import requests
from django.core.wsgi import get_wsgi_application

path = '/var/www/plotlychart'
if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'plotlychart.settings'


#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plotlychart.settings')

application = get_wsgi_application()
