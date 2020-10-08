import os

import connexion
from celery import Celery
from flask_pymongo import PyMongo

__all__ = ["connexion_app", "mongo", "celery"]

connexion_app = connexion.App(__name__, specification_dir="specs/")

app = connexion_app.app
app.config["MONGO_URI"] = os.environ["MONGO_URI"]

celery = Celery("tabellen", broker=os.environ["REDIS_URL"])
mongo = PyMongo(app)
