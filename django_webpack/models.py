from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

if (
    ('staticfiles' in settings.INSTALLED_APPS or 'django.contrib.staticfiles' in settings.INSTALLED_APPS) and
    'django_webpack.staticfiles.WebpackFinder' not in settings.STATICFILES_FINDERS
):
    raise ImproperlyConfigured(
        'When using django-webpack together with staticfiles, please add '
        '\'django_webpack.staticfiles.WebpackFinder\' to the STATICFILES_FINDERS setting.'
    )