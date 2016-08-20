from flask import Flask
from flask_restful import Api

from endpoints.temperature_sensor import TemperatureSensor
from endpoints.sensors import Sensors

app = Flask(__name__)
api = Api(app)

api.add_resource(TemperatureSensor, '/temp/<string:sensor_id>', '/temps')
api.add_resource(Sensors, '/sensors')

if __name__ == '__main__':
    app.run(debug=True)
