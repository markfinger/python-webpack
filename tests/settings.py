import os
from js_host.utils import verbosity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = '_'

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'tests.django_test_app',
    'js_host',
    'webpack',
)

STATICFILES_FINDERS = (
    # Defaults
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # Webpack finder
    'webpack.django_integration.WebpackFinder',
)

WEBPACK = {
    'BUNDLE_ROOT': os.path.join(BASE_DIR, '__BUNDLE_ROOT__'),
    'BUNDLE_URL': '/static/',
}

JS_HOST = {
    'SOURCE_ROOT': BASE_DIR,
    # Let the manager spin up an instance
    'USE_MANAGER': True,
    'VERBOSITY': verbosity.SILENT,
}