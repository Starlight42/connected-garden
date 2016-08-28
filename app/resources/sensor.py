from flask import request
from flask_restful import Resource

from app.models import db, SensorModel, SensorTypeModel


class Sensor(Resource):
    """This endpoint allow to manage temperature sensors"""
    sensor_types = []

    def __init__(self):
        pass

    """ Get a sensor value"""
    def get(self, sensor_id=None):
        sensor_type_id = self.get_sensor_type()

        if sensor_id:
            json_data = request.get_json()
            sensor = SensorModel.query.filter_by(name=json_data['sensor_name'],
                                                 sensor_type_id=sensor_type_id).first()
            if sensor:
                response = sensor.to_json()
            else:
                response = {sensor_id: """No sensor with this name in DB.
                Please create one with a post request first."""}
        else:
            # Get all sensor matching id sensor_type_id
            response = {sensor_id: """No data received or data not JSON"""}

        return response

    """ Add a temperature sensor given is sensor_id"""
    def post(self):
        return self.create_or_update_sensor(request.get_json(silent=True), 'POST')

    """Update a temperature sensor ID and/or value"""
    def put(self, sensor_id):
        return self.create_or_update_sensor(request.get_json(silent=True), 'PUT')

    def create_or_update_sensor(self, json_data, http_verb, sensor_id=None):
        sensor_type_id = self.get_sensor_type()

        if json_data is None:
            response = {'error': 'Data not JSON or header Content-Type not set to application/json'}
        else:
            response = ''
            if http_verb is 'POST':
                response = self.create_sensor(json_data, sensor_type_id)
            elif http_verb is 'PUT':
                response = self.update_sensor(json_data, sensor_type_id)
        return response

    def create_sensor(self, json_sensor_data, sensor_type_id):
        """Create sensor in DB :
            First we create an object model describing our db entry,
            then we add it to the db and commit to validate the action.
            After that we are getting the last inserted id and return the
            result as a confirmation.
        """
        prob = SensorModel(json_sensor_data['sensor_name'], sensor_type_id, json_sensor_data['sensor_value'])
        db.session.add(prob)
        db.session.commit()

        prob_list = SensorModel.query.filter_by(id=prob.id).first()
        return prob_list.to_json()

    def update_sensor(self, json_sensor_data, sensor_type_id):
        prob = SensorModel.query.filter_by(name=json_sensor_data['sensor_name']).first()
        if prob:
            prob.sensor_type_id = sensor_type_id
            prob.name = json_sensor_data['sensor_name']
            prob.value = json_sensor_data['sensor_value']
            db.session.add(prob)
            db.session.commit()
            response = prob.to_json()
        else:
            response = {json_sensor_data['sensor_name']: """No sensor with this name in DB.
            Please create one with a post request first."""}

        return response

    def get_sensor_type(self):
        sensor_types = SensorTypeModel.query.all()
        tmp_types_list = []
        sensor_id = None

        for sensor_type in sensor_types:
            tmp_types_list.append(sensor_type.to_json())

        self.sensor_types = tmp_types_list

        print('Sensor types : \n{}'.format(self.sensor_types))

        if 'humi' in request.path:
            sensor_id = self.get_sensor_type_id('humi')
        elif 'temp' in request.path:
            sensor_id = self.get_sensor_type_id('temp')

        return sensor_id

    def get_sensor_type_id(self, sensor_type_name):
        sensor_id = None

        for ss_type in self.sensor_types:
            if sensor_type_name.capitalize() is ss_type.type_name:
                sensor_id = ss_type.type_id

        return sensor_id

    def get_sensor_type_name(self, sensor_type_id):
        sensor_name = None

        if sensor_type_id in self.sensor_types:
            sensor_name = self.sensor_types[sensor_type_id]

        return sensor_name
