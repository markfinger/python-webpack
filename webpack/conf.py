import os
from optional_django import conf


class Conf(conf.Conf):
    # Environment configuration
    STATIC_ROOT = None
    STATIC_URL = None
    OUTPUT_DIR = 'webpack_assets'
    CONFIG_DIRS = None
    CONTEXT = None

    # Build server
    BUILD_URL = 'http://127.0.0.1:9009/build'

    # Watching
    WATCH = False
    AGGREGATE_TIMEOUT = 200
    POLL = None
    HMR = False

    # Caching
    CACHE = True
    CACHE_DIR = None

    # Manifest
    MANIFEST = None
    USE_MANIFEST = False
    MANIFEST_PATH = None
    MANIFEST_SETTINGS = {
        # Force the compiler to connect to the build server
        'USE_MANIFEST': False,
        # Ensure that the server does not add a hmr runtime
        'HMR': False,
    }

    def get_path_to_output_dir(self):
        return os.path.join(self.STATIC_ROOT, self.OUTPUT_DIR)

    def get_public_path(self):
        static_url = self.STATIC_URL
        if static_url and static_url.endswith('/'):
            static_url = static_url[:-1]

        return '/'.join([static_url, self.OUTPUT_DIR])

settings = Conf()
