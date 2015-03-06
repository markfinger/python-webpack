import os
import unittest
import shutil
from django.conf import settings
from django_webpack.bundle import bundle, WebpackBundle
from django_webpack.settings import BUNDLE_ROOT
from django_webpack.exceptions import ConfigNotFound

BASIC_BUNDLE_CONFIG = os.path.join(os.path.dirname(__file__), 'basic_bundle', 'webpack.config.js')
LIBRARY_BUNDLE_CONFIG = os.path.join(os.path.dirname(__file__), 'library_bundle', 'webpack.config.js')
MULTIPLE_BUNDLES_CONFIG = os.path.join(os.path.dirname(__file__), 'multiple_bundles', 'webpack.config.js')
MULTIPLE_ENTRY_BUNDLE_CONFIG = os.path.join(os.path.dirname(__file__), 'multiple_entry_bundle', 'webpack.config.js')


class TestDjangoWebpack(unittest.TestCase):
    def tearDown(self):
        # Reset the STATIC_ROOT between tests
        if os.path.exists(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)

    def test_bundle_raises_entryfilenotfind_for_nonexistent_config_files(self):
        self.assertRaises(ConfigNotFound, bundle, '/file/that/does/not/exist.js')

    def test_bundle_create_a_file_with_contents(self):
        output = bundle(BASIC_BUNDLE_CONFIG)
        assets = output['assets']
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

    def test_webpackbundles_without_path_to_config_raise_as_exception(self):
        self.assertRaises(TypeError, WebpackBundle)

    def test_webpackbundles_can_return_bundled_assets(self):
        webpack_bundle = WebpackBundle(BASIC_BUNDLE_CONFIG)
        output = bundle(BASIC_BUNDLE_CONFIG)
        assets = output['assets']
        self.assertEqual(webpack_bundle.get_assets(), assets)

    def test_webpackbundles_can_return_urls_to_assets(self):
        webpack_bundle = WebpackBundle(BASIC_BUNDLE_CONFIG)
        asset = webpack_bundle.get_assets()[0]
        urls = webpack_bundle.get_urls()

        self.assertTrue(len(urls), 1)
        url = urls[0]

        self.assertEqual(url, '/static/bundles/' + asset['name'])

    def test_can_render_a_webpack_bundle(self):
        webpack_bundle = WebpackBundle(BASIC_BUNDLE_CONFIG)

        urls = webpack_bundle.get_urls()
        self.assertTrue(len(urls), 1)
        url = urls[0]

        rendered = webpack_bundle.render()

        self.assertIn(url, rendered)
        self.assertEqual(rendered, '<script src="' + url + '"></script>')

    def test_bundle_can_handle_a_bundle_with_multiple_entries(self):
        output = bundle(MULTIPLE_ENTRY_BUNDLE_CONFIG)

        assets = output['assets']

        self.assertTrue(len(assets), 1)
        asset = assets[0]

        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()

        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_ONE__', contents)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TWO__', contents)

    def test_can_render_a_webpack_bundle_with_multiple_entries(self):
        webpack_bundle = WebpackBundle(MULTIPLE_ENTRY_BUNDLE_CONFIG)

        urls = webpack_bundle.get_urls()
        self.assertTrue(len(urls), 1)
        url = urls[0]

        rendered = webpack_bundle.render()

        self.assertIn(url, rendered)
        self.assertEqual(rendered, '<script src="' + url + '"></script>')

    def test_can_render_a_webpack_bundle_with_multiple_entry_points(self):
        webpack_bundle = WebpackBundle(MULTIPLE_ENTRY_BUNDLE_CONFIG)

        urls = webpack_bundle.get_urls()
        self.assertTrue(len(urls), 1)
        url = urls[0]

        rendered = webpack_bundle.render()

        self.assertIn(url, rendered)
        self.assertEqual(rendered, '<script src="' + url + '"></script>')

    def test_bundle_can_handle_multiple_bundles(self):
        output = bundle(MULTIPLE_BUNDLES_CONFIG)

        assets = output['assets']

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

    def test_webpack_bundle_can_render_multiple_bundles(self):
        webpack_bundle = WebpackBundle(MULTIPLE_BUNDLES_CONFIG)

        urls = webpack_bundle.get_urls()

        self.assertTrue(len(urls), 2)

        rendered = webpack_bundle.render()

        for url in urls:
            self.assertIn(url, webpack_bundle.render())

        self.assertEqual(
            rendered,
            '<script src="' + urls[0] + '"></script><script src="' + urls[1] + '"></script>'
        )

    def test_bundle_can_resolve_files_via_the_django_static_file_finder(self):
        output = bundle('test_app/webpack.config.js')

        assets = output['assets']

        self.assertTrue(len(assets), 1)

        asset = assets[0]

        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()

        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_STATIC_FILE_FINDER_TEST__', contents)

    def test_webpack_bundle_can_expose_the_bundling_process_output(self):
        webpack_bundle = WebpackBundle(LIBRARY_BUNDLE_CONFIG)
        output = webpack_bundle.get_bundle_output()
        self.assertIn('stats', output)
        self.assertIsInstance(output['stats'], dict)
        self.assertIn('config', output)
        self.assertIsInstance(output['config'], dict)

    def test_webpack_bundle_can_expose_its_config(self):
        webpack_bundle = WebpackBundle(BASIC_BUNDLE_CONFIG)
        config = webpack_bundle.get_config()
        self.assertDictContainsSubset({
            'context': os.path.join(os.path.dirname(__file__), 'basic_bundle', 'app'),
            'entry': './entry.js',
        }, config)
        self.assertDictContainsSubset({
            'path': BUNDLE_ROOT,
            'filename': 'bundle-[hash].js'
        }, config['output'])

    def test_webpack_bundle_can_expose_its_library_config(self):
        webpack_bundle = WebpackBundle(LIBRARY_BUNDLE_CONFIG)
        self.assertEqual(webpack_bundle.get_library(), 'LIBRARY_TEST')

        webpack_bundle = WebpackBundle(MULTIPLE_BUNDLES_CONFIG)
        self.assertIsNone(webpack_bundle.get_library())