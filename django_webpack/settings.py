import os
from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_WEBPACK', {})

NODE_VERSION_REQUIRED = setting_overrides.get(
    'NODE_VERSION_REQUIRED',
    (0, 10, 0)
)

NPM_VERSION_REQUIRED = setting_overrides.get(
    'NPM_VERSION_REQUIRED',
    (1, 2, 0)
)

PATH_TO_BUNDLER = setting_overrides.get(
    'PATH_TO_BUNDLER',
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'bundle.js'))
)

STATIC_ROOT = setting_overrides.get(
    'STATIC_ROOT',
    settings.STATIC_ROOT,
)

STATIC_URL = setting_overrides.get(
    'STATIC_URL',
    settings.STATIC_URL,
)

DEBUG = setting_overrides.get(
    'DEBUG',
    settings.DEBUG,
)

CACHE = setting_overrides.get(
    'CACHE',
    not settings.DEBUG,
)