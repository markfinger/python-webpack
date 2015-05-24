import json
from types import FunctionType
from optional_django import six
from .exceptions import ConfigFileMissingFromCache
import conf


class Cache(object):
    data = {}

    def get(self, path_to_cache_file, key):
        if path_to_cache_file not in self.data:
            with open(path_to_cache_file, 'r') as cache_file:
                contents = cache_file.read().encode('utf-8')
            self.data[path_to_cache_file] = json.loads(contents)

        if key not in self.data[path_to_cache_file]:
            raise ConfigFileMissingFromCache(
                '{} has no entry for {}. Add the file to webpack\'s CACHE setting, then repopulate the cache'.format(
                    path_to_cache_file,
                    key
                )
            )

        return self.data[path_to_cache_file][key]

    def clear(self):
        self.data = {}

cache = Cache()


def populate_cache(cache_list=None, path_to_cache_file=None):
    if cache_list is None:
        cache_list = conf.settings.CACHE

    if path_to_cache_file is None:
        path_to_cache_file = conf.settings.get_path_to_cache_file()

    config_files = []

    for item in cache_list:
        if isinstance(item, FunctionType):
            output = item()
            if isinstance(output, six.string_types):
                config_files.append(output)
            else:
                config_files += list(output)
        else:
            config_files.append(item)

    # Avoiding a circular import
    from .compiler import webpack

    for config_file in config_files:
        webpack(config_file, cache_file=path_to_cache_file, use_cache_file=False)

    with open(path_to_cache_file, 'r') as cache_file:
        contents = cache_file.read().encode('utf-8')

    return json.loads(contents)