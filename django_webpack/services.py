import os
import json
import warnings
from django_node.base_service import BaseService
from django_node import npm
from .exceptions import BundlingError
from .settings import CACHE

npm.install(os.path.dirname(__file__))


class WebpackService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'services', 'webpack.js')

    def bundle(self, path_to_config):
        response = self.send(
            path_to_config=path_to_config,
            cache=CACHE,
        )

        stats = json.loads(response.text)

        if stats['errors']:
            raise BundlingError('\n\n'.join([path_to_config] + stats['errors']))

        if stats['warnings']:
            warnings.warn(stats['warnings'], Warning)

        return stats