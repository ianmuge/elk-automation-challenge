
import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


class ApiSession(object):
    '''
    classdocs
    '''

    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        self.url = kwargs.get('url')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.insecure = kwargs.get('insecure') or True
        self.auth = kwargs.get('auth') or False

        cfg = kwargs.get('cfg')
        if cfg:
            self.url = cfg.get('url') or self.url
            self.url = self.url.strip('/')
            self.username = cfg.get('username') or self.username
            self.password = cfg.get('password') or self.password
            if cfg.get('xpack'):
                self.auth = True

        if not self.url:
            raise AttributeError('URL can not be empty')

        self.session = requests.Session()

        if self.insecure:
            disable_warnings(InsecureRequestWarning)
            self.session.verify = False
        if self.auth and self.username and self.password:
            self.session.auth = (self.username, self.password)

    def delete(self, path, **kwargs):
        response = self.session.delete(self.url + path, **kwargs)
        response.raise_for_status()
        return response

    def get(self, path, **kwargs):
        response = self.session.get(self.url + path, **kwargs)
        response.raise_for_status()
        return response

    def post(self, path, **kwargs):
        response = self.session.post(self.url + path, **kwargs)
        response.raise_for_status()
        return response

    def put(self, path, **kwargs):
        response = self.session.put(self.url + path, **kwargs)
        response.raise_for_status()
        return response

    def update_headers(self, info):
        self.session.headers.update(info)
