import unittest
import os
import json
from webpack.manifest import generate_manifest, generate_key, write_manifest, read_manifest
from webpack.compiler import webpack
from .settings import ConfigFiles, STATIC_ROOT
from .utils import clean_static_root


class TestManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        clean_static_root()

    @classmethod
    def tearDownClass(cls):
        clean_static_root()

    def test_a_manifest_can_be_generated(self):
        manifest = generate_manifest({
            ConfigFiles.BASIC_CONFIG: ()
        })
        self.assertIsInstance(manifest, dict)
        self.assertEqual(len(manifest.keys()), 1)

        key = generate_key(ConfigFiles.BASIC_CONFIG)
        self.assertIn(key, manifest)
        entry = manifest[key]

        bundle = webpack(ConfigFiles.BASIC_CONFIG)
        self.assertEqual(entry, bundle.data)

    def test_a_manifest_can_be_generated_from_multiple_config_files(self):
        manifest = generate_manifest({
            ConfigFiles.BASIC_CONFIG: (),
            ConfigFiles.LIBRARY_CONFIG: (),
        })
        self.assertIsInstance(manifest, dict)
        self.assertEqual(len(manifest.keys()), 2)

        key1 = generate_key(ConfigFiles.BASIC_CONFIG)
        self.assertIn(key1, manifest)
        entry1 = manifest[key1]

        bundle1 = webpack(ConfigFiles.BASIC_CONFIG)
        self.assertEqual(entry1, bundle1.data)

        key2 = generate_key(ConfigFiles.LIBRARY_CONFIG)
        self.assertIn(key2, manifest)
        entry2 = manifest[key2]

        bundle2 = webpack(ConfigFiles.LIBRARY_CONFIG)
        self.assertEqual(entry2, bundle2.data)

    def test_a_manifest_can_be_generated_with_multiple_contexts(self):
        manifest = generate_manifest({
            ConfigFiles.BASIC_CONFIG: (
                {'foo': 'bar'},
            ),
            ConfigFiles.LIBRARY_CONFIG: (
                {'foo': 'bar'},
                {'woz': 'woo'},
            ),
        })
        self.assertIsInstance(manifest, dict)
        self.assertEqual(len(manifest.keys()), 3)

        key1 = generate_key(ConfigFiles.BASIC_CONFIG, {'foo': 'bar'})
        self.assertIn(key1, manifest)
        entry1 = manifest[key1]
        bundle1 = webpack(ConfigFiles.BASIC_CONFIG, context={'foo': 'bar'})
        self.assertEqual(entry1, bundle1.data)

        key2 = generate_key(ConfigFiles.LIBRARY_CONFIG, {'foo': 'bar'})
        self.assertIn(key2, manifest)
        entry2 = manifest[key2]
        bundle2 = webpack(ConfigFiles.LIBRARY_CONFIG, context={'foo': 'bar'})
        self.assertEqual(entry2, bundle2.data)

        key3 = generate_key(ConfigFiles.LIBRARY_CONFIG, {'woz': 'woo'})
        self.assertIn(key3, manifest)
        entry3 = manifest[key3]
        bundle3 = webpack(ConfigFiles.LIBRARY_CONFIG, context={'woz': 'woo'})
        self.assertEqual(entry3, bundle3.data)

    def test_a_manifest_can_be_written_to_and_read_from_disk(self):
        manifest = generate_manifest({
            ConfigFiles.BASIC_CONFIG: (
                {'foo': 'bar'},
            ),
            ConfigFiles.LIBRARY_CONFIG: (
                {'foo': 'bar'},
                {'woz': 'woo'},
            ),
        })

        path = os.path.join(STATIC_ROOT, 'foo.json')

        write_manifest(path, manifest)

        # Manual check
        with open(path, 'r') as manifest_file:
            content = manifest_file.read()
        self.assertEqual(json.loads(content), manifest)

        # Convenience check
        self.assertEqual(read_manifest(path), manifest)