import os
import shutil
import unittest
from django_webpack.models import WebpackBundle
from django_webpack.exceptions import NoEntryFileDefined, EntryFileNotFound
from test_settings import settings


class TestDjangoWebpack(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(settings['STATIC_ROOT']):
            shutil.rmtree(settings['STATIC_ROOT'])

    def test_can_instantiate_a_webpack_bundle(self):
        WebpackBundle()

    def test_bundles_without_entry_raise_as_exception(self):
        self.assertRaises(NoEntryFileDefined, WebpackBundle().get_path_to_entry)

    def test_bundles_with_nonexistent_entry_raise_an_exception(self):
        bundle = WebpackBundle(entry='file/that/does/not/exist.js')
        self.assertRaises(EntryFileNotFound, bundle.get_path_to_entry)

    def test_bundles_create_a_file_with_contents(self):
        path = WebpackBundle(entry='test_bundle.js').get_path()
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_can_render_a_webpack_bundle(self):
        bundle = WebpackBundle(entry='test_bundle.js')
        rendered = bundle.render()
        self.assertEqual(
            bundle.get_url(),
            '/static/test_bundle-70e51300713754ab4a9a.js',
        )
        self.assertIn(
            bundle.get_url(),
            rendered,
        )