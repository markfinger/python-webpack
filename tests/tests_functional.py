import os
import unittest
import time
from django_webpack.compiler import webpack, WebpackBundle
from django_webpack.settings import BUNDLE_ROOT
from django_webpack.exceptions import ConfigNotFound

TEST_ROOT = os.path.dirname(__file__)

BASIC_BUNDLE_CONFIG = os.path.join(TEST_ROOT, 'basic_bundle', 'webpack.config.js')
LIBRARY_BUNDLE_CONFIG = os.path.join(TEST_ROOT, 'library_bundle', 'webpack.config.js')
MULTIPLE_BUNDLES_CONFIG = os.path.join(TEST_ROOT, 'multiple_bundles', 'webpack.config.js')
MULTIPLE_ENTRY_BUNDLE_CONFIG = os.path.join(TEST_ROOT, 'multiple_entry_bundle', 'webpack.config.js')
WATCHED_CONFIG_BUNDLE_CONFIG = os.path.join(TEST_ROOT, 'watched_config_bundle', 'webpack.config.js')
WATCHED_SOURCE_BUNDLE_CONFIG = os.path.join(TEST_ROOT, 'watched_source_bundle', 'webpack.config.js')
WATCHED_SOURCE_BUNDLE_ENTRY = os.path.join(TEST_ROOT, 'watched_source_bundle', 'app', 'entry.js')
WATCHED_SOURCE_AND_CONFIG_BUNDLE_CONFIG = os.path.join(TEST_ROOT, 'watched_source_and_config_bundle', 'app', 'webpack.config.js')
WATCHED_SOURCE_AND_CONFIG_BUNDLE_ENTRY = os.path.join(TEST_ROOT, 'watched_source_and_config_bundle', 'app', 'entry.js')

watched_config = """
var path = require('path');

module.exports = {
    context: path.join(__dirname, 'app'),
    entry: './entry1.js',
    output: {
        path: '{{ BUNDLE_ROOT }}',
        filename: 'bundle-[hash].js'
    }
};
"""
with open(WATCHED_CONFIG_BUNDLE_CONFIG, 'w') as watched_config_file:
    watched_config_file.write(watched_config)


watched_source = """module.exports = '__DJANGO_WEBPACK_WATCH_SOURCE_ONE__';"""
with open(WATCHED_SOURCE_BUNDLE_ENTRY, 'w') as watched_entry_file:
    watched_entry_file.write(watched_source)

# watched_source_and_config_config = """
# var path = require('path');
#
# module.exports = {
#     context: path.join(__dirname, 'app'),
#     entry: './entry1.js',
#     output: {
#         path: '{{ BUNDLE_ROOT }}',
#         filename: 'bundle-[hash].js'
#     }
# };
# """
# with open(WATCHED_SOURCE_AND_CONFIG_BUNDLE_CONFIG, 'w') as watched_config_file:
#     watched_config_file.write(watched_config)


