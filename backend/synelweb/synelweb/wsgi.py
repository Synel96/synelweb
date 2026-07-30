"""
WSGI config for synelweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "synelweb.settings")

application = get_wsgi_application()

if os.environ.get("RUN_EXCHANGE_RATE_SCHEDULER", "true").lower() != "false":
    from packages.scheduler import start as start_exchange_rate_scheduler

    start_exchange_rate_scheduler()
