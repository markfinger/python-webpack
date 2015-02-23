import os
import unittest
import shutil
from django.conf import settings
from django_webpack import bundle, WebpackBundle
from django_webpack.settings import BUNDLE_ROOT
from django_webpack.exceptions import ConfigNotFound

PATH_TO_WEBPACK_CONFIG = os.path.join(os.path.dirname(__file__), 'webpack.config.js')


class TestDjangoWebpack(unittest.TestCase):
    def tearDown(self):
        # Reset the STATIC_ROOT between tests
        if os.path.exists(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)

    def test_bundle_raises_entryfilenotfind_for_nonexistent_config_files(self):
        self.assertRaises(ConfigNotFound, bundle, '/file/that/does/not/exist.js')

    def test_bundle_create_a_file_with_contents(self):
        assets = bundle(PATH_TO_WEBPACK_CONFIG)
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
        webpack_bundle = WebpackBundle(PATH_TO_WEBPACK_CONFIG)
        self.assertEqual(webpack_bundle.get_assets(), bundle(PATH_TO_WEBPACK_CONFIG))

    def test_webpackbundles_can_return_urls_to_assets(self):
        webpack_bundle = WebpackBundle(PATH_TO_WEBPACK_CONFIG)
        asset = webpack_bundle.get_assets()[0]
        urls = webpack_bundle.get_urls()
        self.assertTrue(len(urls), 1)
        url = urls[0]
        self.assertEqual(url, '/static/bundles/' + asset['name'])

    def test_can_render_a_webpack_bundle(self):
        webpack_bundle = WebpackBundle(PATH_TO_WEBPACK_CONFIG)
        url = webpack_bundle.get_urls()[0]
        rendered = webpack_bundle.render()
        self.assertIn(url, webpack_bundle.render())
        self.assertEqual(rendered, '<script src="' + url + '"></script>')

    # TODO: test multi-part bundles