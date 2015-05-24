import os
import unittest
import json
from django.core.management import call_command
import mock
from optional_django import six
from optional_django.env import DJANGO_CONFIGURED
from optional_django import staticfiles
from optional_django.env import DJANGO_SETTINGS
from webpack.compiler import webpack
from webpack.exceptions import ConfigFileNotFound, ConfigFileMissingFromCache
from webpack.conf import Conf
from .utils import clean_static_root, read_file


TEST_ROOT = os.path.dirname(__file__)
BUNDLES = os.path.join(TEST_ROOT, 'bundles',)

PATH_TO_BASIC_CONFIG = 'basic/webpack.config.js'
PATH_TO_LIBRARY_CONFIG = 'library/webpack.config.js'
PATH_TO_MULTIPLE_BUNDLES_CONFIG = 'multiple_bundles/webpack.config.js'
PATH_TO_MULTIPLE_ENTRY_CONFIG = 'multiple_entry/webpack.config.js'


def render_template_tag(path):
    from django.template import Template, Context
    return Template("{% load webpack %}{% webpack path %}").render(Context({
        'path': path,
    }))


class TestDjangoIntegration(unittest.TestCase):
    # Prevent nose from running these tests
    __test__ = DJANGO_CONFIGURED
    template = "{% load webpack %}{% webpack path %}"

    @classmethod
    def setUpClass(cls):
        clean_static_root()

    @classmethod
    def tearDownClass(cls):
        clean_static_root()

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

    def test_template_tag_can_render_a_basic_bundle(self):
        rendered = render_template_tag(PATH_TO_BASIC_CONFIG)
        self.assertIn('710e9657b7951fbc79b6.js', rendered)

    def test_template_tag_can_render_multiple_assets(self):
        rendered = render_template_tag(PATH_TO_MULTIPLE_BUNDLES_CONFIG)
        self.assertIn('bundle_1.js', rendered)
        self.assertIn('bundle_2.js', rendered)

    def test_template_tag_raises_on_errors(self):
        self.assertRaises(
            ConfigFileNotFound,
            render_template_tag,
            '/non_existent_path',
        )

    def test_populate_webpack_cache_command(self):
        path_to_cache_file = os.path.join(DJANGO_SETTINGS.STATIC_ROOT, 'test_populate_webpack_cache_command.json')

        self.assertFalse(os.path.exists(path_to_cache_file))

        new_settings = Conf()
        new_settings.configure(
            CACHE=(
                PATH_TO_BASIC_CONFIG,
                PATH_TO_MULTIPLE_BUNDLES_CONFIG,
            ),
            CACHE_FILE=path_to_cache_file,
            USE_CACHE_FILE=True,
            **{k: v for k, v in six.iteritems(DJANGO_SETTINGS.WEBPACK) if k != 'CACHE_FILE'}
        )

        with mock.patch('webpack.conf.settings', new_settings):
            call_command('populate_webpack_cache', verbosity=0)

            with open(path_to_cache_file, 'r') as cache_file:
                contents = cache_file.read()

            entries = json.loads(contents)

            self.assertIn(staticfiles.find(PATH_TO_BASIC_CONFIG), entries)
            self.assertIn(staticfiles.find(PATH_TO_MULTIPLE_BUNDLES_CONFIG), entries)

            self.assertEqual(
                webpack(PATH_TO_BASIC_CONFIG).stats,
                entries[staticfiles.find(PATH_TO_BASIC_CONFIG)]['stats'],
            )

            self.assertEqual(
                webpack(PATH_TO_MULTIPLE_BUNDLES_CONFIG).stats,
                entries[staticfiles.find(PATH_TO_MULTIPLE_BUNDLES_CONFIG)]['stats'],
            )

            self.assertRaises(
                ConfigFileMissingFromCache,
                webpack,
                PATH_TO_LIBRARY_CONFIG,
            )


