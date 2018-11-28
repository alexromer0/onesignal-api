import datetime

from onesignalapi.utils import response
import onesignalapi.config.settings as config
from onesignalapi.errors.exceptions import MisconfigurationError


class Validator(object):
    def __init__(self):
        self._response = response.Response()

    def check_setup(self):
        if not config.ONESIGNAL_APP_ID:
            raise MisconfigurationError('No APP_ID configured')
        if not config.ONESIGNAL_API_KEY:
            raise MisconfigurationError('No APP_KEY configured')

    def is_valid_date(self, date):
        try:
            date_parsed = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            return self._response.success_response('ok', date_parsed)
        except ValueError:
            return self._response.error_response('The datetime format is not correct', [])
