import os

# DJANGO
# ======

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

TEMPLATE_DEBUG = DEBUG

SECRET_KEY = '_'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'djangosite.urls'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# DJANGO NODE
# ===========

INSTALLED_APPS += ('django_node',)

DJANGO_NODE = {
    'SERVICES': (
        # Instruct django-node to load in the webpack services
        'django_webpack.services',
    ),
    'PACKAGE_DEPENDENCIES': (
        # Instruct django-node to install the example's dependencies
        # which are located in the example_app/package.json
        os.path.join(BASE_DIR, 'example_app'),
    )
}


# DJANGO WEBPACK
# ==============

INSTALLED_APPS += ('django_webpack',)

STATICFILES_FINDERS += (
    'django_webpack.staticfiles.WebpackFinder',
)


# EXAMPLE APP
# ===========

INSTALLED_APPS += ('example_app',)