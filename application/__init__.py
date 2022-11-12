# look into for initializations
from flask import Flask #import flask class
from config import Config
from flask_mongoengine import MongoEngine
from flask_restx import Api

api = Api()
app = Flask(__name__)  # to identify current application rendered to flask
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)
# api.init_app(app)

from application import routes

