import os
from js_host.conf import settings as js_host_settings
from webpack.conf import settings as webpack_settings

DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

js_host_settings.configure(
    CACHE=not DEBUG,
    USE_MANAGER=DEBUG,
    SOURCE_ROOT=BASE_DIR,
)

webpack_settings.configure(
    # The root directory that webpack will place files into and infer urls from
    BUNDLE_ROOT=os.path.join(BASE_DIR, 'static'),

    # The directory within BUNDLE_ROOT that webpack will place files into
    BUNDLE_DIR='webpack',

    # The root url that webpack will use to determine the urls to bundles
    BUNDLE_URL='/static/',

    # In development, a watcher will rebuild a bundle whenever its config file changes
    WATCH_CONFIG_FILES=DEBUG,

    # In development, a watcher will rebuild a bundle whenever any of its source files change
    WATCH_SOURCE_FILES=DEBUG,
)