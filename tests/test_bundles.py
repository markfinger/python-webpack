import os
import unittest
from optional_django import six
from webpack.bundle import WebpackBundle
from webpack.compiler import webpack
from webpack.exceptions import ConfigFileNotFound
from webpack.conf import settings
from .settings import BUNDLES, ConfigFiles
from .utils import clean_static_root, read_file


class TestBundles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        clean_static_root()

    @classmethod
    def tearDownClass(cls):
        clean_static_root()

    def test_bundle_raises_config_file_not_found_exception_for_nonexistent_config_files(self):
        self.assertRaises(ConfigFileNotFound, webpack, '/file/that/does/not/exist.js')

    def test_bundle_create_a_file_with_contents(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        assets = bundle.get_assets()
        self.assertEqual(len(assets), 1)
        asset = assets[0]
        paths = bundle.get_paths()
        self.assertEqual(paths[0], asset['path'])
        self.assertTrue(asset['name'].startswith('bundle-'))
        self.assertTrue(asset['name'].endswith('.js'))
        self.assertEqual(
            asset['path'],
            os.path.join(settings.get_path_to_bundle_dir(), asset['name'])
        )
        self.assertTrue(os.path.exists(asset['path']))
        self.assertTrue(os.path.exists(os.path.join(settings.get_path_to_bundle_dir(), asset['name'])))
        self.assertEqual(
            asset['url'],
            (settings.STATIC_URL + settings.OUTPUT_DIR + '/' + settings.BUNDLE_DIR + '/' + asset['name']).replace('\\', '/'),
        )
        contents = read_file(asset['path'])
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_REQUIRE_TEST__', contents)

    def test_webpack_returns_webpack_bundle_instances(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        self.assertIsInstance(bundle, WebpackBundle)

    def test_webpack_bundles_can_return_urls_to_assets(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        asset = bundle.get_assets()[0]
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        self.assertEqual(urls[0], '/static/webpack/bundles/' + asset['name'])

    def test_can_render_a_webpack_bundle(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        rendered = bundle.render()
        self.assertIn(urls[0], rendered)
        self.assertEqual(rendered, '<script src="' + urls[0] + '"></script>')

    def test_bundle_renders_itself_when_coerced_to_strings(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        self.assertEqual(str(bundle), bundle.render())
        if six.PY2:
            self.assertEqual(unicode(bundle), unicode(bundle.render()))

    def test_bundle_can_handle_a_bundle_with_multiple_entries(self):
        bundle = webpack(ConfigFiles.MULTIPLE_ENTRY_CONFIG)
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
        bundle = webpack(ConfigFiles.MULTIPLE_ENTRY_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        rendered = bundle.render()
        self.assertIn(urls[0], rendered)
        self.assertEqual(rendered, '<script src="' + urls[0] + '"></script>')

    def test_can_render_a_bundle_with_multiple_entry_points(self):
        bundle = webpack(ConfigFiles.MULTIPLE_ENTRY_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        rendered = bundle.render()
        self.assertIn(urls[0], rendered)
        self.assertEqual(rendered, '<script src="' + urls[0] + '"></script>')

    def test_bundle_can_handle_multiple_bundles(self):
        bundle = webpack(ConfigFiles.MULTIPLE_BUNDLES_CONFIG)
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
        bundle = webpack(ConfigFiles.MULTIPLE_BUNDLES_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 2)
        rendered = bundle.render()
        for url in urls:
            self.assertIn(url, bundle.render())
        self.assertEqual(rendered, '<script src="' + urls[0] + '"></script><script src="' + urls[1] + '"></script>')

    def test_bundle_can_expose_the_bundling_processes_output(self):
        bundle = webpack(ConfigFiles.LIBRARY_CONFIG)
        stats = bundle.stats
        self.assertIsInstance(stats, dict)
        self.assertIn('webpackConfig', stats)
        self.assertIsInstance(stats['webpackConfig'], dict)
        self.assertIn('pathsToAssets', stats)
        self.assertIsInstance(stats['pathsToAssets'], dict)
        self.assertIn('urlsToAssets', stats)
        self.assertIsInstance(stats['urlsToAssets'], dict)

    def test_bundle_can_expose_its_config(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        config = bundle.get_config()
        self.assertDictContainsSubset(
            {
                'context': os.path.join(BUNDLES, 'basic', 'app'),
                'entry': './entry.js',
            },
            config
        )
        self.assertDictContainsSubset(
            {
                'path': os.path.join(settings.STATIC_ROOT, settings.OUTPUT_DIR, settings.BUNDLE_DIR),
                'filename': 'bundle-[hash].js'
            },
            config['output']
        )

    def test_bundle_can_expose_its_library_config(self):
        bundle = webpack(ConfigFiles.LIBRARY_CONFIG)
        self.assertEqual(bundle.get_library(), 'LIBRARY_TEST')
        self.assertEqual(bundle.get_var(), 'LIBRARY_TEST')
        bundle = webpack(ConfigFiles.MULTIPLE_BUNDLES_CONFIG)
        self.assertIsNone(bundle.get_library())