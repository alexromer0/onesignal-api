import requests
import json


class HttpRequest:
    response = {'error': False, 'message': '', 'data': []}
    url = ''
    headers = {}
    payload = {}

    def __init__(self, url, headers=False):
        self.url = url
        if isinstance(headers, dict):
            self.headers = headers
        else:
            self.response['error'] = True
            self.response['message'] = 'The headers are not dict type'
            self.response['data'] = headers

    def post_request(self, data):
        if not self.url:
            self.response['error'] = True
            self.response['message'] = 'The url is empty, please provide an url'
            self.response['data'] = []
        else:
            try:
                req = requests.post(self.url, headers=self.headers, data=json.dumps(data))
                if req.status_code == 200:
                    res = req.json()
                    if 'errors' not in res:
                        self.response['error'] = False
                        self.response['message'] = 'Ok'
                        self.response['data'] = res
                    else:
                        self.response['error'] = True
                        self.response['message'] = 'Fail with a status 200, check the data for more information'
                        self.response['data'] = res['errors']
                else:
                    self.response['error'] = True
                    self.response['message'] = 'Fail with a status different than 200, check the data for more info'
                    self.response['data'] = req.json()

                return self.response
            except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
                self.response['error'] = True
                self.response['message'] = e.message
                return self.response
