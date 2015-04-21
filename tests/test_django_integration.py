import os
import unittest
from optional_django.env import DJANGO_CONFIGURED
from webpack.compiler import webpack
from optional_django import staticfiles
from .utils import clean_bundle_root, read_file

TEST_ROOT = os.path.dirname(__file__)
BUNDLES = os.path.join(TEST_ROOT, 'bundles',)

PATH_TO_BASIC_CONFIG = os.path.join(BUNDLES, 'basic', 'webpack.config.js')
PATH_TO_LIBRARY_CONFIG = os.path.join(BUNDLES, 'library', 'webpack.config.js')
PATH_TO_MULTIPLE_BUNDLES_CONFIG = os.path.join(BUNDLES, 'multiple_bundles', 'webpack.config.js')
PATH_TO_MULTIPLE_ENTRY_CONFIG = os.path.join(BUNDLES, 'multiple_entry', 'webpack.config.js')


class TestDjangoIntegration(unittest.TestCase):
    # Prevent nose from running these tests
    __test__ = DJANGO_CONFIGURED

    @classmethod
    def setUpClass(cls):
        clean_bundle_root()

    @classmethod
    def tearDownClass(cls):
        clean_bundle_root()

    def test_bundle_can_resolve_files_via_the_django_static_file_finder(self):
        bundle = webpack('django_test_app/webpack.config.js')
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        contents = read_file(assets[0]['path'])
        self.assertIn('__DJANGO_WEBPACK_ENTRY_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_STATIC_FILE_FINDER_TEST__', contents)

    def test_bundle_urls_can_be_resolved_via_the_static_file_finder_used_by_the_dev_server(self):
        bundle = webpack('django_test_app/webpack.config.js')
        assets = bundle.get_assets()
        self.assertTrue(len(assets), 1)
        relative_url = assets[0]['url'].split('/static/')[-1]
        self.assertEqual(staticfiles.find(relative_url), assets[0]['path'])