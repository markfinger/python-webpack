import os
import shutil
import unittest
from django_webpack.models import WebpackBundle
from django_webpack.exceptions import BundleHasNoSourceFile, SourceFileNotFound
from test_settings import settings


class TestDjangoWebpack(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(settings['STATIC_ROOT']):
            shutil.rmtree(settings['STATIC_ROOT'])

    def test_can_instantiate_a_webpack_bundle(self):
        class Bundle(WebpackBundle):
            pass
        Bundle()

    def test_bundles_without_sources_raise_as_exception(self):
        class Bundle(WebpackBundle):
            pass
        self.assertRaises(BundleHasNoSourceFile, Bundle().get_source)

    def test_bundles_with_missing_sources_raise_an_exception(self):
        class Bundle(WebpackBundle):
            source = 'file/that/does/not/exist.js'
        self.assertRaises(SourceFileNotFound, Bundle().get_path_to_source)

    def test_bundles_create_a_file_with_contents(self):
        class Bundle(WebpackBundle):
            source = 'test_bundle.js'
        path = Bundle().get_path_to_bundle()
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_can_render_a_webpack_bundle(self):
        class Bundle(WebpackBundle):
            source = 'test_bundle.js'
        bundle = Bundle()
        rendered = bundle.render_bundle()
        self.assertEqual(
            bundle.get_url_to_bundle(),
            '/static/test_bundle-70e51300713754ab4a9a.js',
        )
        self.assertIn(
            bundle.get_url_to_bundle(),
            rendered,
        )