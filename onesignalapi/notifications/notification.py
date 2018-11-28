# -*- coding: utf-8 -*-
"""Notifications main class.

This module handle the push notification creation, sending, include segments,
exclude segments, set filters and scheduling.

It always return a dictionary (dict) with this 3 elements:
- error: (bool) True or False, if there was an error
- message: (String) If there is an error it explain it, or `Ok` if nothing fails
- data: (list) It contains the response data or error data

"""
import pytz

from onesignalapi.config import settings as config
import onesignalapi.utils.http_request as http_helper
import onesignalapi.utils.validator as validator
from onesignalapi.errors.exceptions import *
from onesignalapi.utils import response


class Notification(object):
    def __init__(self, title, subtitle, message):
        """ Instantiate class Notification

        :param title:
        :param subtitle:
        :param message:
        """
        self.__url = config.ONESIGNAL_BASE_URL + config.ONESIGNAL_VERSION + '/notifications'
        self.__title = title
        self.__subtitle = subtitle
        self.__message = message
        self.__headers = {"Content-Type": "application/json; charset=utf-8",
                          "Authorization": "Basic " + config.ONESIGNAL_API_KEY.__str__()}
        # Params
        self.__send_after = False
        self.__included_segments = False
        self.__excluded_segments = False
        self.__include_players_ids = []
        self.__filters = []

        self.__payload = {}
        self.__response = {}

        self.__resp = response.Response()
        self.__valid = validator.Validator()

    def send(self):
        """ Sends the current notification

        :return Response:
        """
        try:
            self.__valid.check_setup()
        except MisconfigurationError as e:
            return self.__resp.error_response(e, [])

        try:
            req = http_helper.HttpRequest(self.__url, self.__headers)
        except ValueError as e:
            return self.__resp.error_response(e, [])

        self.__payload['app_id'] = config.ONESIGNAL_APP_ID
        self.__payload['headings'] = {"en": self.__title}
        self.__payload['subtitle'] = {"en": self.__subtitle}
        self.__payload['contents'] = {"en": self.__message}
        self.__payload['ios_badgeType'] = config.IOS_BADGETYPE
        self.__payload['ios_badgeCount'] = 1

        try:
            res = req.post_request(self.__payload)
            self.__response = self.__resp.success_response('success', res['data'])
        except HttpRequestError as e:
            self.__response = self.__resp.error_response(str(e), e.data)

        return self.__response

    def include_segments(self, segments):
        if isinstance(segments, list):
            if self.__excluded_segments and any(map(lambda v: v in self.__excluded_segments, segments)):
                self.__response = self.__resp.error_response(
                    'One or more of the provided segments are present into the excluded segments', [])
            else:
                self.__included_segments = segments
                self.__response = self.__resp.success_response('Ok', segments)
                self.__payload['included_segments'] = self.__included_segments
        else:
            self.__response = self.__resp.error_response('Not an array given, the parameter must be an array', [])
        return self.__response

    def exclude_segments(self, segments):
        if isinstance(segments, list):
            if self.__included_segments and any(map(lambda v: v in self.__included_segments, segments)):
                self.__response = self.__resp.error_response(
                    'One or more of the provided segments are present into the included segments', [])
            else:
                self.__excluded_segments = segments
                self.__payload['excluded_segments'] = self.__excluded_segments
                self.__response = self.__resp.success_response('Ok', self.__excluded_segments)
        else:
            self.__response = self.__resp.error_response('Not an array given, the parameter must be an array', [])

        return self.__response

    def set_filters(self, filters):
        if isinstance(filters, list):
            self.__filters = filters
            self.__payload['filters'] = self.__filters
            self.__response = self.__resp.success_response('ok', [])
        else:
            self.__response = self.__resp.error_response('Not an array given, the parameter must be an array', [])
        return self.__response

    def set_content(self, title, subtitle, message):
        if not title and not subtitle and not message:
            self.__response = self.__resp.error_response(
                'All the fields are empty, title, subtitle and message. Need at least one', [])
            return self.__response
        else:
            self.__title = title
            self.__subtitle = subtitle
            self.__message = message
            return self.__resp.success_response('ok', [])

    def set_playerids(self, players):
        if isinstance(players, list):
            if not self.__included_segments and not self.__excluded_segments:
                self.__include_players_ids = players
                self.__payload['include_player_ids'] = self.__include_players_ids
                return self.__resp.success_response('ok', [])
            else:
                self.__response = self.__resp.error_response(
                    'There are values in include or exclude segments, delete them and try again', [])
                return self.__response
        else:
            self.__response = self.__resp.error_response('The player parameter must be a list', [])
            return self.__response

    def delete_included_segments(self):
        del self.__included_segments[:]
        return self.__resp.success_response('ok', [])

    def delete_excluded_segments(self):
        del self.__excluded_segments[:]
        return self.__resp.success_response('ok', [])

    def schedule(self, date):
        valid_date = self.__valid.is_valid_date(date)
        if valid_date['error']:
            self.__response = self.__resp.error_response('There is a misconfiguration, check data for more info',
                                                         {'errors': valid_date['message']})
            return self.__response
        else:
            # Convert date to given timezone
            original_date = valid_date['data']
            user_datetime = pytz.timezone(config.TIMEZONE).localize(original_date)
            # Convert date to UTC
            utc_datetime = user_datetime.astimezone(pytz.utc)
            self.__send_after = utc_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')
            self.__payload['send_after'] = self.__send_after
            return self.__resp.success_response('ok', [])
