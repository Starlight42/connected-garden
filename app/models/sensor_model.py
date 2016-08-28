from app import db


class SensorModel(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    sensor_type_id = db.Column(db.Integer, db.ForeignKey('sensor_type.id'))
    name = db.Column(db.String(42), unique=True)
    value = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint(sensor_type_id, name, name='uniq_name_type'),)

    def __init__(self, sensor_name, sensor_type_id, sensor_value=None):
        self.sensor_type_id = sensor_type_id
        self.name = sensor_name
        self.value = sensor_value

    def to_json(self):
        return dict(sensor_id=self.id, sensor_name=self.name, sensor_value=self.value)
