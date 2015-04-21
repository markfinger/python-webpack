from setuptools import setup
import django_webpack

setup(
    name='django-webpack',
    version=django_webpack.VERSION,
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
        'optional-django==0.1.0'
    ],
    description='Generate Webpack bundles from a Django application.',
    long_description='Documentation at https://github.com/markfinger/django-webpack',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-webpack',
)