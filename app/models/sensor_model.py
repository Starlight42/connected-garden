from app import db


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_type_id = db.Column(db.Integer)
    name = db.Column(db.String(42), unique=True)
    value = db.Column(db.Integer)

    def __init__(self, sensor_name, sensor_value=None):
        self.name = sensor_name
        self.value = sensor_value

    def __repr__(self):
        return '<Sensor : {} = {}>'.format(self.name, self.value)
