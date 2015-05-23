import os
import shutil
import unittest
import mock
from optional_django.env import DJANGO_CONFIGURED
from webpack.compiler import webpack
from webpack.exceptions import BundlingError
from optional_django import staticfiles
from .utils import clean_static_root, read_file

TEST_ROOT = os.path.dirname(__file__)
BUNDLES = os.path.join(TEST_ROOT, 'bundles',)

PATH_TO_BASIC_CONFIG = 'basic/webpack.config.js'
PATH_TO_LIBRARY_CONFIG = 'library/webpack.config.js'
PATH_TO_MULTIPLE_BUNDLES_CONFIG = 'multiple_bundles/webpack.config.js'
PATH_TO_MULTIPLE_ENTRY_CONFIG = 'multiple_entry/webpack.config.js'


class WebpackTemplateTagMixin(object):
    template = "{% load webpack %}{% webpack path %}"

    def render_templatetag(self, path):
        from django.template import Template, Context
        return Template(self.template).render(Context({
            'path': path,
        }))


class TestDjangoIntegration(WebpackTemplateTagMixin, unittest.TestCase):
    # Prevent nose from running these tests
    __test__ = DJANGO_CONFIGURED

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

    def test_templatetag_basic(self):
        rendered = self.render_templatetag(PATH_TO_BASIC_CONFIG)
        self.assertIn('710e9657b7951fbc79b6.js', rendered)

    def test_templatetag_multiple(self):
        rendered = self.render_templatetag(PATH_TO_MULTIPLE_BUNDLES_CONFIG)
        self.assertIn('bundle_1.js', rendered)
        self.assertIn('bundle_2.js', rendered)


class TestWebpackOfflineStorageMixin(WebpackTemplateTagMixin, unittest.TestCase):
    __test__ = DJANGO_CONFIGURED

    def setUp(self):
        """
        Patch the settings temporarily so that we can turn on the offline
        compiler.
        """
        from django.conf import settings as django_settings
        from webpack.conf import Conf
        new_conf = Conf()
        new_conf.configure(
            COMPILE_OFFLINE=True,
            OFFLINE_BUNDLES=[
                PATH_TO_BASIC_CONFIG,
                PATH_TO_MULTIPLE_BUNDLES_CONFIG,
            ],
            **django_settings.WEBPACK
        )
        self.patch_di = mock.patch('webpack.django_integration.settings', new=new_conf)
        self.patch_tt = mock.patch('webpack.templatetags.webpack.settings', new=new_conf)
        self.patch_di.start()
        self.patch_tt.start()
        self.cleanup_static_root()

    def tearDown(self):
        """
        Turn off patches.
        """
        self.patch_di.stop()
        self.patch_tt.stop()
        self.cleanup_static_root()

    @classmethod
    def cleanup_static_root(cls):
        from django.conf import settings as django_settings
        if os.path.exists(django_settings.STATIC_ROOT):
            shutil.rmtree(django_settings.STATIC_ROOT)

    @classmethod
    def collectstatic(cls):
        from django.core.management import call_command
        call_command('collectstatic', verbosity=0, interactive=False)

    def test_webpack_is_not_called_during_request(self):
        self.collectstatic()
        with mock.patch('webpack.templatetags.webpack.webpack') as patch:
            rendered = self.render_templatetag(PATH_TO_BASIC_CONFIG)
            self.assertFalse(patch.called)
        self.assertIn('710e9657b7951fbc79b6.js', rendered)

    def test_throws_error_if_we_didnt_run_collectstatic(self):
        with self.assertRaises(BundlingError):
            self.render_templatetag(PATH_TO_BASIC_CONFIG)

    def test_throws_error_if_requested_bundle_wasnt_precompiled(self):
        from django.core.exceptions import ImproperlyConfigured
        self.collectstatic()
        with self.assertRaises(ImproperlyConfigured):
            self.render_templatetag(PATH_TO_LIBRARY_CONFIG)
