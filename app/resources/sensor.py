from flask import request
from flask_restful import Resource

from app.models import db, SensorModel
import app.resources


class Sensor(Resource):
    """This endpoint allow to manage sensors"""
    sensor_type = None

    def __init__(self):
        self.sensor_type = app.resources.SensorType()

    """ Get a sensor value"""
    def get(self, sensor_type_id=None, sensor_id=None):
        # if sensor_type_id:
        # We fetch and return all sensors of type sensor_type_id
        # get_sensors_of type(sensor_type_id)
        # elif sensor_id:
        # We fetch and return sensor with id sensor_id
        # get_sensor(sensor_id)
        # else:
        # We fetch and return all sensors
        # get_sensors()

        json_data = request.get_json()
        sensor = SensorModel.query.filter_by(name=json_data['sensor_name'],
                                             sensor_type_id=sensor_type_id).first()
        if sensor:
            response = sensor.to_json()
        else:
            response = {json_data['sensor_name']: """No sensor with this name in DB.
            Please create one with a post request first."""}

        return response

    """ Add a temperature sensor given is sensor_id"""
    def post(self):
        return self.create_or_update_sensor(request.get_json(silent=True))

    """Bulk update a temperature sensor ID and/or value"""
    def put(self, sensor_id):
        return self.create_or_update_sensor(request.get_json(silent=True))

    """Update a sensor Value"""
    def patch(self, sensor_id):
        pass

    """Delete a sensor given is sensor_id"""
    def delete(self, sensor_id):
        pass

    def create_or_update_sensor(self, json_data):
        sensor_type_id = self.get_sensor_type_id()

        if json_data is None:
            response = {'error': 'Data not JSON or header Content-Type not set to application/json'}
        else:
            response = ''
            if request.method == 'POST':
                response = self.create_sensor(json_data, sensor_type_id)
            elif request.method == 'PUT':
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
        prob = SensorModel.query.filter_by(name=json_sensor_data['sensor_name'],
                                           sensor_type_id=sensor_type_id).first()
        if prob:
            # TODO : check if json_data['sensor_type_id] exists. If yes we need to update type_id too
            prob.sensor_type_id = sensor_type_id
            prob.name = json_sensor_data['sensor_name']
            prob.value = json_sensor_data['sensor_value']
            db.session.add(prob)
            db.session.commit()
            response = prob.to_json()
        else:
            response = {json_sensor_data['sensor_name']:
                        """No sensor with name : {0} of type : {1} in DB."""
                        .format(json_sensor_data['sensor_name'],
                                self.sensor_type.get_sensor_type_name(sensor_type_id))}

        return response

    def get_sensor_type_id(self, sensor_type_name):
        return self.sensor_type.get_sensor_type_id(sensor_type_name)
