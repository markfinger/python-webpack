import os
import unittest
import json
from webpack.compiler import webpack, generate_compiler_options
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
            contents = cache_file.read()

        cache1 = json.loads(contents)

        self.assertIsInstance(cache1, dict)

        options1 = generate_compiler_options(ConfigFiles.LIBRARY_CONFIG, cache_file=path_to_cache_file)
        cache_key1 = options1['cacheKey']

        self.assertIn(cache_key1, cache1)

        self.assertEqual(cache1[cache_key1]['stats'], bundle1.stats)

        bundle3 = webpack(ConfigFiles.BASIC_CONFIG, cache_file=path_to_cache_file)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read()

        cache2 = json.loads(contents)

        self.assertNotEqual(cache2, cache1)

        self.assertIsInstance(cache2, dict)

        options2 = generate_compiler_options(ConfigFiles.BASIC_CONFIG, cache_file=path_to_cache_file)
        cache_key2 = options2['cacheKey']

        self.assertIn(cache_key1, cache2)
        self.assertIn(cache_key2, cache2)

        self.assertEqual(cache2[cache_key1]['stats'], bundle1.stats)
        self.assertEqual(cache2[cache_key2]['stats'], bundle3.stats)

    def test_the_cache_can_be_populated_from_a_list_of_config_files(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_populate_cache.json')

        entries = populate_cache(
            cache_list=(ConfigFiles.BASIC_CONFIG, ConfigFiles.LIBRARY_CONFIG),
            cache_file=path_to_cache_file,
        )

        options1 = generate_compiler_options(ConfigFiles.BASIC_CONFIG, cache_file=path_to_cache_file)
        options2 = generate_compiler_options(ConfigFiles.LIBRARY_CONFIG, cache_file=path_to_cache_file)

        cache_key1 = options1['cacheKey']
        cache_key2 = options2['cacheKey']

        self.assertIn(cache_key1, entries)
        self.assertIn(cache_key2, entries)

        self.assertIsInstance(entries[cache_key1], dict)
        self.assertIsInstance(entries[cache_key2], dict)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read()

        self.assertEqual(entries, json.loads(contents))

    def test_the_cache_can_be_populated_from_callbacks(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_populate_cache_from_callbacks.json')

        entries = populate_cache(
            cache_list=(
                lambda: ConfigFiles.BASIC_CONFIG,
                lambda: [ConfigFiles.LIBRARY_CONFIG, ConfigFiles.MULTIPLE_BUNDLES_CONFIG],
                ConfigFiles.MULTIPLE_ENTRY_CONFIG
            ),
            cache_file=path_to_cache_file,
        )

        cache_key1 = generate_compiler_options(ConfigFiles.BASIC_CONFIG, cache_file=path_to_cache_file)['cacheKey']
        cache_key2 = generate_compiler_options(ConfigFiles.LIBRARY_CONFIG, cache_file=path_to_cache_file)['cacheKey']
        cache_key3 = generate_compiler_options(ConfigFiles.MULTIPLE_BUNDLES_CONFIG, cache_file=path_to_cache_file)['cacheKey']
        cache_key4 = generate_compiler_options(ConfigFiles.MULTIPLE_ENTRY_CONFIG, cache_file=path_to_cache_file)['cacheKey']

        self.assertEqual(len({cache_key1, cache_key2, cache_key3, cache_key4}), 4)

        self.assertIn(cache_key1, entries)
        self.assertIn(cache_key2, entries)
        self.assertIn(cache_key3, entries)
        self.assertIn(cache_key4, entries)

        self.assertIsInstance(entries[cache_key1], dict)
        self.assertIsInstance(entries[cache_key2], dict)
        self.assertIsInstance(entries[cache_key3], dict)
        self.assertIsInstance(entries[cache_key4], dict)

        with open(path_to_cache_file, 'r') as cache_file:
            contents = cache_file.read()

        self.assertEqual(entries, json.loads(contents))

    def test_the_cache_singleton_can_read_from_cache_files(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_cache_singleton.json')

        entries = populate_cache(
            cache_list=(ConfigFiles.CACHED_CONFIG,),
            cache_file=path_to_cache_file,
        )

        options = generate_compiler_options(ConfigFiles.CACHED_CONFIG, cache_file=path_to_cache_file)
        cache_key = options['cacheKey']

        self.assertIn(cache_key, entries)
        self.assertIsInstance(entries[cache_key], dict)

        entry = cache.get(path_to_cache_file, cache_key)

        self.assertEqual(entry, entries[cache_key])

        self.assertIsInstance(entry['fileDependencies'], list)

        self.assertIn(PATH_TO_CACHED_ENTRY, entry['fileDependencies'])
        self.assertIn(PATH_TO_CACHED_REQUIRE_TEST, entry['fileDependencies'])
        self.assertEqual(ConfigFiles.CACHED_CONFIG, entry['config'])

    def test_the_cache_includes_file_dependencies_and_the_config_file(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_file_dependencies.json')

        populate_cache(
            cache_list=(ConfigFiles.CACHED_CONFIG,),
            cache_file=path_to_cache_file,
        )

        options = generate_compiler_options(ConfigFiles.CACHED_CONFIG, cache_file=path_to_cache_file)

        entry = cache.get(path_to_cache_file, options['cacheKey'])

        self.assertIsInstance(entry['fileDependencies'], list)

        self.assertIn(PATH_TO_CACHED_ENTRY, entry['fileDependencies'])
        self.assertIn(PATH_TO_CACHED_REQUIRE_TEST, entry['fileDependencies'])
        self.assertEqual(entry['config'], ConfigFiles.CACHED_CONFIG)

    def test_the_compiler_can_use_the_cache(self):
        path_to_cache_file = os.path.join(settings.STATIC_ROOT, 'test_compiler_uses_the_cache.json')

        populate_cache(
            cache_list=(ConfigFiles.CACHED_CONFIG,),
            cache_file=path_to_cache_file,
        )

        options = generate_compiler_options(ConfigFiles.CACHED_CONFIG, cache_file=path_to_cache_file)
        cache_key = options['cacheKey']

        entry = cache.get(path_to_cache_file, cache_key)

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
            cache_file=path_to_cache_file,
        )

        options = generate_compiler_options(ConfigFiles.CACHED_CONFIG, cache_file=path_to_cache_file)

        entry = cache.get(path_to_cache_file, options['cacheKey'])

        bundle = webpack(ConfigFiles.CACHED_CONFIG, cache_file=path_to_cache_file, use_cache_file=True)

        self.assertEqual(bundle.stats, entry['stats'])

        self.assertRaises(
            ConfigFileMissingFromCache,
            webpack,
            PATH_TO_CACHED_REQUIRE_TEST,
            cache_file=path_to_cache_file,
            use_cache_file=True
        )