class TestDjangoWebpack(unittest.TestCase):
    def test_bundle_raises_configfilenotfound_for_nonexistent_config_files(self):
        self.assertRaises(ConfigNotFound, webpack, '/file/that/does/not/exist.js')

    def test_bundle_create_a_file_with_contents(self):
        bundle = webpack(BASIC_BUNDLE_CONFIG)
        assets = bundle.get_assets()
        self.assertEqual(len(assets), 1)
        asset = assets[0]

        self.assertTrue(asset['name'].startswith('bundle-'))
        self.assertTrue(asset['name'].endswith('.js'))

        self.assertEqual(asset['path'], os.path.join(BUNDLE_ROOT, asset['name']))
        self.assertTrue(os.path.exists(asset['path']))
        self.assertTrue(os.path.exists(os.path.join(BUNDLE_ROOT, asset['name'])))

        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()

        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_REQUIRE_TEST__', contents)

    def test_webpack_returns_webpack_bundle_instances(self):
        bundle = webpack(BASIC_BUNDLE_CONFIG)
        self.assertIsInstance(bundle, WebpackBundle)

    def test_webpack_bundles_can_return_urls_to_assets(self):
        bundle = webpack(BASIC_BUNDLE_CONFIG)
        asset = bundle.get_assets()[0]
        urls = bundle.get_urls()

        self.assertTrue(len(urls), 1)
        url = urls[0]

        self.assertEqual(url, '/static/bundles/' + asset['name'])

    def test_can_render_a_webpack_bundle(self):
        bundle = webpack(BASIC_BUNDLE_CONFIG)

        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        url = urls[0]

        rendered = bundle.render()

        self.assertIn(url, rendered)
        self.assertEqual(rendered, '<script src="' + url + '"></script>')

    def test_bundle_can_handle_a_bundle_with_multiple_entries(self):
        bundle = webpack(MULTIPLE_ENTRY_BUNDLE_CONFIG)

        assets = bundle.get_assets()

        self.assertTrue(len(assets), 1)
        asset = assets[0]

        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()

        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_ONE__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TWO__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_THREE__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_FOUR__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_FIVE__', contents)

    def test_can_render_a_bundle_with_multiple_entries(self):
        bundle = webpack(MULTIPLE_ENTRY_BUNDLE_CONFIG)

        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        url = urls[0]

        rendered = bundle.render()

        self.assertIn(url, rendered)
        self.assertEqual(rendered, '<script src="' + url + '"></script>')

    def test_can_render_a_bundle_with_multiple_entry_points(self):
        bundle = webpack(MULTIPLE_ENTRY_BUNDLE_CONFIG)

        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        url = urls[0]

        rendered = bundle.render()

        self.assertIn(url, rendered)
        self.assertEqual(rendered, '<script src="' + url + '"></script>')

    def test_bundle_can_handle_multiple_bundles(self):
        bundle = webpack(MULTIPLE_BUNDLES_CONFIG)

        assets = bundle.get_assets()

        self.assertTrue(len(assets), 2)

        asset_names = [asset['name'] for asset in assets]
        self.assertIn('bundle-bundle_1.js', asset_names)
        self.assertIn('bundle-bundle_2.js', asset_names)

        bundle_1 = [asset for asset in assets if asset['name'] == 'bundle-bundle_1.js'][0]
        bundle_2 = [asset for asset in assets if asset['name'] == 'bundle-bundle_2.js'][0]

        self.assertEqual(bundle_1['name'], 'bundle-bundle_1.js')
        self.assertEqual(bundle_2['name'], 'bundle-bundle_2.js')
        
        with open(bundle_1['path'], 'r') as bundle_1_file:
            bundle_1_contents = bundle_1_file.read()

        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', bundle_1_contents)
        self.assertIn('__DJANGO_WEBPACK_BUNDLE_ONE__', bundle_1_contents)
        self.assertNotIn('__DJANGO_WEBPACK_BUNDLE_TWO__', bundle_1_contents)
        
        with open(bundle_2['path'], 'r') as bundle_2_file:
            bundle_2_contents = bundle_2_file.read()

        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', bundle_2_contents)
        self.assertNotIn('__DJANGO_WEBPACK_BUNDLE_ONE__', bundle_2_contents)
        self.assertIn('__DJANGO_WEBPACK_BUNDLE_TWO__', bundle_2_contents)

    def test_bundle_can_render_multiple_bundles(self):
        bundle = webpack(MULTIPLE_BUNDLES_CONFIG)

        urls = bundle.get_urls()

        self.assertTrue(len(urls), 2)

        rendered = bundle.render()

        for url in urls:
            self.assertIn(url, bundle.render())

        self.assertEqual(
            rendered,
            '<script src="' + urls[0] + '"></script><script src="' + urls[1] + '"></script>'
        )

    def test_bundle_can_resolve_files_via_the_django_static_file_finder(self):
        bundle = webpack('test_app/webpack.config.js')

        assets = bundle.get_assets()

        self.assertTrue(len(assets), 1)

        asset = assets[0]

        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()

        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_STATIC_FILE_FINDER_TEST__', contents)

    def test_bundle_can_expose_the_bundling_processes_output(self):
        bundle = webpack(LIBRARY_BUNDLE_CONFIG)
        output = bundle.output
        self.assertIn('stats', output)
        self.assertIsInstance(output['stats'], dict)
        self.assertIn('config', output)
        self.assertIsInstance(output['config'], dict)

    def test_bundle_can_expose_its_config(self):
        bundle = webpack(BASIC_BUNDLE_CONFIG)
        config = bundle.get_config()
        self.assertDictContainsSubset({
            'context': os.path.join(TEST_ROOT, 'basic_bundle', 'app'),
            'entry': './entry.js',
        }, config)
        self.assertDictContainsSubset({
            'path': BUNDLE_ROOT,
            'filename': 'bundle-[hash].js'
        }, config['output'])

    def test_bundle_can_expose_its_library_config(self):
        bundle = webpack(LIBRARY_BUNDLE_CONFIG)
        self.assertEqual(bundle.get_library(), 'LIBRARY_TEST')

        bundle = webpack(MULTIPLE_BUNDLES_CONFIG)
        self.assertIsNone(bundle.get_library())

    def test_config_file_can_be_watched_to_rebuild_the_bundle(self):
        self.assertIn('./entry1.js', watched_config)
        with open(WATCHED_CONFIG_BUNDLE_CONFIG, 'r') as config_file:
            self.assertEqual(watched_config, config_file.read())

        bundle = webpack(WATCHED_CONFIG_BUNDLE_CONFIG, watch_config=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        asset = assets[0]
        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()
        self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_ONE__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_TWO__', contents)

        changed_config = watched_config.replace('./entry1.js', './entry2.js')
        self.assertNotIn('./entry1.js', changed_config)
        with open(WATCHED_CONFIG_BUNDLE_CONFIG, 'w') as config_file:
            config_file.write(changed_config)
        os.utime(WATCHED_CONFIG_BUNDLE_CONFIG, None)

        time.sleep(4)

        bundle = webpack(WATCHED_CONFIG_BUNDLE_CONFIG, watch_config=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        asset = assets[0]
        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_ONE__', contents)
        self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_TWO__', contents)

    def test_source_files_can_be_watched_to_rebuild_a_bundle(self):
        self.assertIn("""module.exports = '__DJANGO_WEBPACK_WATCH_SOURCE_ONE__';""", watched_source)
        with open(WATCHED_SOURCE_BUNDLE_ENTRY, 'r') as entry_file:
            self.assertEqual("""module.exports = '__DJANGO_WEBPACK_WATCH_SOURCE_ONE__';""", entry_file.read())

        bundle = webpack(WATCHED_SOURCE_BUNDLE_CONFIG, watch_source=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        asset = assets[0]
        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()
        self.assertIn('__DJANGO_WEBPACK_WATCH_SOURCE_ONE__', contents)
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_SOURCE_TWO__', contents)

        with open(WATCHED_SOURCE_BUNDLE_ENTRY, 'w') as entry_file:
            entry_file.write("""module.exports = '__DJANGO_WEBPACK_WATCH_SOURCE_TWO__';""")
        os.utime(WATCHED_SOURCE_BUNDLE_ENTRY, None)

        bundle = webpack(WATCHED_SOURCE_BUNDLE_CONFIG, watch_source=True)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        asset = assets[0]
        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()
        self.assertNotIn('__DJANGO_WEBPACK_WATCH_SOURCE_ONE__', contents)
        self.assertIn('__DJANGO_WEBPACK_WATCH_SOURCE_TWO__', contents)

    # def test_source_and_config_files_can_be_watched_to_rebuild_a_bundle(self):
    #     self.assertIn('./entry1.js', watched_source_and_config_config)
    #     with open(WATCHED_SOURCE_AND_CONFIG_BUNDLE_CONFIG, 'r') as config_file:
    #         self.assertEqual(watched_source_and_config_config, config_file.read())
    #
    #     bundle = webpack(WATCHED_SOURCE_AND_CONFIG_BUNDLE_CONFIG, watch_config=True, watch_source=True)
    #     assets = bundle.get_assets()
    #     self.assertTrue(len(assets), 1)
    #     asset = assets[0]
    #     with open(asset['path'], 'r') as asset_file:
    #         contents = asset_file.read()
    #     self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_ONE__', contents)
    #     self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_TWO__', contents)
    #
    #     changed_config = watched_source_and_config_config.replace('./entry1.js', './entry2.js')
    #     self.assertNotIn('./entry1.js', changed_config)
    #     with open(WATCHED_SOURCE_AND_CONFIG_BUNDLE_CONFIG, 'w') as config_file:
    #         config_file.write(changed_config)
    #     os.utime(WATCHED_SOURCE_AND_CONFIG_BUNDLE_CONFIG, None)
    #
    #     time.sleep(4)
    #
    #     bundle = webpack(WATCHED_SOURCE_AND_CONFIG_BUNDLE_CONFIG, watch_config=True, watch_source=True)
    #     assets = bundle.get_assets()
    #     self.assertTrue(len(assets), 1)
    #     asset = assets[0]
    #     with open(asset['path'], 'r') as asset_file:
    #         contents = asset_file.read()
    #     self.assertNotIn('__DJANGO_WEBPACK_WATCH_CONFIG_ONE__', contents)
    #     self.assertIn('__DJANGO_WEBPACK_WATCH_CONFIG_TWO__', contents)

    # TODO: test that you can watch both the source and config
    # TODO: test that you can mix watched an non-watched versions of a file