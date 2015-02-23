import os

DEBUG = True

SECRET_KEY = '_'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static_root')

DJANGO_NODE = {
    'SERVICES': (
        'django_webpack.services',
    )
}

DJANGO_WEBPACK = {
    'BUNDLE_ROOT': os.path.join(STATIC_ROOT, 'bundles'),
    'BUNDLE_URL': STATIC_URL + 'bundles/',
}