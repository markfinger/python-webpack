import os
from js_host.utils import verbosity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = '_'

STATIC_ROOT = os.path.join(BASE_DIR, '__STATIC_ROOT__')
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

STATICFILES_STORAGE = 'webpack.django_integration.WebpackOfflineStaticFilesStorage'

STATICFILES_DIRS = (
    # Give Django access the the bundles directory.
    os.path.join(BASE_DIR, 'bundles'),
)

WEBPACK = {
    'STATIC_ROOT': STATIC_ROOT,
    'STATIC_URL': STATIC_URL,
    # Prevent caching across processes
    'CACHE_FILE': None
}

JS_HOST = {
    'SOURCE_ROOT': BASE_DIR,
    # Let the manager spin up an instance
    'USE_MANAGER': True,
    'VERBOSITY': verbosity.SILENT,
}


TEST_ROOT = os.path.dirname(__file__)
BUNDLES = os.path.join(TEST_ROOT, 'bundles',)


class ConfigFiles(object):
    BASIC_CONFIG = os.path.join(BUNDLES, 'basic', 'webpack.config.js')
    LIBRARY_CONFIG = os.path.join(BUNDLES, 'library', 'webpack.config.js')
    MULTIPLE_BUNDLES_CONFIG = os.path.join(BUNDLES, 'multiple_bundles', 'webpack.config.js')
    MULTIPLE_ENTRY_CONFIG = os.path.join(BUNDLES, 'multiple_entry', 'webpack.config.js')
    CACHED_CONFIG = os.path.join(BUNDLES, 'cached', 'webpack.config.js')