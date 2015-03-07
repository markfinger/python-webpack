from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

setting_overrides = getattr(settings, 'DJANGO_WEBPACK', {})

BUNDLE_ROOT = setting_overrides.get('BUNDLE_ROOT', None)
if BUNDLE_ROOT is None:
    raise ImproperlyConfigured('DJANGO_WEBPACK[\'BUNDLE_ROOT\'] has not been defined')

BUNDLE_URL = setting_overrides.get('BUNDLE_URL', None)
if BUNDLE_URL is None:
    raise ImproperlyConfigured('DJANGO_WEBPACK[\'BUNDLE_URL\'] has not been defined')

CACHE = setting_overrides.get(
    'CACHE',
    not settings.DEBUG,
)

WATCH_CONFIG_FILES = setting_overrides.get(
    'WATCH_CONFIG_FILES',
    settings.DEBUG,
)

OUTPUT_FULL_STATS = setting_overrides.get(
    'OUTPUT_FULL_STATS',
    False,
)