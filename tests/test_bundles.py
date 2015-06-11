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
        output = bundle.get_output()['main']['js'][0]
        self.assertEqual(asset, output)
        self.assertEqual(
            asset,
            os.path.join(
                settings.get_path_to_bundle_dir(),
                bundle.options['__hash__'],
                'bundle-{}.js'.format(bundle.data['stats']['hash'])
            )
        )
        self.assertTrue(os.path.exists(asset))
        self.assertEqual(
            bundle.get_urls()['main']['js'][0],
            (
                settings.STATIC_URL +
                settings.OUTPUT_DIR +
                '/' +
                settings.BUNDLE_DIR +
                '/' +
                bundle.options['__hash__'] +
                '/' +
                'bundle-{}.js'.format(bundle.data['stats']['hash'])
            ).replace('\\', '/'),
        )
        contents = read_file(asset)
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_REQUIRE_TEST__', contents)

    def test_webpack_returns_webpack_bundle_instances(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        self.assertIsInstance(bundle, WebpackBundle)

    def test_webpack_bundles_can_return_urls_to_assets(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        assets = bundle.get_assets()
        urls = bundle.get_urls()
        self.assertTrue(len(urls['main']['js']), 1)
        self.assertEqual(
            urls['main']['js'][0],
            '/static/webpack/bundles/' + bundle.options['__hash__'] + '/' + os.path.basename(assets[0]),
        )

    def test_can_render_a_webpack_bundle(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls['main']['js']), 1)
        rendered = bundle.render()
        self.assertIn(urls['main']['js'][0], rendered)
        self.assertEqual(rendered, '<script src="' + urls['main']['js'][0] + '"></script>')

    def test_bundle_renders_itself_when_coerced_to_strings(self):
        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        self.assertEqual(str(bundle), bundle.render())
        if six.PY2:
            self.assertEqual(unicode(bundle), unicode(bundle.render()))

    def test_bundle_can_handle_a_bundle_with_multiple_entries(self):
        bundle = webpack(ConfigFiles.MULTIPLE_ENTRY_CONFIG)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0])
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
        self.assertIn(urls['main']['js'][0], rendered)
        self.assertEqual(rendered, '<script src="' + urls['main']['js'][0] + '"></script>')

    def test_can_render_a_bundle_with_multiple_entry_points(self):
        bundle = webpack(ConfigFiles.MULTIPLE_ENTRY_CONFIG)
        urls = bundle.get_urls()
        self.assertTrue(len(urls), 1)
        rendered = bundle.render()
        self.assertIn(urls['main']['js'][0], rendered)
        self.assertEqual(rendered, '<script src="' + urls['main']['js'][0] + '"></script>')

    def test_bundle_can_handle_multiple_bundles(self):
        bundle = webpack(ConfigFiles.MULTIPLE_BUNDLES_CONFIG)
        assets = bundle.get_assets()
        output = bundle.get_output()
        urls = bundle.get_urls()
        self.assertTrue(len(assets), 2)
        self.assertIn('bundle-bundle_1.js', output['bundle_1']['js'][0])
        self.assertIn('bundle-bundle_2.js', output['bundle_2']['js'][0])
        self.assertIn('bundle_1', output)
        self.assertIn('bundle_2', output)
        self.assertIn('bundle_1', urls)
        self.assertIn('bundle_2', urls)
        bundle_1_contents = read_file(output['bundle_1']['js'][0])
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', bundle_1_contents)
        self.assertIn('__DJANGO_WEBPACK_BUNDLE_ONE__', bundle_1_contents)
        self.assertNotIn('__DJANGO_WEBPACK_BUNDLE_TWO__', bundle_1_contents)
        bundle_2_contents = read_file(output['bundle_2']['js'][0])
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', bundle_2_contents)
        self.assertNotIn('__DJANGO_WEBPACK_BUNDLE_ONE__', bundle_2_contents)
        self.assertIn('__DJANGO_WEBPACK_BUNDLE_TWO__', bundle_2_contents)

    def test_bundle_can_render_multiple_entries(self):
        bundle = webpack(ConfigFiles.MULTIPLE_BUNDLES_CONFIG)
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 2)
        urls = bundle.get_urls()
        rendered = bundle.render()
        self.assertIn(
            urls['bundle_1']['js'][0],
            bundle.render()
        )
        self.assertIn(
            urls['bundle_2']['js'][0],
            bundle.render()
        )
        self.assertEqual(
            rendered,
            '<script src="' + urls['bundle_1']['js'][0] + '"></script>\n<script src="' + urls['bundle_2']['js'][0] + '"></script>',
        )

    def test_bundle_can_expose_the_bundling_processes_output(self):
        bundle = webpack(ConfigFiles.LIBRARY_CONFIG)
        data = bundle.data
        self.assertIsInstance(data, dict)
        self.assertIn('stats', data)
        self.assertIsInstance(data['stats'], dict)
        self.assertIn('webpackConfig', data)
        self.assertIsInstance(data['webpackConfig'], dict)
        self.assertIn('assets', data)
        self.assertIsInstance(data['assets'], list)
        self.assertIn('output', data)
        self.assertIsInstance(data['output'], dict)
        self.assertIn('urls', data)
        self.assertIsInstance(data['urls'], dict)

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
                'path': os.path.join(
                    settings.STATIC_ROOT,
                    settings.OUTPUT_DIR,
                    settings.BUNDLE_DIR,
                    bundle.options['__hash__']
                ),
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