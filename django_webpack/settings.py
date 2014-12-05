import os
from django.conf import settings
from django_node.settings import PATH_TO_NODE as DEFAULT_PATH_TO_NODE

setting_overrides = getattr(settings, 'DJANGO_WEBPACK', {})

PATH_TO_NODE = setting_overrides.get(
    'PATH_TO_NODE',
    DEFAULT_PATH_TO_NODE
)

NODE_VERSION_REQUIRED = setting_overrides.get(
    'NODE_VERSION_REQUIRED',
    (0, 10, 0)
)

NPM_VERSION_REQUIRED = setting_overrides.get(
    'NPM_VERSION_REQUIRED',
    (1, 2, 0)
)

# TODO move dep and package checks to django-node
CHECK_DEPENDENCIES = setting_overrides.get(
    'CHECK_DEPENDENCIES',
    True
)

CHECK_PACKAGES = setting_overrides.get(
    'CHECK_PACKAGES',
    True
)

BUNDLER = setting_overrides.get(
    'BUNDLER',
    os.path.abspath(os.path.join(__file__, '../bundle.js'))
)

STATIC_ROOT = setting_overrides.get(
    'STATIC_ROOT',
    settings.STATIC_ROOT,
)

STATIC_URL = setting_overrides.get(
    'STATIC_URL',
    settings.STATIC_URL,
)