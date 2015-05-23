import os
import unittest
import json
from webpack.compiler import webpack
from webpack.conf import settings
from webpack.cache import populate_cache, cache
from webpack.exceptions import ConfigFileMissingFromCache
from .utils import clean_static_root, read_file

TEST_ROOT = os.path.dirname(__file__)
BUNDLES = os.path.join(TEST_ROOT, 'bundles',)

PATH_TO_BASIC_CONFIG = os.path.join(BUNDLES, 'basic', 'webpack.config.js')
PATH_TO_LIBRARY_CONFIG = os.path.join(BUNDLES, 'library', 'webpack.config.js')
PATH_TO_MULTIPLE_BUNDLES_CONFIG = os.path.join(BUNDLES, 'multiple_bundles', 'webpack.config.js')
PATH_TO_MULTIPLE_ENTRY_CONFIG = os.path.join(BUNDLES, 'multiple_entry', 'webpack.config.js')
PATH_TO_CACHED_CONFIG = os.path.join(BUNDLES, 'cached', 'webpack.config.js')

PATH_TO_CACHED_ENTRY = os.path.join(BUNDLES, 'cached', 'app', 'entry.js')
PATH_TO_CACHED_REQUIRE_TEST = os.path.join(BUNDLES, 'cached', 'app', 'require_test.js')


class TestCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        clean_static_root()

    @classmethod
    def tearDownClass(cls):
        clean_static_root()

    def test_compilation_output_can_be_written_to_a_cache_file(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_compilation_output_can_be_cached.json')

        bundle1 = webpack(PATH_TO_LIBRARY_CONFIG, cache_file=path_to_cache_file)
        bundle2 = webpack(PATH_TO_LIBRARY_CONFIG, cache_file=path_to_cache_file)

        self.assertEqual(bundle1.stats, bundle2.stats)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read().decode('utf-8')

        cache1 = json.loads(contents)

        self.assertIsInstance(cache1, dict)

        self.assertIn(PATH_TO_LIBRARY_CONFIG, cache1)

        self.assertEqual(cache1[PATH_TO_LIBRARY_CONFIG]['stats'], bundle1.stats)

        bundle3 = webpack(PATH_TO_BASIC_CONFIG, cache_file=path_to_cache_file)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read().decode('utf-8')

        cache2 = json.loads(contents)

        self.assertNotEqual(cache2, cache1)

        self.assertIsInstance(cache2, dict)

        self.assertIn(PATH_TO_LIBRARY_CONFIG, cache2)
        self.assertIn(PATH_TO_BASIC_CONFIG, cache2)

        self.assertEqual(cache2[PATH_TO_LIBRARY_CONFIG]['stats'], bundle1.stats)
        self.assertEqual(cache2[PATH_TO_BASIC_CONFIG]['stats'], bundle3.stats)

    def test_the_cache_can_be_populated_from_a_list_of_config_files(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_populate_cache.json')

        entries = populate_cache(
            cache_list=(PATH_TO_BASIC_CONFIG, PATH_TO_LIBRARY_CONFIG),
            path_to_cache_file=path_to_cache_file,
        )

        self.assertIn(PATH_TO_BASIC_CONFIG, entries)
        self.assertIn(PATH_TO_LIBRARY_CONFIG, entries)

        self.assertIsInstance(entries[PATH_TO_BASIC_CONFIG], dict)
        self.assertIsInstance(entries[PATH_TO_LIBRARY_CONFIG], dict)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read().encode('utf-8')

        self.assertEqual(entries, json.loads(contents))

    def test_the_cache_can_be_populated_from_callbacks(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_populate_cache_from_callbacks.json')

        entries = populate_cache(
            cache_list=(
                lambda: PATH_TO_BASIC_CONFIG,
                lambda: [PATH_TO_LIBRARY_CONFIG, PATH_TO_MULTIPLE_BUNDLES_CONFIG],
                PATH_TO_MULTIPLE_ENTRY_CONFIG
            ),
            path_to_cache_file=path_to_cache_file,
        )

        self.assertIn(PATH_TO_BASIC_CONFIG, entries)
        self.assertIn(PATH_TO_LIBRARY_CONFIG, entries)
        self.assertIn(PATH_TO_MULTIPLE_BUNDLES_CONFIG, entries)
        self.assertIn(PATH_TO_MULTIPLE_ENTRY_CONFIG, entries)

        self.assertIsInstance(entries[PATH_TO_BASIC_CONFIG], dict)
        self.assertIsInstance(entries[PATH_TO_LIBRARY_CONFIG], dict)
        self.assertIsInstance(entries[PATH_TO_MULTIPLE_BUNDLES_CONFIG], dict)
        self.assertIsInstance(entries[PATH_TO_MULTIPLE_ENTRY_CONFIG], dict)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read().encode('utf-8')

        self.assertEqual(entries, json.loads(contents))

    def test_the_cache_singleton_can_read_from_cache_files(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_cache_singleton.json')

        entries = populate_cache(
            cache_list=(PATH_TO_CACHED_CONFIG,),
            path_to_cache_file=path_to_cache_file,
        )

        self.assertIn(PATH_TO_CACHED_CONFIG, entries)
        self.assertIsInstance(entries[PATH_TO_CACHED_CONFIG], dict)

        entry = cache.get(path_to_cache_file, PATH_TO_CACHED_CONFIG)

        self.assertEqual(entry, entries[PATH_TO_CACHED_CONFIG])

        self.assertIsInstance(entry['fileDependencies'], list)

        self.assertIn(PATH_TO_CACHED_ENTRY, entry['fileDependencies'])
        self.assertIn(PATH_TO_CACHED_REQUIRE_TEST, entry['fileDependencies'])

    def test_the_cache_includes_file_dependencies(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_file_dependencies.json')

        populate_cache(
            cache_list=(PATH_TO_CACHED_CONFIG,),
            path_to_cache_file=path_to_cache_file,
        )

        entry = cache.get(path_to_cache_file, PATH_TO_CACHED_CONFIG)

        self.assertIsInstance(entry['fileDependencies'], list)

        self.assertIn(PATH_TO_CACHED_ENTRY, entry['fileDependencies'])
        self.assertIn(PATH_TO_CACHED_REQUIRE_TEST, entry['fileDependencies'])

    def test_the_compiler_can_use_the_cache(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_compiler_uses_the_cache.json')

        populate_cache(
            cache_list=(PATH_TO_CACHED_CONFIG,),
            path_to_cache_file=path_to_cache_file,
        )

        entry = cache.get(path_to_cache_file, PATH_TO_CACHED_CONFIG)

        bundle = webpack(PATH_TO_CACHED_CONFIG, cache_file=path_to_cache_file, use_cache_file=True)

        self.assertEqual(bundle.stats, entry['stats'])

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
        self.assertIn('__DJANGO_WEBPACK_CACHED_TEST__', contents)
        self.assertIn('__DJANGO_WEBPACK_CACHED_REQUIRE_TEST__', contents)

    def test_an_exception_is_raised_if_a_config_file_is_missing_from_the_cache(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_missing_config_file_raises.json')

        populate_cache(
            cache_list=(PATH_TO_CACHED_CONFIG,),
            path_to_cache_file=path_to_cache_file,
        )

        entry = cache.get(path_to_cache_file, PATH_TO_CACHED_CONFIG)

        bundle = webpack(PATH_TO_CACHED_CONFIG, cache_file=path_to_cache_file, use_cache_file=True)

        self.assertEqual(bundle.stats, entry['stats'])

        self.assertRaises(
            ConfigFileMissingFromCache,
            webpack,
            '/foo/bar',
            cache_file=path_to_cache_file,
            use_cache_file=True
        )

