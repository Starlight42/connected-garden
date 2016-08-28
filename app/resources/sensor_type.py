from flask_restful import Resource
from app.models import SensorTypeModel


class SensorType(Resource):
    def get(self, type_name):
        sensor_type = SensorTypeModel.query.filter_by(sensor_type_name=type_name)
        if sensor_type:
            return {sensor_type.id: sensor_type.sensor_type_name}

    def post(self, type_name):
        pass
