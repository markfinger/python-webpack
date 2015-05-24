from flask import Flask, render_template
from webpack.compiler import webpack
from settings import DEBUG, CONFIG_FILE

app = Flask(__name__)
app.debug = DEBUG


@app.route('/')
def index():
    # Ask the compiler to either start building or provide the details of the
    # most recent build
    bundle = webpack(CONFIG_FILE)
    return render_template('index.html', bundle=bundle)


if __name__ == '__main__':
    app.run()