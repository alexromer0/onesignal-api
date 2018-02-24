class Response(object):

    def __init__(self):
        self.__structure = {'error': None, 'message': '', 'data': ''}

    def error_response(self, msg, data):
        self.__structure['error'] = True
        self.__structure['message'] = msg
        self.__structure['data'] = data
        return self.__structure

    def success_response(self, msg, data):
        self.__structure['error'] = False
        self.__structure['message'] = msg
        self.__structure['data'] = data
        return self.__structure
