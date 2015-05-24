import os
import unittest
import json
from webpack.compiler import webpack
from webpack.conf import settings
from webpack.cache import populate_cache, cache
from webpack.exceptions import ConfigFileMissingFromCache
from .utils import clean_static_root, read_file
from .settings import ConfigFiles, BUNDLES


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

        bundle1 = webpack(ConfigFiles.LIBRARY_CONFIG, cache_file=path_to_cache_file)
        bundle2 = webpack(ConfigFiles.LIBRARY_CONFIG, cache_file=path_to_cache_file)

        self.assertEqual(bundle1.stats, bundle2.stats)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read().decode('utf-8')

        cache1 = json.loads(contents)

        self.assertIsInstance(cache1, dict)

        self.assertIn(ConfigFiles.LIBRARY_CONFIG, cache1)

        self.assertEqual(cache1[ConfigFiles.LIBRARY_CONFIG]['stats'], bundle1.stats)

        bundle3 = webpack(ConfigFiles.BASIC_CONFIG, cache_file=path_to_cache_file)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read().decode('utf-8')

        cache2 = json.loads(contents)

        self.assertNotEqual(cache2, cache1)

        self.assertIsInstance(cache2, dict)

        self.assertIn(ConfigFiles.LIBRARY_CONFIG, cache2)
        self.assertIn(ConfigFiles.BASIC_CONFIG, cache2)

        self.assertEqual(cache2[ConfigFiles.LIBRARY_CONFIG]['stats'], bundle1.stats)
        self.assertEqual(cache2[ConfigFiles.BASIC_CONFIG]['stats'], bundle3.stats)

    def test_the_cache_can_be_populated_from_a_list_of_config_files(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_populate_cache.json')

        entries = populate_cache(
            cache_list=(ConfigFiles.BASIC_CONFIG, ConfigFiles.LIBRARY_CONFIG),
            path_to_cache_file=path_to_cache_file,
        )

        self.assertIn(ConfigFiles.BASIC_CONFIG, entries)
        self.assertIn(ConfigFiles.LIBRARY_CONFIG, entries)

        self.assertIsInstance(entries[ConfigFiles.BASIC_CONFIG], dict)
        self.assertIsInstance(entries[ConfigFiles.LIBRARY_CONFIG], dict)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read().encode('utf-8')

        self.assertEqual(entries, json.loads(contents))

    def test_the_cache_can_be_populated_from_callbacks(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_populate_cache_from_callbacks.json')

        entries = populate_cache(
            cache_list=(
                lambda: ConfigFiles.BASIC_CONFIG,
                lambda: [ConfigFiles.LIBRARY_CONFIG, ConfigFiles.MULTIPLE_BUNDLES_CONFIG],
                ConfigFiles.MULTIPLE_ENTRY_CONFIG
            ),
            path_to_cache_file=path_to_cache_file,
        )

        self.assertIn(ConfigFiles.BASIC_CONFIG, entries)
        self.assertIn(ConfigFiles.LIBRARY_CONFIG, entries)
        self.assertIn(ConfigFiles.MULTIPLE_BUNDLES_CONFIG, entries)
        self.assertIn(ConfigFiles.MULTIPLE_ENTRY_CONFIG, entries)

        self.assertIsInstance(entries[ConfigFiles.BASIC_CONFIG], dict)
        self.assertIsInstance(entries[ConfigFiles.LIBRARY_CONFIG], dict)
        self.assertIsInstance(entries[ConfigFiles.MULTIPLE_BUNDLES_CONFIG], dict)
        self.assertIsInstance(entries[ConfigFiles.MULTIPLE_ENTRY_CONFIG], dict)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read().encode('utf-8')

        self.assertEqual(entries, json.loads(contents))

    def test_the_cache_singleton_can_read_from_cache_files(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_cache_singleton.json')

        entries = populate_cache(
            cache_list=(ConfigFiles.CACHED_CONFIG,),
            path_to_cache_file=path_to_cache_file,
        )

        self.assertIn(ConfigFiles.CACHED_CONFIG, entries)
        self.assertIsInstance(entries[ConfigFiles.CACHED_CONFIG], dict)

        entry = cache.get(path_to_cache_file, ConfigFiles.CACHED_CONFIG)

        self.assertEqual(entry, entries[ConfigFiles.CACHED_CONFIG])

        self.assertIsInstance(entry['fileDependencies'], list)

        self.assertIn(PATH_TO_CACHED_ENTRY, entry['fileDependencies'])
        self.assertIn(PATH_TO_CACHED_REQUIRE_TEST, entry['fileDependencies'])

    def test_the_cache_includes_file_dependencies(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_file_dependencies.json')

        populate_cache(
            cache_list=(ConfigFiles.CACHED_CONFIG,),
            path_to_cache_file=path_to_cache_file,
        )

        entry = cache.get(path_to_cache_file, ConfigFiles.CACHED_CONFIG)

        self.assertIsInstance(entry['fileDependencies'], list)

        self.assertIn(PATH_TO_CACHED_ENTRY, entry['fileDependencies'])
        self.assertIn(PATH_TO_CACHED_REQUIRE_TEST, entry['fileDependencies'])

    def test_the_compiler_can_use_the_cache(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_compiler_uses_the_cache.json')

        populate_cache(
            cache_list=(ConfigFiles.CACHED_CONFIG,),
            path_to_cache_file=path_to_cache_file,
        )

        entry = cache.get(path_to_cache_file, ConfigFiles.CACHED_CONFIG)

        bundle = webpack(ConfigFiles.CACHED_CONFIG, cache_file=path_to_cache_file, use_cache_file=True)

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
            cache_list=(ConfigFiles.CACHED_CONFIG,),
            path_to_cache_file=path_to_cache_file,
        )

        entry = cache.get(path_to_cache_file, ConfigFiles.CACHED_CONFIG)

        bundle = webpack(ConfigFiles.CACHED_CONFIG, cache_file=path_to_cache_file, use_cache_file=True)

        self.assertEqual(bundle.stats, entry['stats'])

        self.assertRaises(
            ConfigFileMissingFromCache,
            webpack,
            PATH_TO_CACHED_REQUIRE_TEST,
            cache_file=path_to_cache_file,
            use_cache_file=True
        )

