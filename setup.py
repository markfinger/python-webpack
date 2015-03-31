from setuptools import setup

VERSION = '3.0.1'

setup(
    name='django-webpack',
    version=VERSION,
    packages=['django_webpack', 'django_webpack.services'],
    package_data={
        'django_webpack': [
            'services/package.json',
            'services/webpack.js',
        ]
    },
    install_requires=[
        'django',
        'django-node==4.0.0',
    ],
    description='Generate Webpack bundles from a Django application.',
    long_description='Documentation at https://github.com/markfinger/django-webpack',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-webpack',
)