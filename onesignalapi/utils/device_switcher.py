class DeviceSwitch(object):
    def __init__(self, device_data):
        self.__device_data = device_data

    def switch(self, key, value):
        switcher = {
            "identifier": self.__identifier,
            "language": self.__language,
            "timezone": self.__timezone,
            "game_version": self.__game_version,
            "device_model": self.__device_model,
            "device_os": self.__device_os,
            "ad_id": self.__ad_id,
            "sdk": self.__sdk,
            "session_count": self.__session_count,
            "tags": self.__tags,
            "amount_spent": self.__amount_spent,
            "created_at": self.__created_at,
            "playtime": self.__playtime,
            "badge_count": self.__badge_count,
            "last_active": self.__last_active,
            # WARNING: Be careful with this one
            "notification_type": self.__notification_types,
            # For testing only
            "test_type": self.__test_type,
            "long": self.__long,
            "lat": self.__lat,
            "country": self.__country
        }
        # Get the function from switcher dictionary
        func = switcher.get(key, lambda: "Invalid argument")
        # Execute the function
        return func(value)

    # val: String
    @staticmethod
    def __identifier(val):
        if isinstance(val, str):
            return val
        else:
            raise ValueError('Identifier value must be a string')

    # val: String
    @staticmethod
    def __language(val):
        if isinstance(val, str):
            return val
        else:
            raise ValueError('Language value must be a string')

    # val: int
    @staticmethod
    def __timezone(val):
        if type(val) is int:
            return val
        else:
            raise ValueError('Timezone value must be an integer')

    # val: String
    @staticmethod
    def __game_version(val):
        if isinstance(val, str):
            return val
        else:
            raise ValueError('Game version value must be a string')

    # val: String
    @staticmethod
    def __device_model(val):
        if isinstance(val, str):
            return val
        else:
            raise ValueError('Device model value must be a string')

    # val: String
    @staticmethod
    def __device_os(val):
        if isinstance(val, str):
            return val
        else:
            raise ValueError('Device OS value must be a string')

    # val: String
    @staticmethod
    def __ad_id(val):
        if isinstance(val, str):
            return val
        else:
            raise ValueError('Ad ID value must be a string')

    # val: String
    @staticmethod
    def __sdk(val):
        if isinstance(val, str):
            return val
        else:
            raise ValueError('SDK value must be a string')

    # val: int
    @staticmethod
    def __session_count(val):
        if type(val) is int:
            return val
        else:
            raise ValueError('Session Count value must be an integer')

    # val: Dictionary {}
    def __tags(self, val):
        if isinstance(val, dict):
            temp_tags = self.__device_data['tags']
            for key_data, val_data in val.items():
                # updating and creating the tags
                temp_tags[key_data] = val_data
            return temp_tags
        else:
            raise ValueError('Tags val must be a dictionary')

    # val: String
    @staticmethod
    def __amount_spent(val):
        if isinstance(val, str):
            return val
        else:
            raise ValueError('Amount spent value must be a string')

    # val: int
    @staticmethod
    def __created_at(val):
        if type(val) is int:
            return val
        else:
            raise ValueError('Created At value must be an integer')

    # val: int
    @staticmethod
    def __playtime(val):
        if type(val) is int:
            return val
        else:
            raise ValueError('Playtime value must be an integer')

    # val: int
    @staticmethod
    def __badge_count(val):
        if type(val) is int:
            return val
        else:
            raise ValueError('Badge Count value must be an integer')

    # val: int
    @staticmethod
    def __last_active(val):
        if type(val) is int:
            return val
        else:
            raise ValueError('Last Active value must be an integer')

    # val: int
    @staticmethod
    def __notification_types(val):
        if type(val) is int:
            return val
        else:
            raise ValueError('Notification Types value must be an integer')

    # val: int
    @staticmethod
    def __test_type(val):
        if type(val) is int:
            return val
        else:
            raise ValueError('Test Type value must be an integer')

    # val: float
    @staticmethod
    def __long(val):
        if type(val) is float:
            return val
        else:
            raise ValueError('Long must be float')

    # val: float
    @staticmethod
    def __lat(val):
        if type(val) is float:
            return val
        else:
            raise ValueError('Lat must be float')

    # val: String
    @staticmethod
    def __country(val):
        if isinstance(val, str):
            return val
        else:
            raise ValueError('Country value must be a string')
