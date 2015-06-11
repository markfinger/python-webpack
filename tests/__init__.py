import sys
import os
import atexit
import subprocess
import shutil

cache_dir = os.path.join(os.getcwd(), '.webpack_cache')
if os.path.exists(cache_dir) and os.path.isdir(cache_dir):
    shutil.rmtree(cache_dir)

if 'nosetests' in sys.argv[0]:
    # Configure js-host and webpack before any tests are run
    import webpack.conf
    from .settings import WEBPACK
    webpack.conf.settings.configure(**WEBPACK)

process = subprocess.Popen(
    (os.path.join(os.getcwd(), 'node_modules', '.bin', 'webpack-build-server'),),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

atexit.register(lambda _process: _process.kill(), process)

output = process.stdout.readline()

output = output.decode('utf-8')

if not output.startswith('~'):
    raise Exception('Unexpected output {}'.format(output))
