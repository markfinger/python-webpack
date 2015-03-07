import os
import json
import warnings
from django_node.base_service import BaseService
from .exceptions import BundlingError
from .settings import WATCH_CONFIG_FILES, BUNDLE_ROOT


class WebpackService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'services', 'webpack.js')
    package_dependencies = os.path.dirname(__file__)

    def bundle(self, path_to_config):
        response = self.send(
            path_to_config=path_to_config,
            bundle_root=BUNDLE_ROOT,
            watch_config_files=WATCH_CONFIG_FILES,
        )

        output = json.loads(response.text)

        stats = output['stats']

        if stats['errors']:
            raise BundlingError('\n\n'.join([path_to_config] + stats['errors']))

        if stats['warnings']:
            warnings.warn(stats['warnings'], Warning)

        return output