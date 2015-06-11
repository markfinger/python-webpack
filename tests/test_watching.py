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

PATH_TO_WATCHED_SOURCE_CONFIG = os.path.join(BUNDLES, 'watched_source', 'webpack.config.js')
PATH_TO_WATCHED_SOURCE_ENTRY = os.path.join(BUNDLES, 'watched_source', 'app', 'entry.js')

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


# Ensure that the files are in the state that we expect
write_file(PATH_TO_WATCHED_SOURCE_ENTRY, WATCHED_SOURCE_CONTENT)


class TestWatching(unittest.TestCase):
    _PRODUCTION = True

    @classmethod
    def setUpClass(cls):
        clean_static_root()

    @classmethod
    def tearDownClass(cls):
        clean_static_root()

    def test_source_files_can_be_watched_to_rebuild_a_bundle(self):
        self.assertEqual(read_file(PATH_TO_WATCHED_SOURCE_ENTRY), WATCHED_SOURCE_CONTENT)

        bundle = webpack(PATH_TO_WATCHED_SOURCE_CONFIG, watch=True)

        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0])
        self.assertIn('__DJANGO_WEBPACK_WATCH_SOURCE_ONE__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_SOURCE_TWO__', contents)

        time.sleep(WATCH_WAIT)
        write_file(PATH_TO_WATCHED_SOURCE_ENTRY, """module.exports = '__DJANGO_WEBPACK_WATCH_SOURCE_TWO__';""")
        time.sleep(WATCH_WAIT)

        bundle = webpack(PATH_TO_WATCHED_SOURCE_CONFIG, watch=True)

        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0])
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_SOURCE_ONE__', contents)
        self.assertIn('__DJANGO_WEBPACK_WATCH_SOURCE_TWO__', contents)