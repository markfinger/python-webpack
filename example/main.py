import os
from flask import Flask, render_template
from webpack.compiler import webpack
from settings import DEBUG, BASE_DIR

app = Flask(__name__)
app.debug = DEBUG

# An absolute path to the bundle's config file
webpack_config = os.path.join(BASE_DIR, 'static', 'js', 'webpack.config.js')

@app.route('/')
def index():

    # Call the compiler to either start building the bundle or provide the details
    # of the most recent build
    bundle = webpack(webpack_config)

    return render_template('index.html', bundle=bundle)


if __name__ == '__main__':
    app.run()