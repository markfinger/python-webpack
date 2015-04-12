import os
import json
import warnings
from django_node.base_service import BaseService
from ..exceptions import BundlingError
from ..settings import BUNDLE_ROOT, BUNDLE_DIR, OUTPUT_FULL_STATS


class WebpackService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'webpack.js')
    package_dependencies = os.path.dirname(__file__)

    def compile(self, path_to_config, watch_config, watch_source):
        response = self.send(
            config=path_to_config,
            watch=watch_source,
            watchDelay=200,
            watchConfig=watch_config,
            cache=False,
            fullStats=OUTPUT_FULL_STATS,
            bundleDir=os.path.join(BUNDLE_ROOT, BUNDLE_DIR),
        )

        stats = json.loads(response.text)

        if stats['errors']:
            raise BundlingError('\n\n'.join([path_to_config] + stats['errors']))

        if stats['warnings']:
            warnings.warn(stats['warnings'], Warning)

        return stats