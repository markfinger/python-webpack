import os
from optional_django import conf


class Conf(conf.Conf):
    BUILD_SERVER_URL = 'http://127.0.0.1:9009'

    STATIC_ROOT = None

    STATIC_URL = None

    WATCH = True

    CONTEXT = None

    HMR = False

    CACHE = True

    AGGREGATE_TIMEOUT = 200

    POLL = None

    OUTPUT_DIR = 'webpack'

    CACHE_DIR = None

    def get_path_to_output_dir(self):
        return os.path.join(self.STATIC_ROOT, self.OUTPUT_DIR)

    def get_public_path(self):
        static_url = self.STATIC_URL
        if static_url and static_url.endswith('/'):
            static_url = static_url[0:-1]
        return '/'.join([static_url, self.OUTPUT_DIR])

settings = Conf()
