from config import settings
from notifications.notification import Notification
from devices import device


class OneSignal(object):
    def __init__(self, app_id, api_key):
        settings.ONESIGNAL_API_KEY = api_key
        settings.ONESIGNAL_APP_ID = app_id

    @staticmethod
    def new_notification(title, subtitle, content):
        notification = Notification(title, subtitle, content)
        return notification

    @staticmethod
    def set_timezone(timezone):
        settings.TIMEZONE = timezone

    @staticmethod
    def set_device(os_id):
        dev = device.Device(os_id)
        return dev
