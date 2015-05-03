from setuptools import setup
import webpack

setup(
    name='webpack',
    version=webpack.__version__,
    packages=['webpack'],
    install_requires=[
        'optional-django==0.2.1'
    ],
    description='Python bindings to Webpack',
    long_description='Documentation at https://github.com/markfinger/python-webpack',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/python-webpack',
)