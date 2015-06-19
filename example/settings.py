import os
from webpack.conf import settings

DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    # The root directory that static assets are located in
    STATIC_ROOT=os.path.join(BASE_DIR, 'static'),
    # The url that STATIC_ROOT is served from
    STATIC_URL='/static/',
    # Turn on source watching in development
    WATCH=DEBUG,
    # Turn on hmr in development
    HMR=DEBUG,
    ENV='dev' if DEBUG else 'prod',
)