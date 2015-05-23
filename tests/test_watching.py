import os
import unittest
import time
from webpack.compiler import webpack
from .utils import write_file, read_file, clean_static_root

# The number of seconds that we delay while waiting for
# file changes to be detected
WATCH_WAIT = 0.2

TEST_ROOT = os.path.dirname(__file__)
BUNDLES = os.path.join(TEST_ROOT, 'bundles',)

PATH_TO_WATCHED_CONFIG = os.path.join(BUNDLES, 'watched_config', 'webpack.config.js')
PATH_TO_WATCHED_SOURCE_CONFIG = os.path.join(BUNDLES, 'watched_source', 'webpack.config.js')
PATH_TO_WATCHED_SOURCE_ENTRY = os.path.join(BUNDLES, 'watched_source', 'app', 'entry.js')
PATH_TO_WATCHED_SOURCE_AND_CONFIG_CONFIG = os.path.join(BUNDLES, 'watched_source_and_config', 'webpack.config.js')
PATH_TO_WATCHED_SOURCE_AND_CONFIG_ENTRY = os.path.join(BUNDLES, 'watched_source_and_config', 'app', 'entry2.js')

WATCHED_CONFIG_CONTENT = """
var path = require('path');

module.exports = {
    context: path.join(__dirname, 'app'),
    entry: './entry1.js',
    output: {
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
        filename: 'bundle-[hash].js'
    }
};
"""

WATCHED_SOURCE_AND_CONFIG_ENTRY_CONTENT = """module.exports = '__DJANGO_WEBPACK_WATCH_CONFIG_AND_SOURCE_TWO__';"""


# Ensure that the files are in the state that we expect
write_file(PATH_TO_WATCHED_CONFIG, WATCHED_CONFIG_CONTENT)
write_file(PATH_TO_WATCHED_SOURCE_ENTRY, WATCHED_SOURCE_CONTENT)
write_file(PATH_TO_WATCHED_SOURCE_AND_CONFIG_CONFIG, WATCHED_SOURCE_AND_CONFIG_CONFIG_CONTENT)
write_file(PATH_TO_WATCHED_SOURCE_AND_CONFIG_ENTRY, WATCHED_SOURCE_AND_CONFIG_ENTRY_CONTENT)


class TestWatching(unittest.TestCase):
    _PRODUCTION = True

    @classmethod
    def setUpClass(cls):
        clean_static_root()

    @classmethod
    def tearDownClass(cls):
        clean_static_root()

    def test_config_file_can_be_watched_to_rebuild_the_bundle(self):
        self.assertIn('./entry1.js', WATCHED_CONFIG_CONTENT)
        self.assertEqual(read_file(PATH_TO_WATCHED_CONFIG), WATCHED_CONFIG_CONTENT)

        bundle = webpack(PATH_TO_WATCHED_CONFIG, watch_config=True)

        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_ONE__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_TWO__', contents)

        time.sleep(WATCH_WAIT)
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

        time.sleep(WATCH_WAIT)
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

        time.sleep(WATCH_WAIT)
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

        time.sleep(WATCH_WAIT)
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