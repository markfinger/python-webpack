from setuptools import setup

VERSION = '0.1.0'

setup(
    name='django-webpack',
    version=VERSION,
    packages=['django_webpack'],
    package_data={
        'django_webpack': [
            '*.js',
            '*.json',
            'tests/*.py'
        ]
    },
    install_requires=[
        'django',
        'django-node >= 1.0.0',
    ],
    description='Django Webpack',
    long_description=\
'''
Provides an interface for Django to use Webpack to generate bundles.

Documentation at https://github.com/markfinger/django-webpack
''',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-webpack',
)