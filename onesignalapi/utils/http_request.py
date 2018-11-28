import requests
import json

from onesignalapi.errors.exceptions import HttpRequestError
from .response import Response


class HttpRequest(object):
    __headers = None

    def __init__(self, url, headers=None):
        self.__url = url
        self.__payload = {}
        self.response = {}
        if headers is not None:
            if isinstance(headers, dict):
                self.__headers = headers
                self.response = Response().success_response('ok', [])
            else:
                self.response = Response().error_response('The headers attribute must be a dictionary', [])
                raise ValueError('The headers attribute must be a dictionary')

    def post_request(self, data):
        if not self.__url:
            raise HttpRequestError('The url is empty, please provide an url')

        try:
            req = requests.post(self.__url, headers=self.__headers, data=json.dumps(data))
            if req.status_code == 200:
                res = req.json()
                if 'errors' not in res:
                    _response = Response()
                    self.response = _response.success_response('Ok', res)
                else:
                    raise HttpRequestError('Fail with a status 200, check the data for more information', res['errors'])
            else:
                raise HttpRequestError('Fail with a status different than 200, check the data for more info', req.json())

        except requests.exceptions.RequestException as e:
            raise HttpRequestError(repr(e))

    def put_request(self, data):
        try:
            if not self.__url:
                _response = Response()
                self.response = _response.error_response('The url is empty, please provide an url', [])
            else:
                req = requests.put(self.__url, data=json.dumps(data), headers=self.__headers)
                if req.status_code == 200:
                    _response = Response()
                    self.response = _response.success_response('success', req.json())
                else:
                    _response = Response()
                    self.response['error'] = _response.error_response(
                        'Fail with a status different than 200, check the data for more info', req.json())

            return self.response
        except requests.exceptions.RequestException as e:
            _response = Response()
            self.response = _response.error_response(repr(e), [])
            return self.response

    def get_request(self, data):
        try:
            if not self.__url:
                _response = Response()
                self.response = _response.error_response('The url is empty, please provide an url', [])
            else:
                req = requests.get(self.__url, params=json.dumps(data))
                if req.status_code == 200:
                    _response = Response()
                    self.response = _response.success_response('success', req.json())
                else:
                    _response = Response()
                    self.response = _response.error_response(
                        'Fail with a status different than 200, check the data for more info', [req.text])

            return self.response
        except requests.exceptions.RequestException as e:
            _response = Response()
            self.response = _response.error_response(repr(e), [])
            return self.response
