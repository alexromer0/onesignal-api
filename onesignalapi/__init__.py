from config import settings
from notifications.notification import Notification


class OneSignal:
    def __init__(self, app_id, api_key):
        settings.ONESIGNAL_API_KEY = api_key
        settings.ONESIGNAL_APP_ID = app_id

    @staticmethod
    def new_notification(title, subtitle, content):
        notification = Notification(title, subtitle, content)
        return notification
