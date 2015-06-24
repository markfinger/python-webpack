import json
import os
import hashlib
from optional_django import staticfiles
from . import conf, __version__
from .server import server
from .exceptions import ImproperlyConfigured, ConfigFileNotFound


def generate_compiler_options(config_file, watch=None, extra_context=None, cache=None):
    if not conf.settings.STATIC_ROOT:
        raise ImproperlyConfigured('webpack.conf.settings.STATIC_ROOT has not been defined.')

    if not conf.settings.STATIC_URL:
        raise ImproperlyConfigured('webpack.conf.settings.STATIC_URL has not been defined.')

    if not os.path.isabs(config_file):
        abs_path = staticfiles.find(config_file)
        if not abs_path:
            raise ConfigFileNotFound(config_file)
        config_file = abs_path

    if not os.path.exists(config_file):
        raise ConfigFileNotFound(config_file)

    if watch is None:
        watch = conf.settings.WATCH

    if cache is None:
        cache = conf.settings.CACHE

    context = {}
    if conf.settings.CONTEXT:
        context.update(conf.settings.CONTEXT)
    if extra_context:
        context.update(extra_context)

    options = {
        'config': config_file,
        'watch': watch,
        'cache': cache,
        'cacheDir': conf.settings.get_path_to_cache_dir(),
        'hmr': conf.settings.HMR,
        'hmrRoot': server.url,
        'context': context,
        'outputPath': conf.settings.get_path_to_output_dir(),
        'publicPath': conf.settings.get_public_path(),
        'staticRoot': conf.settings.STATIC_ROOT,
        'staticUrl': conf.settings.STATIC_URL,
        'aggregateTimeout': conf.settings.AGGREGATE_TIMEOUT,
    }

    # As it defaults to `undefined` it's only defined if necessary
    if conf.settings.POLL is not None:
        options['poll'] = conf.settings.POLL

    # Avoid collisions by directing output into unique directories
    hashable_content = '{}__{}'.format(json.dumps(options), __version__)
    options_hash = hashlib.md5(hashable_content).hexdigest()
    options['outputPath'] = os.path.join(options['outputPath'], options_hash)
    options['publicPath'] += '/' + options_hash

    # Used in the test suite
    options['__python_webpack_hash__'] = options_hash

    return options