DB_PATH = 'sqlite:////tmp/test.db'

EXEC_MODE = 'DEBUG'

ERRORS = {
    'SensorAlreadyExistsError': {
        'message': 'A sensor with that username already exists.',
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': 'A resource with that ID no longer exists.',
        'status': 410,
        'extra': 'Any extra information you want.',
    },
    'SensorBadRequest': {
        'message': 'Data not JSON or header Content-Type not set to application/json',
        'status': 400
    }
}
