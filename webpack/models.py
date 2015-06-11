# Django hook to validate and configure settings on startup

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

FINDER_PATH = 'webpack.django_integration.WebpackFinder'

if (
    ('staticfiles' in settings.INSTALLED_APPS or 'django.contrib.staticfiles' in settings.INSTALLED_APPS) and
    FINDER_PATH not in settings.STATICFILES_FINDERS
):
    raise ImproperlyConfigured(
        (
            'When using webpack together with staticfiles, please add \'{}\' to the '
            'STATICFILES_FINDERS setting.'
        ).format(FINDER_PATH)
    )

import webpack.conf

webpack.conf.settings.configure(
    **getattr(settings, 'WEBPACK', {})
)
