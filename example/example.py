import os
from flask import Flask, render_template
from settings import DEBUG, BASE_DIR
from webpack.compiler import webpack

app = Flask(__name__)
app.debug = DEBUG


@app.route('/')
def index():
    # Send a request to the build server
    bundle = webpack(os.path.join(BASE_DIR, 'webpack.config.js'))
    return render_template('index.html', bundle=bundle)


if __name__ == '__main__':
    app.run()