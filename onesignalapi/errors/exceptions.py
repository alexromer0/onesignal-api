class MisconfigurationError(Exception):
    """
    Misconfiguration exception
    """
    def __init__(self, message):
        super(MisconfigurationError, self).__init__(message)


class HttpRequestError(Exception):
    
    def __init__(self, message, data = None):
        super(HttpRequestError, self).__init__(message)

        if data is not None:
            self.data = data