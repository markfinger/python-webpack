import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = '_'

STATIC_ROOT = os.path.join(BASE_DIR, '__STATIC_ROOT__')
STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'tests.django_test_app',
    'webpack',
)

STATICFILES_FINDERS = (
    # Defaults
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # Webpack finder
    'webpack.django_integration.WebpackFinder',
)

BUNDLES = os.path.join(BASE_DIR, 'bundles',)

WEBPACK = {
    'STATIC_ROOT': STATIC_ROOT,
    'STATIC_URL': STATIC_URL,
    'CONTEXT': {
        'default_context': 'test'
    },
    'CONFIG_DIRS': (
        BASE_DIR,
        BUNDLES,
    ),
    # While webpack-build's cache will check for asset existence,
    # watching compilers do not, so we need to ensure that the cache
    # is cleared between runs
    'CACHE_DIR': os.path.join(STATIC_ROOT, 'cache_dir'),
}


class ConfigFiles(object):
    BASIC_CONFIG = os.path.join('basic', 'webpack.config.js')
    LIBRARY_CONFIG = os.path.join('library', 'webpack.config.js')
    MULTIPLE_BUNDLES_CONFIG = os.path.join('multiple_bundles', 'webpack.config.js')
    MULTIPLE_ENTRY_CONFIG = os.path.join('multiple_entry', 'webpack.config.js')
    CACHED_CONFIG = os.path.join('cached', 'webpack.config.js')