import sys
import os
import atexit
import subprocess
import time


if 'nosetests' in sys.argv[0]:
    # Configure webpack before any tests are run
    import webpack.conf
    from .settings import WEBPACK
    webpack.conf.settings.configure(**WEBPACK)

from webpack.compiler import build_server

if build_server.is_running():
    raise Exception(
        'A build server is already running at {}, this will cause test failures. The server should be stopped'.format(
            build_server.url
        )
    )

process = subprocess.Popen(
    (
        os.path.join(os.getcwd(), 'node_modules', '.bin', 'webpack-build'),
        '-s'
    ),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

# Ensure the process is killed
atexit.register(lambda _process: _process.kill(), process)

output = process.stdout.readline().decode('utf-8')

if output.strip() == '':
    output += process.stdout.readline().decode('utf-8')

if 'webpack-build v' not in output:
    # Trying to detect issues on Travis
    # raise Exception('Unexpected output: "{}"'.format(output))

    print(output)
    while True:
        print(process.stdout.readline().decode('utf-8'))

# Travis takes a while to boot the server up
print('****travis**** ', os.environ.get('TRAVIS', None), '***CI****', os.environ.get('CI', None))
if os.environ.get('TRAVIS', None):
    for i in xrange(5):
        if not build_server.is_running(True):
            time.sleep(1)

time.sleep(0.5)
if not build_server.is_running():
    raise Exception(
        'The build server appears to have booted, but it is not responding at {} within the expected time period'.format(
            build_server.url
        )
    )
