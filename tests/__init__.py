import sys
import os
import atexit
import subprocess
import shutil

# Ensure any file caching is cleared before a run
cache_dir = os.path.join(os.getcwd(), '.webpack_cache')
if os.path.exists(cache_dir) and os.path.isdir(cache_dir):
    shutil.rmtree(cache_dir)

if 'nosetests' in sys.argv[0]:
    # Configure js-host and webpack before any tests are run
    import webpack.conf
    from .settings import WEBPACK
    webpack.conf.settings.configure(**WEBPACK)

from webpack.server import server

if server.is_running():
    raise Exception(
        'A build server is already running at {}, this will cause test failures. The server should be stopped'.format(
            server.url
        )
    )

process = subprocess.Popen(
    (os.path.join(os.getcwd(), 'node_modules', '.bin', 'webpack-build'),),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

# Ensure the process is killed
atexit.register(lambda _process: _process.kill(), process)

output = process.stdout.readline().decode('utf-8')

if output.strip() == '':
    output += process.stdout.readline().decode('utf-8')

if 'webpack-build v' not in output:
    raise Exception('Unexpected output: "{}"'.format(output))
