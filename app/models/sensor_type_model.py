from app import db, config


class SensorTypeModel(db.Model):
    __tablename__ = 'sensor_type'
    id = db.Column(db.Integer, primary_key=True)
    sensor_type_name = db.Column(db.String(42), unique=True)
    sensors = db.relationship('SensorModel', backref=__tablename__, lazy='dynamic')

    def __init__(self, sensor_type_name):
        self.sensor_type_name = sensor_type_name

    def to_json(self):
        return dict(type_id=self.id, type_name=self.sensor_type_name)


"""
    Check application launch mode.
    If we are in DEBUG mode the db is stored in /tmp, so we have to create sensor_type table.
    Then we provision it with current supported sensor types
"""
if config.EXEC_MODE is 'DEBUG':
    """Execute a create_all (tables) which create if not exists mandatory tables"""
    db.create_all()
    """Check if sensor_type is already populated"""
    if SensorTypeModel.query.first() is None:
        sensor_types = [SensorTypeModel('TEMP'), SensorTypeModel('HUMI'), SensorTypeModel('T/H')]
        for sensor_type in sensor_types:
            db.session.add(sensor_type)
        db.session.commit()
