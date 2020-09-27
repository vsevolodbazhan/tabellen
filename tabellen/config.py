import connexion
from flask_pymongo import PyMongo

DATABASE_NAME = "tabellen"
MONGO_URI = f"mongodb://localhost:27017/{DATABASE_NAME}"

connexion_app = connexion.App(__name__, specification_dir="specs/")

app = connexion_app.app
app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)
