class Response(object):

    def __init__(self, msg, data):
        self._message = msg
        self._data = data

    @property
    def error_response(self):
        return {'error': True, 'message': self._message, 'data': self._data}

    @property
    def success_response(self):
        return {'error': False, 'message': self._message, 'data': self._data}