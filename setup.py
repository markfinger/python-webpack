from setuptools import setup

VERSION = '1.0.1'

setup(
    name='django-webpack',
    version=VERSION,
    packages=['django_webpack'],
    package_data={
        'django_webpack': [
            '*.js',
            '*.json',
            'tests/*.py'
            'tests/test_bundle.js'
        ]
    },
    install_requires=[
        'django',
        'django-node >= 2.0.1',
    ],
    description='Generate Webpack bundles from a Django application.',
    long_description='Documentation at https://github.com/markfinger/django-webpack',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-webpack',
)