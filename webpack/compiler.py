import json
import os
import sys
import warnings
from js_host.function import Function
from js_host.exceptions import FunctionError
from optional_django import six
from optional_django import staticfiles
from .exceptions import ImproperlyConfigured, ConfigFileNotFound, BundlingError, WebpackWarning
from .conf import settings
from .cache import cache
from .bundle import WebpackBundle


js_host_function = Function(settings.JS_HOST_FUNCTION)


def webpack(config_file, watch_config=None, watch_source=None, cache_file=None, use_cache_file=None):
    if not settings.STATIC_ROOT:
        raise ImproperlyConfigured('webpack.conf.settings.STATIC_ROOT has not been defined.')

    if not settings.STATIC_URL:
        raise ImproperlyConfigured('webpack.conf.settings.STATIC_URL has not been defined.')

    if cache_file is None:
        cache_file = settings.get_path_to_cache_file()

    if use_cache_file is None:
        use_cache_file = settings.USE_CACHE_FILE

    if use_cache_file:
        entry = cache.get(cache_file, config_file)
        return WebpackBundle(entry['stats'])

    if not os.path.isabs(config_file):
        abs_path = staticfiles.find(config_file)
        if not abs_path:
            raise ConfigFileNotFound(config_file)
        config_file = abs_path

    if not os.path.exists(config_file):
        raise ConfigFileNotFound(config_file)

    if watch_config is None:
        watch_config = settings.WATCH_CONFIG_FILES

    if watch_source is None:
        watch_source = settings.WATCH_SOURCE_FILES

    try:
        output = js_host_function.call(
            config=config_file,
            watch=watch_source,
            watchConfig=watch_config,
            cacheFile=cache_file,
            outputPath=settings.get_path_to_bundle_dir(),
            staticRoot=settings.STATIC_ROOT,
            staticUrl=settings.STATIC_URL,
            aggregateTimeout=settings.AGGREGATE_TIMEOUT,
            poll=settings.POLL,
            # Prevent cache entries from expiring
            cacheTTL=False,
        )
    except FunctionError as e:
        raise six.reraise(BundlingError, BundlingError(*e.args), sys.exc_info()[2])

    stats = json.loads(output)

    if stats['errors']:
        raise BundlingError(
            '{}\n\n{}'.format(config_file, '\n\n'.join(stats['errors']))
        )

    if stats['warnings']:
        warnings.warn(stats['warnings'], WebpackWarning)

    return WebpackBundle(stats)