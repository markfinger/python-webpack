import os

DEBUG = True

SECRET_KEY = '_'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static_root')

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'tests.test_app',
)

DJANGO_NODE = {
    'SERVICES': (
        'django_webpack.services',
    ),
    'INSTALL_PACKAGE_DEPENDENCIES_DURING_RUNTIME': True,
}

DJANGO_WEBPACK = {
    'BUNDLE_ROOT': os.path.join(STATIC_ROOT, 'bundles'),
    'BUNDLE_URL': STATIC_URL + 'bundles/',
    # Uncomment these to test the dev helpers
    # 'WATCH_CONFIG_FILES': True,
    # 'WATCH_SOURCE_FILES': True
}