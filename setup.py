from setuptools import setup
import webpack

setup(
    name='webpack',
    version=webpack.__version__,
    packages=[
        'webpack',
        'webpack.templatetags',
        'webpack.management.commands',
    ],
    install_requires=[
        'requests>=2.5.0',
        'optional-django==0.3.0'
    ],
    description='Python bindings to Webpack',
    long_description='Documentation at https://github.com/markfinger/python-webpack',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/python-webpack',
)