# -*- coding: utf-8 -*-
"""Notifications main class.

This module handle the push notification creation, sending, include segments,
exclude segments, set filters.

It always return a dictionary (dict) with this 3 elements:
- error: (bool) True or False, if there was an error
- message: (String) If there is an error it explain it, or `Ok` if nothing fails
- data: (list) It contains the response data or error data

TODO:
A lot! XD
"""
import onesignalapi.config.settings as config
import onesignalapi.utils.http_request as http_helper
import onesignalapi.utils.validator as validator


class Notification:
    response = {}
    response['error'] = False
    response['message'] = False
    response['data'] = []
    included_segments = False
    excluded_segments = False
    include_players_ids = []
    filters = []
    url = False
    message = ''
    title = ''
    subtitle = ''
    payload = {}
    headers = {}

    def __init__(self, title, subtitle, message):
        self.url = config.ONESIGNAL_BASE_URL + config.ONESIGNAL_VERSION + '/notifications'
        self.title = title
        self.subtitle = subtitle
        self.message = message
        self.headers = {"Content-Type": "application/json; charset=utf-8",
                        "Authorization": "Basic " + config.ONESIGNAL_API_KEY.__str__()}

    def send(self):
        valid = validator.Validator()
        setup_valid = valid.check_setup()

        if setup_valid['error']:
            self.response['error'] = True
            self.response['message'] = 'There ara some missconfigurations, check data for more info'
            self.response['data'] = {'errors': setup_valid['data']}
            return self.response
        else:
            self.payload['app_id'] = config.ONESIGNAL_APP_ID
            self.payload['headings'] = {"en": self.title}
            self.payload['subtitle'] = {"en": self.subtitle}
            self.payload['contents'] = {"en": self.message}
            self.payload['ios_badgeType'] = "Increase"
            self.payload['ios_badgeCount'] = 1

            req = http_helper.HttpRequest(self.url, self.headers)
            if req.response['error']:
                return req.response
            res = req.post_request(self.payload)
            if res['error']:
                self.response['error'] = True
                self.response['message'] = res['message']
                self.response['data'] = res['data']
            return self.response

    def include_segments(self, segments):
        if isinstance(segments, list):
            if self.excluded_segments and any(map(lambda v: v in self.excluded_segments, segments)):
                self.response['error'] = True
                self.response['message'] = 'One or more of the provided segments are present into the excluded segments'
                self.response['data'] = []
            else:
                self.included_segments = segments
                self.response['error'] = False
                self.response['message'] = 'Ok'
                self.response['data'] = segments
                self.payload['included_segments'] = self.included_segments
        else:
            self.response['error'] = True
            self.response['message'] = 'Not an array given, the parameter must be an array'
            self.response['data'] = []
        return self.response

    def exclude_segments(self, segments):
        if isinstance(segments, list):
            if self.included_segments and any(map(lambda v: v in self.included_segments, segments)):
                self.response['error'] = True
                self.response['message'] = 'One or more of the provided segments are present into the included segments'
                self.response['data'] = []
            else:
                self.excluded_segments = segments
                self.payload['excluded_segments'] = self.excluded_segments
                self.response['error'] = False
                self.response['message'] = 'Ok'
                self.response['data'] = self.excluded_segments
        else:
            self.response['error'] = True
            self.response['message'] = 'Not an array given, the parameter must be an array'
            self.response['data'] = []

        return self.response

    def set_filters(self, filters):
        if isinstance(filters, list):
            self.filters = filters
            self.payload['filters'] = self.filters
        else:
            self.response['error'] = True
            self.response['message'] = 'Not an array given, the parameter must be an array'
            self.response['data'] = []
            return self.response

    def set_content(self, title, subtitle, message):
        if not title and not subtitle and not message:
            self.response['error'] = True
            self.response['message'] = 'All the fields are empty, title, subtitle and message. Need at least one'
            self.response['data'] = []
            return self.response
        else:
            self.title = title
            self.subtitle = subtitle
            self.message = message
            return True

    def set_playerids(self, players):
        if isinstance(players, list):
            if not self.included_segments or not self.excluded_segments:
                self.include_players_ids = players
                self.payload['include_player_ids'] = self.include_players_ids
                return True
            else:
                self.response['error'] = True
                self.response['message'] = 'There are values in include or exclude segments, delete them and try again'
                self.response['data'] = []
                return self.response
        else:
            self.response['error'] = True
            self.response['message'] = 'The player parameter must be a list'
            self.response['data'] = []
            return self.response

    def delete_included_segments(self):
        del self.included_segments[:]
        return True

    def delete_excluded_segments(self):
        del self.excluded_segments[:]
        return True
