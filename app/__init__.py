from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from app import config


app = Flask(__name__)
api = Api(app, errors=config.ERRORS)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_PATH
db = SQLAlchemy(app)
from app.resources import (Sensor, SensorType)

api.add_resource(Sensor, '/sensor/temp/', '/sensor/humi/')
api.add_resource(SensorType, '/sensor/type/')
