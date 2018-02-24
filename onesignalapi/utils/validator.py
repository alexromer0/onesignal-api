import datetime

from onesignalapi.utils import response
import onesignalapi.config.settings as config


class Validator(object):
    def __init__(self):
        self._response = response.Response()

    def check_setup(self):
        if not config.ONESIGNAL_APP_ID:
            return self._response.error_response('There is not APP_ID configured', [])
        if not config.ONESIGNAL_API_KEY:
            return self._response.error_response('There is not APP_KEY configured', [])
        return self._response.success_response('ok', [])

    def is_valid_date(self, date):
        try:
            date_parsed = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            return self._response.success_response('ok', date_parsed)
        except ValueError:
            return self._response.error_response('The datetime format is not correct', [])
