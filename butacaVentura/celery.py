import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "butacaVentura.settings")

app = Celery("butacaVentura")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()