from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_WEBPACK', {})

# TODO sort out a default for this or raise an error
BUNDLE_ROOT = setting_overrides.get(
    'BUNDLE_ROOT',
    None,
)

# TODO: sort this out as well
BUNDLE_URL = setting_overrides.get(
    'BUNDLE_URL',
    None,
)

CACHE = setting_overrides.get(
    'CACHE',
    not settings.DEBUG,
)