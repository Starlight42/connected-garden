from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from app import config


app = Flask(__name__)
api = Api(app, errors=config.ERRORS)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_PATH
db = SQLAlchemy(app)
from app.resources import (Sensor, SensorType)

api.add_resource(Sensor, '/api/sensors/<int:sensor_id>/', '/api/sensors/<int:sensor_type_id>/', '/api/sensors/')
api.add_resource(SensorType, '/api/sensortypes/<int:type_id>', '/api/sensortypes/')

"""
Sensors :
    GET :
        /api/sensors/<int:sensor_id>/ -> return sensor of id sensor_id
        (/api/sensors/<int:sensor_type_id>/ -> return all sensors of type type_id) TODO: find a better url for this GET
        /api/sensors/ -> return all sensors

    POST :
        /api/sensors/ req: json object data {'sensor_name': 'xx', 'sensor_value': 'xx', 'sensor_type_id': 'xx'}
                      -> Create and return new sensor object

    PUT :
        /api/sensors/<int:sensor_id>/ req: json object data {'sensor_id': 'xx', 'sensor_value': 'xx', 'sensor_type_id': 'xx'}
                                      -> Bulk update (erase and recreate) of sensor sensor_id

    PATCH :
        /api/sensors/<int:sensor_id>/ req: json object data {'sensor_value': 'xx'}
                                      -> Update sensor of id sensor_id value

    DELETE :
        /api/sensors/<int:sensor_id>/ -> Delete sensor sensor_id


SensorTypes:
    GET :
        /api/sensortypes/<int:type_id> -> Return a sensor type of id type_id
        /api/sensortypes/ -> Return all existing sensor types

    POST :
        /api/sensortypes/ req: json object data {'sensor_type_name': 'xx'}
                          -> Create and return new sensor type

    PUT/PATCH :
        /api/sensortypes/<int:type_id> req: json object data {'sensor_type_name': 'xx'}
                                       -> Update sensor_type of id type_id and return it

    DELETE :
        /api/sensortypes/<int:type_id> -> Delete sensor_type of id type_id
"""
