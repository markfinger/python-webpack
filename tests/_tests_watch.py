"""
These tests verify the behaviour of the source and config watching
functionality. They're pretty fragile, slow, and can inexplicably
not work in certain environments.

To prevent these tests from running, start the test runner with
the --no-watch-tests argument.
"""

import os
import unittest
import time
import shutil
from django_webpack.services import WebpackService
from django_webpack.compiler import webpack
from .settings import STATIC_ROOT

# The number of seconds that we delay while waiting for
# file changes to be detected
WATCH_WAIT = 2

TEST_ROOT = os.path.dirname(__file__)

PATH_TO_WATCHED_CONFIG = os.path.join(TEST_ROOT, 'watched_config_bundle', 'webpack.config.js')
PATH_TO_WATCHED_SOURCE_CONFIG = os.path.join(TEST_ROOT, 'watched_source_bundle', 'webpack.config.js')
PATH_TO_WATCHED_SOURCE_ENTRY = os.path.join(TEST_ROOT, 'watched_source_bundle', 'app', 'entry.js')
PATH_TO_WATCHED_SOURCE_AND_CONFIG_CONFIG = os.path.join(
    TEST_ROOT,
    'watched_source_and_config_bundle',
    'webpack.config.js'
)
PATH_TO_WATCHED_SOURCE_AND_CONFIG_ENTRY = os.path.join(
    TEST_ROOT,
    'watched_source_and_config_bundle',
    'app',
    'entry2.js'
)

WATCHED_CONFIG_CONTENT = """
var path = require('path');

module.exports = {
    context: path.join(__dirname, 'app'),
    entry: './entry1.js',
    output: {
        path: '[bundle_dir]',
        filename: 'bundle-[hash].js'
    }
};
"""

WATCHED_SOURCE_CONTENT = """module.exports = '__DJANGO_WEBPACK_WATCH_SOURCE_ONE__';"""

WATCHED_SOURCE_AND_CONFIG_CONFIG_CONTENT = """
var path = require('path');

module.exports = {
    context: path.join(__dirname, 'app'),
    entry: './entry1.js',
    output: {
        path: '[bundle_dir]',
        filename: 'bundle-[hash].js'
    }
};
"""

WATCHED_SOURCE_AND_CONFIG_ENTRY_CONTENT = """module.exports = '__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_TWO__';"""


def write_file(file_name, content):
    with open(file_name, 'w') as _file:
        _file.write(content)


def read_file(file_name):
    with open(file_name, 'r') as _file:
        return _file.read()

# Ensure that the files are in the state that we expect
write_file(PATH_TO_WATCHED_CONFIG, WATCHED_CONFIG_CONTENT)
write_file(PATH_TO_WATCHED_SOURCE_ENTRY, WATCHED_SOURCE_CONTENT)
write_file(PATH_TO_WATCHED_SOURCE_AND_CONFIG_CONFIG, WATCHED_SOURCE_AND_CONFIG_CONFIG_CONTENT)
write_file(PATH_TO_WATCHED_SOURCE_AND_CONFIG_ENTRY, WATCHED_SOURCE_AND_CONFIG_ENTRY_CONTENT)

# Are we testing against a persistent service?
if WebpackService().get_server().test():
    # Wait for the service to detect the changes to the files
    time.sleep(WATCH_WAIT)
else:
    # Clean out any files generated from previous test runs
    if os.path.exists(STATIC_ROOT):
        shutil.rmtree(STATIC_ROOT)

class TestDjangoWebpack(unittest.TestCase):
    def test_config_file_can_be_watched_to_rebuild_the_bundle(self):
        self.assertIn('./entry1.js', WATCHED_CONFIG_CONTENT)
        self.assertEqual(read_file(PATH_TO_WATCHED_CONFIG), WATCHED_CONFIG_CONTENT)
        bundle = webpack(PATH_TO_WATCHED_CONFIG, watch_config=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_ONE__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_TWO__', contents)
        changed_config = WATCHED_CONFIG_CONTENT.replace('./entry1.js', './entry2.js')
        self.assertNotIn('./entry1.js', changed_config)
        write_file(PATH_TO_WATCHED_CONFIG, changed_config)
        time.sleep(WATCH_WAIT)
        bundle = webpack(PATH_TO_WATCHED_CONFIG, watch_config=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_ONE__', contents)
        self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_TWO__', contents)

    def test_source_files_can_be_watched_to_rebuild_a_bundle(self):
        self.assertEqual(read_file(PATH_TO_WATCHED_SOURCE_ENTRY), WATCHED_SOURCE_CONTENT)
        bundle = webpack(PATH_TO_WATCHED_SOURCE_CONFIG, watch_source=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertIn('__DJANGO_WEBPACK_WATCH_SOURCE_ONE__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_SOURCE_TWO__', contents)
        write_file(PATH_TO_WATCHED_SOURCE_ENTRY, """module.exports = '__DJANGO_WEBPACK_WATCH_SOURCE_TWO__';""")
        time.sleep(WATCH_WAIT)
        bundle = webpack(PATH_TO_WATCHED_SOURCE_CONFIG, watch_source=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_SOURCE_ONE__', contents)
        self.assertIn('__DJANGO_WEBPACK_WATCH_SOURCE_TWO__', contents)

    def test_source_and_config_files_can_be_watched_to_rebuild_a_bundle(self):
        self.assertEqual(read_file(PATH_TO_WATCHED_SOURCE_AND_CONFIG_CONFIG), WATCHED_SOURCE_AND_CONFIG_CONFIG_CONTENT)
        bundle = webpack(PATH_TO_WATCHED_SOURCE_AND_CONFIG_CONFIG, watch_config=True, watch_source=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_ONE__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_TWO__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_THREE__', contents)
        changed_config = WATCHED_SOURCE_AND_CONFIG_CONFIG_CONTENT.replace('./entry1.js', './entry2.js')
        self.assertNotIn('./entry1.js', changed_config)
        write_file(PATH_TO_WATCHED_SOURCE_AND_CONFIG_CONFIG, changed_config)
        time.sleep(WATCH_WAIT)
        bundle = webpack(PATH_TO_WATCHED_SOURCE_AND_CONFIG_CONFIG, watch_config=True, watch_source=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_ONE__', contents)
        self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_TWO__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_THREE__', contents)
        changed_source = """module.exports = '__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_THREE__';"""
        write_file(PATH_TO_WATCHED_SOURCE_AND_CONFIG_ENTRY, changed_source)
        time.sleep(WATCH_WAIT)
        bundle = webpack(PATH_TO_WATCHED_SOURCE_AND_CONFIG_CONFIG, watch_config=True, watch_source=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_ONE__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_TWO__', contents)
        self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_THREE__', contents)