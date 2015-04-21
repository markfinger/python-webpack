import os
from service_host.conf import settings as service_host_settings
from webpack.conf import settings as webpack_settings

DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

service_host_settings.configure(
    # Configure the service host to respect the project's
    # DEBUG flag
    PRODUCTION=not DEBUG,
    CACHE=not DEBUG,

    # In development, the service host will be controlled by
    # a manager process which runs in the background and handles
    # starting and stopping other node processes
    USE_MANAGER=DEBUG,

    # A path to the node_modules directory where `service-host`
    # was installed by npm
    PATH_TO_NODE_MODULES=os.path.join(BASE_DIR, 'node_modules'),

    # The config file that the service host uses
    CONFIG_FILE=os.path.join(BASE_DIR, 'services.config.js')
)

webpack_settings.configure(
    # The root directory that webpack will place files into
    # and infer urls from
    BUNDLE_ROOT=os.path.join(BASE_DIR, 'static'),

    # The directory within BUNDLE_ROOT that webpack will place
    # files into
    BUNDLE_DIR='webpack',

    # The root url that webpack will use to determine the urls
    # to bundles
    BUNDLE_URL='/static/',

    # In development, a watcher will rebuild a bundle whenever
    # the config file changes
    WATCH_CONFIG_FILES=DEBUG,

    # In development, a watcher will rebuild a bundle whenever
    # the source files change
    WATCH_SOURCE_FILES=DEBUG,
)