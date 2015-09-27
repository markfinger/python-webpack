import json
import os
import hashlib
from . import conf, __version__
from .resolver import find_config_file
from .exceptions import ImproperlyConfigured


def _setting(overrides, key):
    if overrides and key in overrides:
        return overrides[key]
    return getattr(conf.settings, key)


def generate_compiler_options(config_file, extra_context=None, setting_overrides=None):
    if not _setting(setting_overrides, 'STATIC_ROOT'):
        raise ImproperlyConfigured('webpack.conf.settings.STATIC_ROOT has not been defined.')

    if not _setting(setting_overrides, 'STATIC_URL'):
        raise ImproperlyConfigured('webpack.conf.settings.STATIC_URL has not been defined.')

    context = {}
    if conf.settings.CONTEXT:
        context.update(conf.settings.CONTEXT)
    if extra_context:
        context.update(extra_context)

    options = {
        'config': find_config_file(config_file),
        'watch': _setting(setting_overrides, 'WATCH'),
        'cache': _setting(setting_overrides, 'CACHE'),
        'hmr': _setting(setting_overrides, 'HMR'),
        'context': context,
        'outputPath': conf.settings.get_path_to_output_dir(),
        'publicPath': conf.settings.get_public_path(),
        'staticRoot': _setting(setting_overrides, 'STATIC_ROOT'),
        'staticUrl': _setting(setting_overrides, 'STATIC_URL'),
        'aggregateTimeout': _setting(setting_overrides, 'AGGREGATE_TIMEOUT'),
    }

    if conf.settings.CACHE_DIR:
        options['cacheDir'] = _setting(setting_overrides, 'CACHE_DIR')

    # As it defaults to `undefined` it's only defined if necessary
    if conf.settings.POLL is not None:
        options['poll'] = _setting(setting_overrides, 'POLL')

    # Avoid collisions by directing output into unique directories
    hashable_content = '{}__{}'.format(json.dumps(options), __version__)
    hashable_content = hashable_content.encode('utf-8')
    options_hash = hashlib.md5(hashable_content).hexdigest()
    options['outputPath'] = os.path.join(options['outputPath'], options_hash)
    options['publicPath'] += '/' + options_hash

    # Used in the test suite
    options['__python_webpack_hash__'] = options_hash

    return options