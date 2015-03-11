import os
import unittest
import time
import shutil
from django.contrib.staticfiles import finders
from django_webpack.services import WebpackService
from django_webpack.compiler import webpack, WebpackBundle
from django_webpack.settings import BUNDLE_ROOT, BUNDLE_URL, BUNDLE_DIR
from django_webpack.exceptions import ConfigNotFound
from .settings import STATIC_ROOT

# The number of seconds that we delay while waiting for
# file changes to be detected
WATCH_WAIT = 10

TEST_ROOT = os.path.dirname(__file__)

PATH_TO_BASIC_CONFIG = os.path.join(TEST_ROOT, 'basic_bundle', 'webpack.config.js')
PATH_TO_LIBRARY_CONFIG = os.path.join(TEST_ROOT, 'library_bundle', 'webpack.config.js')
PATH_TO_MULTIPLE_BUNDLES_CONFIG = os.path.join(TEST_ROOT, 'multiple_bundles', 'webpack.config.js')
PATH_TO_MULTIPLE_ENTRY_CONFIG = os.path.join(TEST_ROOT, 'multiple_entry_bundle', 'webpack.config.js')
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
    def test_bundle_raises_configfilenotfound_for_nonexistent_config_files(self):
        self.assertRaises(ConfigNotFound, webpack, '/file/that/does/not/exist.js')

    def test_bundle_create_a_file_with_contents(self):
        bundle = webpack(PATH_TO_BASIC_CONFIG)
        assets = bundle.get_assets()
        self.assertEqual(len(assets), 1)
        asset = assets[0]
        self.assertTrue(asset['name'].startswith('bundle-'))
        self.assertTrue(asset['name'].endswith('.js'))
        self.assertEqual(asset['path'], os.path.join(BUNDLE_ROOT, BUNDLE_DIR, asset['name']))
        self.assertTrue(os.path.exists(asset['path']))
        self.assertTrue(os.path.exists(os.path.join(BUNDLE_ROOT, BUNDLE_DIR, asset['name'])))
        self.assertEqual(BUNDLE_URL + BUNDLE_DIR + '/' + asset['name'], asset['url'])
        contents = read_file(asset['path'])
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_REQUIRE_TEST__', contents)

    def test_webpack_returns_webpack_bundle_instances(self):
        bundle = webpack(PATH_TO_BASIC_CONFIG)
        self.assertIsInstance(bundle, WebpackBundle)

    def test_webpack_bundles_can_return_urls_to_assets(self):
        bundle = webpack(PATH_TO_BASIC_CONFIG)
        asset = bundle.get_assets()[0]
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        self.assertEqual(urls[0], '/static/webpack/' + asset['name'])

    def test_can_render_a_webpack_bundle(self):
        bundle = webpack(PATH_TO_BASIC_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        rendered = bundle.render()
        self.assertIn(urls[0], rendered)
        self.assertEqual(rendered, '<script src="' + urls[0] + '"></script>')

    def test_bundle_can_handle_a_bundle_with_multiple_entries(self):
        bundle = webpack(PATH_TO_MULTIPLE_ENTRY_CONFIG)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_ONE__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TWO__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_THREE__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_FOUR__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_FIVE__', contents)

    def test_can_render_a_bundle_with_multiple_entries(self):
        bundle = webpack(PATH_TO_MULTIPLE_ENTRY_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        rendered = bundle.render()
        self.assertIn(urls[0], rendered)
        self.assertEqual(rendered, '<script src="' + urls[0] + '"></script>')

    def test_can_render_a_bundle_with_multiple_entry_points(self):
        bundle = webpack(PATH_TO_MULTIPLE_ENTRY_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        rendered = bundle.render()
        self.assertIn(urls[0], rendered)
        self.assertEqual(rendered, '<script src="' + urls[0] + '"></script>')

    def test_bundle_can_handle_multiple_bundles(self):
        bundle = webpack(PATH_TO_MULTIPLE_BUNDLES_CONFIG)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 2)
        asset_names = [asset['name'] for asset in assets]
        self.assertIn('bundle-bundle_1.js', asset_names)
        self.assertIn('bundle-bundle_2.js', asset_names)
        bundle_1 = [asset for asset in assets if asset['name'] == 'bundle-bundle_1.js'][0]
        bundle_2 = [asset for asset in assets if asset['name'] == 'bundle-bundle_2.js'][0]
        self.assertEqual(bundle_1['name'], 'bundle-bundle_1.js')
        self.assertEqual(bundle_2['name'], 'bundle-bundle_2.js')
        bundle_1_contents = read_file(bundle_1['path'])
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', bundle_1_contents)
        self.assertIn('__DJANGO_WEBPACK_BUNDLE_ONE__', bundle_1_contents)
        self.assertNotIn('__DJANGO_WEBPACK_BUNDLE_TWO__', bundle_1_contents)
        bundle_2_contents = read_file(bundle_2['path'])
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', bundle_2_contents)
        self.assertNotIn('__DJANGO_WEBPACK_BUNDLE_ONE__', bundle_2_contents)
        self.assertIn('__DJANGO_WEBPACK_BUNDLE_TWO__', bundle_2_contents)

    def test_bundle_can_render_multiple_bundles(self):
        bundle = webpack(PATH_TO_MULTIPLE_BUNDLES_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 2)
        rendered = bundle.render()
        for url in urls:
            self.assertIn(url, bundle.render())
        self.assertEqual(rendered, '<script src="' + urls[0] + '"></script><script src="' + urls[1] + '"></script>')

    def test_bundle_can_resolve_files_via_the_django_static_file_finder(self):
        bundle = webpack('test_app/webpack.config.js')
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_STATIC_FILE_FINDER_TEST__', contents)

    def test_bundle_urls_can_be_resolved_via_the_dev_servers_static_files(self):
        bundle = webpack('test_app/webpack.config.js')
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        relative_url = assets[0]['url'].split('/static/')[-1]
        self.assertEqual(finders.find(relative_url), assets[0]['path'])

    def test_bundle_can_expose_the_bundling_processes_output(self):
        bundle = webpack(PATH_TO_LIBRARY_CONFIG)
        output = bundle.output
        self.assertIn('stats', output)
        self.assertIsInstance(output['stats'], dict)
        self.assertIn('config', output)
        self.assertIsInstance(output['config'], dict)
        self.assertEqual(output['pathToConfig'], PATH_TO_LIBRARY_CONFIG)
        self.assertEqual(output['watchSource'], False)
        self.assertEqual(output['watchConfig'], False)

    def test_bundle_can_expose_its_config(self):
        bundle = webpack(PATH_TO_BASIC_CONFIG)
        config = bundle.get_config()
        self.assertDictContainsSubset(
            {
                'context': os.path.join(TEST_ROOT, 'basic_bundle', 'app'),
                'entry': './entry.js',
            },
            config
        )
        self.assertDictContainsSubset(
            {
                'path': os.path.join(BUNDLE_ROOT, BUNDLE_DIR),
                'filename': 'bundle-[hash].js'
            },
            config['output']
        )

    def test_bundle_can_expose_its_library_config(self):
        bundle = webpack(PATH_TO_LIBRARY_CONFIG)
        self.assertEqual(bundle.get_library(), 'LIBRARY_TEST')

        bundle = webpack(PATH_TO_MULTIPLE_BUNDLES_CONFIG)
        self.assertIsNone(bundle.get_library())

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