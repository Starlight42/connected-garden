from flask_restful import Resource
from app.models import SensorTypeModel


class SensorType(Resource):
    sensor_types = []

    def __init__(self):
        self.set_sensor_type()

    def get(self, type_name):
        sensor_type = SensorTypeModel.query.filter_by(sensor_type_name=type_name)
        if sensor_type:
            return {sensor_type.id: sensor_type.sensor_type_name}

    def post(self, type_name):
        pass

    def set_sensor_type(self):
        sensor_types = SensorTypeModel.query.all()
        tmp_types_list = []

        for sensor_type in sensor_types:
            tmp_types_list.append(sensor_type.to_json())

        self.sensor_types = tmp_types_list

    def get_sensor_type_id(self, sensor_type_name):
        sensor_id = None

        for ss_type in self.sensor_types:
            if sensor_type_name.upper() == ss_type['type_name']:
                sensor_id = ss_type['type_id']

        return sensor_id

    def get_sensor_type_name(self, sensor_type_id):
        sensor_name = None

        for ss_type in self.sensor_types:
            if sensor_type_id == ss_type['type_id']:
                sensor_name = ss_type['type_name']

        return sensor_name
