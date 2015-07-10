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

        return res.status_code == 200 and 'webpack-build' in res.text

    def build(self, options):
        try:
            res = requests.post(self.url, json=options)
        except requests.ConnectionError:
            raise BuildServerConnectionError('Tried to send build request to {}'.format(self.url))

        if res.status_code != 200:
            raise BuildServerUnexpectedResponse(
                'Unexpected response from {} - {}: {}'.format(self.url, res.status_code, res.text)
            )

        return res.json()


server = BuildServer(settings.BUILD_URL)
