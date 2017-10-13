from flask import request
from flask_restful import Resource
from sqlalchemy import exc

from app.models import db, SensorModel
import app.resources


class Sensor(Resource):
    """This endpoint allow to manage sensors"""
    sensor_type = None

    def __init__(self):
        self.sensor_type = app.resources.SensorType()

    """Base endpoint functions for sensor"""

    """ Get a sensor value"""
    def get(self, sensor_id=None):
        if sensor_id:
            """ We fetch and return sensor with id sensor_id """
            response = self.get_sensor(sensor_id)
        else:
            """ We fetch and return all sensors """
            response = self.get_sensors()

        return response

    """ Add a temperature sensor given is sensor_id"""
    def post(self):
        """Create sensor in DB :
            First we create an object model describing our db entry,
            then we add it to the db and commit to validate the action.
            After that we are getting the last inserted id and return the
            result as a confirmation.
        """
        json_data = request.get_json(silent=True)

        if json_data is None:
            response = {'error': 'Data not JSON or header Content-Type not set to application/json'}
        else:
            prob = SensorModel(json_data['sensor_name'], json_data['sensor_type_id'],
                               json_data['sensor_value'])

            self.commit_db_changes(prob)
            # Check commit_db_change return if failed (IntegrityError) set response from return status
            prob_list = SensorModel.query.filter_by(id=prob.id).first()
            response = self.add_sensor_type_name(prob_list.to_json())

        return response

    """ Bulk update a sensor.
        PUT is essentialy a DELETE followed by a POST """
    def put(self, sensor_id):
        # Not usefull for now
        pass

    """ Update a sensor Value or sensor type or both"""
    def patch(self, sensor_id):
        json_data = request.get_json(silent=True)

        if json_data is None:
            response = {'error': 'Data not JSON or header Content-Type not set to application/json'}
        else:
            prob = SensorModel.query.filter_by(id=sensor_id).first()
            if prob:
                prob.name = json_data['sensor_name'] if \
                    'sensor_name' in json_data else prob.name
                prob.value = json_data['sensor_value'] if \
                    'sensor_value' in json_data else prob.value
                prob.sensor_type_id = json_data['sensor_type_id'] if \
                    'sensor_type_id' in json_data else prob.sensor_type_id

                response = self.commit_db_changes(prob)
            else:
                response = {'error': 'No sensor found with this ID'}

        return response

    """ Delete a sensor given is sensor_id """
    def delete(self, sensor_id):
        sensor = SensorModel.query.filter_by(id=sensor_id).first()

        if sensor:
            db.session.delete(sensor)
            db.session.commit()
            response = {"deleted": self.add_sensor_type_name(sensor.to_json())}
        else:
            response = {"errorMsg": "No sensor with this id in DB"}

        return response

    """Usefull tools functions for sensor"""

    def commit_db_changes(self, db_obj):
        db.session.add(db_obj)

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            db.session.flush()
            response = {"Error": e.args}
        else:
            response = db_obj.to_json()

        return response

    """ Return the sensor with id sensor_id """
    def get_sensor(self, sensor_id):
        sensor = SensorModel.query.filter_by(id=sensor_id).first()

        if sensor:
            response = self.add_sensor_type_name(sensor.to_json())

        else:
            response = {"errorMsg": """No sensor with this name in DB.
            Please create one with a post request first."""}

        return response

    """ Return a list of all sensors """
    def get_sensors(self):
        sensors = SensorModel.query.all()

        if sensors:
            sensor_list = [self.add_sensor_type_name(sensor.to_json()) for sensor in sensors]
            response = {"sensors": sensor_list}
        else:
            response = {"errorMsg": """There is no sensor in the DB"""}

        return response

    def get_sensor_type_id(self, sensor_type_name):
        return self.sensor_type.get_sensor_type_id(sensor_type_name)

    def add_sensor_type_name(self, response):
        response['sensor_type_name'] = self.sensor_type.get_sensor_type_name(response['sensor_type_id'])
        return response
