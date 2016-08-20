from flask_restful import Resource


class Sensors(Resource):
    """Retrieve the complete list of sensors"""

    def get(self):
        return {'temp_sensor0': 'blibla',
                'temp_sensor1': 'bliblo',
                'humidity_sensor0': 'blublu'}

    def post(self):
        """Error can not post sensors list"""
