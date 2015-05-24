import os
import sys
from js_host.conf import settings as js_host_settings
from webpack.conf import settings as webpack_settings

DEBUG = False
PRECOMPILING = 'precompile.py' in sys.argv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'static', 'js', 'webpack.config.js')

# In development, we need access to the js-host
if DEBUG or PRECOMPILING:
    js_host_settings.configure(
        USE_MANAGER=DEBUG or PRECOMPILING,
    )

webpack_settings.configure(
    # The root directory that webpack will place files into and infer urls from
    STATIC_ROOT=os.path.join(BASE_DIR, 'static'),

    # The root url that webpack will use to determine the urls to bundles
    STATIC_URL='/static/',

    # In development, a watcher will rebuild a bundle whenever its config file changes
    WATCH_CONFIG_FILES=DEBUG,

    # In development, a watcher will rebuild a bundle whenever any of its source files change
    WATCH_SOURCE_FILES=DEBUG,

    # A list of files which are precompiled for a production environment
    CACHE=(
        CONFIG_FILE,
    ),

    # In production, the python process should use the cache file, rather than relying
    # on an active connection to the compiler
    USE_CACHE_FILE=not DEBUG,
)