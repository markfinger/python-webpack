import os

DEBUG = True

SECRET_KEY = '_'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static_root')

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'tests.test_app',
)

STATICFILES_FINDERS = (
    # Defaults
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # Webpack finder
    'django_webpack.staticfiles.WebpackFinder',
)

DJANGO_NODE = {
    'SERVICES': (
        'django_webpack.services',
    ),
}