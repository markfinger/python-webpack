import os
from flask import Flask, render_template
from webpack.conf import settings
from webpack.compiler import webpack

DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    # The root directory that static assets are located in
    STATIC_ROOT=os.path.join(BASE_DIR, 'static'),
    # The url that STATIC_ROOT is served from
    STATIC_URL='/static/',
    CONFIG_DIRS=(
        os.path.join(BASE_DIR, '..'),
    ),
    # Turn on source watching in development
    WATCH=DEBUG,
    # Turn on hmr in development
    HMR=DEBUG,
    CONTEXT={
        'DEBUG': DEBUG
    },
)

app = Flask(__name__)
app.debug = DEBUG


@app.route('/')
def index():
    return render_template(
        'index.html',
        # Send a request to the build server
        bundle=webpack('example.webpack.js')
    )


if __name__ == '__main__':
    app.run()