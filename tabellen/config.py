import os

import connexion
from flask_pymongo import PyMongo

connexion_app = connexion.App(__name__, specification_dir="specs/")

app = connexion_app.app
app.config["MONGO_URI"] = os.environ["MONGO_URI"]

mongo = PyMongo(app)
