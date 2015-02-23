import os
import json
import warnings
from django_node.base_service import BaseService
from django_node.utils import resolve_dependencies
from .exceptions import BundlingError

resolve_dependencies(
    path_to_run_npm_install_in=os.path.dirname(__file__),
)


class WebpackService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'services', 'webpack.js')

    def bundle(self, path_to_config):
        response = self.send(
            path_to_config=path_to_config
        )

        stats = json.loads(response.text)

        if stats['errors']:
            raise BundlingError(stats['errors'])

        if stats['warnings']:
            warnings.warn(stats['warnings'], Warning)

        return stats