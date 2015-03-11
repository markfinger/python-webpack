from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

setting_overrides = getattr(settings, 'DJANGO_WEBPACK', {})

BUNDLE_ROOT = setting_overrides.get(
    'BUNDLE_ROOT',
    settings.STATIC_ROOT,
)
if BUNDLE_ROOT is None:
    raise ImproperlyConfigured(
        'DJANGO_WEBPACK[\'BUNDLE_ROOT\'] defaults to STATIC_ROOT, please define either'
    )

BUNDLE_URL = setting_overrides.get(
    'BUNDLE_URL',
    settings.STATIC_URL,
)
if BUNDLE_URL is None:
    raise ImproperlyConfigured(
        'DJANGO_WEBPACK[\'BUNDLE_URL\'] defaults to STATIC_URL, please define either'
    )
if not BUNDLE_URL.endswith('/'):
    raise ImproperlyConfigured(
        'URL settings (e.g. DJANGO_WEBPACK[\'BUNDLE_ROOT\']) must have a trailing slash'
    )
BUNDLE_URL = settings.STATIC_URL

BUNDLE_DIR = setting_overrides.get(
    'BUNDLE_DIR',
    'webpack',
)

WATCH_CONFIG_FILES = setting_overrides.get(
    'WATCH_CONFIG_FILES',
    settings.DEBUG,
)

WATCH_SOURCE_FILES = setting_overrides.get(
    'WATCH_SOURCE_FILES',
    settings.DEBUG,
)

OUTPUT_FULL_STATS = setting_overrides.get(
    'OUTPUT_FULL_STATS',
    False,
)