"""
An application configuration. All adjustments should be done
in `settings` module.
"""

import connexion
from celery import Celery
from flask_pymongo import PyMongo

from .settings import settings

__all__ = ["connexion_app", "mongo", "celery"]

connexion_app = connexion.App(
    __name__, specification_dir=settings.SPECIFICATION_DIRECTORY
)

app = connexion_app.app
app.config["MONGO_URI"] = settings.MONGO_URI

celery = Celery(settings.CELERY_APP_NAME, broker=settings.REDIS_URL)
mongo = PyMongo(app)
