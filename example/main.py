import os
from flask import Flask, render_template
from webpack.compiler import webpack
from settings import DEBUG, BASE_DIR

app = Flask(__name__)
app.debug = DEBUG


@app.route('/')
def hello():
    # An absolute path to bundle's config file
    webpack_config = os.path.join(BASE_DIR, 'static', 'js', 'webpack.config.js')

    # Call the compiler to either build the bundle or - if it has
    # already been built - provide the details of the most recent
    # build
    bundle = webpack(webpack_config)

    return render_template('index.html', bundle=bundle)


if __name__ == '__main__':
    app.run()