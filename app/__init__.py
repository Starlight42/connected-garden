from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
from app.endpoints import Sensors, TemperatureSensor

api.add_resource(TemperatureSensor, '/temp/<string:sensor_id>')
api.add_resource(Sensors, '/sensors')
