from flask import request
from flask_restful import Resource


class TemperatureSensor(Resource):
    """This endpoint allow to manage temperature sensors"""
    sensors = {}

    """ Get a temperature sensor value"""
    def get(self, sensor_id):
        if sensor_id in self.sensors.keys():
            response = {sensor_id: self.sensors[sensor_id]}
        else:
            response = {sensor_id: """No temperature sensor with this ID in DB.
            Please create one with a post request first."""}
        return response

    """ Add a temperature sensor given is sensor_id"""
    def post(self, sensor_id):
        return self.create_or_update_sensor(sensor_id, request.get_json(silent=True), 'POST')

    """Update a temperature sensor ID and/or value"""
    def put(self, sensor_id):
        return self.create_or_update_sensor(sensor_id, request.get_json(silent=True), 'PUT')

    def create_or_update_sensor(self, sensor_id, json_data, flag):
        if json_data is None:
            response = {'error': 'Data not JSON or header Content-Type not set to application/json'}
        else:
            response = ''
            if flag is 'POST':
                response = self.create_sensor(sensor_id, json_data)
            elif flag is 'PUT':
                response = self.update_sensor(sensor_id, json_data)
        return response

    def create_sensor(self, sensor_id, json_sensor_data):
        if sensor_id not in self.sensors.keys():
            self.sensors[sensor_id] = json_sensor_data['sensor_value']
            response = {sensor_id: self.sensors[sensor_id]}
        else:
            response = {sensor_id: """A temperature sensor with the same ID exists in DB.
            Please use PUT to update it or change the sensor name"""}
        return response

    def update_sensor(self, sensor_id, json_sensor_data):
        if self.sensors.pop(sensor_id, None) is not None:
            self.sensors[json_sensor_data['sensor_id']] = json_sensor_data['sensor_value']
            response = {json_sensor_data['sensor_id']: self.sensors[json_sensor_data['sensor_id']]}
        else:
            response = {sensor_id: """No temperature sensor found with this ID"""}
        return response
