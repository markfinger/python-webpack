from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import webpack.conf

FINDER_PATH = 'webpack.django_integration.WebpackFinder'


class WebpackConfig(AppConfig):
    name = 'webpack'

    def ready(self):
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

        webpack.conf.settings.configure(
            **getattr(settings, 'WEBPACK', {})
        )