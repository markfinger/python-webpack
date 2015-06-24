import requests
from .conf import settings
from .exceptions import BuildServerConnectionError, BuildServerUnexpectedResponse


class BuildServer(object):
    def __init__(self, url):
        self.url = url

    def is_running(self):
        try:
            res = requests.get(self.url)
        except requests.ConnectionError:
            return False

        return res.status_code == 200 and 'webpack-build-server' in res.text

    def build(self, options):
        if not self.is_running():
            raise BuildServerConnectionError('Cannot connect to {}'.format(self.url))

        res = requests.post('{}/build'.format(self.url), json=options)

        if res.status_code != 200:
            raise BuildServerUnexpectedResponse(res.text)

        return res.json()


server = BuildServer(settings.BUILD_SERVER_URL)
