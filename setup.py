from setuptools import setup

VERSION = '1.0.0'

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
        'django-node >= 2.0.0',
    ],
    description='Django Webpack',
    long_description=\
'''
Generate Webpack bundles from a Django application.

Documentation at https://github.com/markfinger/django-webpack
''',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-webpack',
)