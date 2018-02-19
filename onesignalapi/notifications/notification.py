# -*- coding: utf-8 -*-
"""Notifications main class.

This module handle the push notification creation, sending, include segments,
exclude segments, set filters and scheduling.

It always return a dictionary (dict) with this 3 elements:
- error: (bool) True or False, if there was an error
- message: (String) If there is an error it explain it, or `Ok` if nothing fails
- data: (list) It contains the response data or error data

TODO:
A lot! XD
"""
import pytz

import onesignalapi.config.settings as config
import onesignalapi.utils.http_request as http_helper
import onesignalapi.utils.validator as validator


class Notification:
    __response = {'error': False, 'message': False, 'data': []}

    # Params
    __send_after = False
    __included_segments = False
    ___excluded_segments = False
    __include_players_ids = []
    __filters = []
    __url = False
    __message = ''
    __title = ''
    __subtitle = ''

    __payload = {}
    __headers = {}
    __valid = None

    def __init__(self, title, subtitle, message):
        self.__url = config.ONESIGNAL_BASE_URL + config.ONESIGNAL_VERSION + '/notifications'
        self.__title = title
        self.__subtitle = subtitle
        self.__message = message
        self.__headers = {"Content-Type": "application/json; charset=utf-8",
                        "Authorization": "Basic " + config.ONESIGNAL_API_KEY.__str__()}
        self.__valid = validator.Validator()

    def send(self):
        setup_valid = self.__valid.check_setup()

        if setup_valid['error']:
            self.__response['error'] = True
            self.__response['message'] = 'There ara some missconfigurations, check data for more info'
            self.__response['data'] = {'errors': setup_valid['data']}
        else:
            self.__payload['app_id'] = config.ONESIGNAL_APP_ID
            self.__payload['headings'] = {"en": self.__title}
            self.__payload['subtitle'] = {"en": self.__subtitle}
            self.__payload['contents'] = {"en": self.__message}
            self.__payload['ios_badgeType'] = "Increase"
            self.__payload['ios_badgeCount'] = 1

            req = http_helper.HttpRequest(self.__url, self.__headers)
            if req.response['error']:
                return req.response
            res = req.post_request(self.__payload)
            if res['error']:
                self.__response['error'] = True
                self.__response['message'] = res['message']
                self.__response['data'] = res['data']
        return self.__response

    def include_segments(self, segments):
        if isinstance(segments, list):
            if self.___excluded_segments and any(map(lambda v: v in self.___excluded_segments, segments)):
                self.__response['error'] = True
                self.__response['message'] = 'One or more of the provided segments are present into the excluded segments'
                self.__response['data'] = []
            else:
                self.__included_segments = segments
                self.__response['error'] = False
                self.__response['message'] = 'Ok'
                self.__response['data'] = segments
                self.__payload['included_segments'] = self.__included_segments
        else:
            self.__response['error'] = True
            self.__response['message'] = 'Not an array given, the parameter must be an array'
            self.__response['data'] = []
        return self.__response

    def exclude_segments(self, segments):
        if isinstance(segments, list):
            if self.__included_segments and any(map(lambda v: v in self.__included_segments, segments)):
                self.__response['error'] = True
                self.__response['message'] = 'One or more of the provided segments are present into the included segments'
                self.__response['data'] = []
            else:
                self.___excluded_segments = segments
                self.__payload['excluded_segments'] = self.___excluded_segments
                self.__response['error'] = False
                self.__response['message'] = 'Ok'
                self.__response['data'] = self.___excluded_segments
        else:
            self.__response['error'] = True
            self.__response['message'] = 'Not an array given, the parameter must be an array'
            self.__response['data'] = []

        return self.__response

    def set_filters(self, filters):
        if isinstance(filters, list):
            self.__filters = filters
            self.__payload['filters'] = self.__filters
        else:
            self.__response['error'] = True
            self.__response['message'] = 'Not an array given, the parameter must be an array'
            self.__response['data'] = []
            return self.__response

    def set_content(self, title, subtitle, message):
        if not title and not subtitle and not message:
            self.__response['error'] = True
            self.__response['message'] = 'All the fields are empty, title, subtitle and message. Need at least one'
            self.__response['data'] = []
            return self.__response
        else:
            self.__title = title
            self.__subtitle = subtitle
            self.__message = message
            return True

    def set_playerids(self, players):
        if isinstance(players, list):
            if not self.__included_segments or not self.___excluded_segments:
                self.__include_players_ids = players
                self.__payload['include_player_ids'] = self.__include_players_ids
                return True
            else:
                self.__response['error'] = True
                self.__response['message'] = 'There are values in include or exclude segments, delete them and try again'
                self.__response['data'] = []
                return self.__response
        else:
            self.__response['error'] = True
            self.__response['message'] = 'The player parameter must be a list'
            self.__response['data'] = []
            return self.__response

    def delete_included_segments(self):
        del self.__included_segments[:]
        return True

    def delete_excluded_segments(self):
        del self.___excluded_segments[:]
        return True

    def schedule(self, date):
        valid_date = self.__valid.is_valid_date(date)
        if valid_date['error']:
            self.__response['error'] = True
            self.__response['message'] = 'There ara some missconfigurations, check data for more info'
            self.__response['data'] = {'errors': valid_date['data']}
            return self.__response
        else:
            # Convert date to given timezone
            original_date = valid_date['data'][0]
            user_datetime = pytz.timezone(config.TIMEZONE).localize(original_date)
            # Convert date to UTC
            utc_datetime = user_datetime.astimezone(pytz.utc)
            self.__send_after = utc_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')
            self.__payload['send_after'] = self.__send_after
            return True
