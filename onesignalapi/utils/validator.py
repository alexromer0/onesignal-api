import onesignalapi.config.settings as config

class Validator:
    response = {}
    response['error'] = False
    response['data'] = []


    def check_setup(self,):
        del self.response['data'][:]
        if config.ONESIGNAL_APP_ID == False:
            self.response['error'] = True
            self.response['data'].append('There is not APP_ID configured')
        if config.ONESIGNAL_API_KEY == False:
            self.response['error'] = True
            self.response['data'].append('There is not APP_KEY configured')

        return self.response