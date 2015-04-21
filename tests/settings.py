import os
from service_host.conf import settings as service_host_settings
from webpack.conf import settings as webpack_settings

TEST_ROOT = os.path.dirname(__file__)

service_host_settings.configure(
    PATH_TO_NODE_MODULES=os.path.join(TEST_ROOT, 'node_modules'),
    CONFIG_FILE=os.path.join(TEST_ROOT, 'services.config.js'),
    # Saves us from having to spin an instance up ourselves
    USE_MANAGER=True,
    # Ensure the host stops when the tests do
    ON_EXIT_MANAGED_HOSTS_STOP_TIMEOUT=0,
)

webpack_settings.configure(
    BUNDLE_ROOT=os.path.join(os.path.dirname(__file__), '__BUNDLE_ROOT__'),
    BUNDLE_URL='/static/',
)