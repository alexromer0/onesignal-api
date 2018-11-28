from onesignalapi.utils import response, http_request, device_switcher, validator
import onesignalapi.config.settings as config


class Device(object):

    def __init__(self, os_id):
        self.__id = os_id
        self.__url = config.ONESIGNAL_BASE_URL + config.ONESIGNAL_VERSION + '/players'
        self.__response = response.Response()
        self.__headers = {"Content-Type": "application/json; charset=utf-8"}
        self.__valid = validator.Validator()

    def update_device(self, data):
        if not config.ONESIGNAL_APP_ID:
            return self.__response.error_response('No One signal APP ID configured', [])

        payload = {"app_id": config.ONESIGNAL_APP_ID}
        if isinstance(data, dict):
            if not self.__id:
                return self.__response.error_response('Not one signal id provided', self.__id)
            else:
                # First you need to get the devices and make sure you are not overwriting the device data
                device = self.get_device()
                if device['error']:
                    return self.__response.error_response('There was a problem updating: ' + device['message'],
                                                          device['data'])
                else:
                    # Switcher
                    switcher = device_switcher.DeviceSwitch(device['data'])
                    for key, value in data.items():
                        try:
                            # Validate and transform all the values
                            payload[key] = switcher.switch(key, value)
                        except ValueError as e:
                            return self.__response.error_response(repr(e), [])
                    # Do the update
                    self.__url = self.__url + '/' + self.__id
                    req = http_request.HttpRequest(self.__url, self.__headers)
                    r = req.put_request(payload)
                    if r['error']:
                        resp = self.__response.error_response('There was an error updating the device: ' + r['message'],
                                                              r['data'])
                    else:
                        resp = self.__response.success_response('success', r['data'])
                    return resp
        else:
            return self.__response.error_response('No dictionary received for data', data)

    def get_device(self):
        if not config.ONESIGNAL_APP_ID:
            return self.__response.error_response('No One signal APP ID configured', [])

        if not self.__id:
            return self.__response.error_response('No one signal id provided', self.__id)
        else:
            url = self.__url + '/' + self.__id
            try:
                req = http_request.HttpRequest(url)
                data = {'app_id': config.ONESIGNAL_APP_ID}
                r = req.get_request(data)
                if r['error']:
                    resp = self.__response.error_response(
                        'There was an error trying to get the device: ' + r['message'],
                        r['data'])
                else:
                    resp = self.__response.success_response('success', r['data'])
                return resp
            except ValueError as e:
                return self.__response.error_response(repr(e), [])
