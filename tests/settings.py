import os
from js_host.conf import settings as js_host_settings
from webpack.conf import settings as webpack_settings

BASE_DIR = os.path.dirname(__file__)

js_host_settings.configure(
    SOURCE_ROOT=BASE_DIR,
    # Let the manager spin up an instance
    USE_MANAGER=True,
)

webpack_settings.configure(
    BUNDLE_ROOT=os.path.join(BASE_DIR, '__BUNDLE_ROOT__'),
    BUNDLE_URL='/static/',
)