import datetime

import onesignalapi.config.settings as config


class Validator:
    response = {'error': False, 'data': []}

    def check_setup(self):
        del self.response['data'][:]
        if not config.ONESIGNAL_APP_ID:
            self.response['error'] = True
            self.response['data'].append('There is not APP_ID configured')
        if not config.ONESIGNAL_API_KEY:
            self.response['error'] = True
            self.response['data'].append('There is not APP_KEY configured')

        return self.response

    def is_valid_date(self, date):
        del self.response['data'][:]
        try:
            date_parsed = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            self.response['error'] = False
            self.response['data'].append(date_parsed)
        except ValueError:
            self.response['error'] = True
            self.response['data'].append('The datetime format is not correct')

        return self.response
