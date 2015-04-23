from setuptools import setup
import webpack

setup(
    name='webpack',
    version=webpack.VERSION,
    packages=['webpack'],
    install_requires=[
        'django-node==4.0.0',
        'optional-django==0.1.0'
    ],
    description='Generate Webpack bundles from a Django application.',
    long_description='Documentation at https://github.com/markfinger/django-webpack',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-webpack',
)