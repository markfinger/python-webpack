import json
import os
import sys
import warnings
from js_host.function import Function
from js_host.exceptions import FunctionError
from optional_django import six
if six.PY2:
    from urllib import pathname2url
else:
    from urllib.request import pathname2url
from optional_django.safestring import mark_safe
from optional_django import staticfiles
from .exceptions import ImproperlyConfigured, ConfigFileNotFound, BundlingError, WebpackWarning
from .conf import settings


class WebpackBundle(object):
    stats = None

    def __init__(self, stats):
        self.stats = stats

    def __str__(self):
        return mark_safe(self.render())

    def __unicode__(self):
        return mark_safe(unicode(self.render()))

    def render(self):
        """
        Returns HTML script elements pointing to the bundle's assets
        """
        urls = self.get_urls()
        if urls:
            return mark_safe(''.join([self.render_tag(url) for url in urls]))
        return ''

    @staticmethod
    def render_tag(url):
        ext = url.split('.')[-1]
        if ext not in settings.TAG_TEMPLATES:
            ext = 'js'
        return settings.TAG_TEMPLATES[ext].format(url=url)

    def get_assets(self):
        if self.stats:
            assets = []
            paths_to_assets = self.stats.get('pathsToAssets', {})
            urls_to_assets = self.stats.get('urlsToAssets', {})
            for asset in self.stats.get('assets', None):
                name = asset['name']
                assets.append({
                    'name': name,
                    'path': paths_to_assets.get(name, None),
                    'url': urls_to_assets.get(name, None),
                })
            return assets

    def get_paths(self):
        """
        Returns paths to the bundle's assets
        """
        return [asset['path'] for asset in self.get_assets() if asset['path']]

    def get_urls(self):
        """
        Returns urls to the bundle's assets
        """
        return [asset['url'] for asset in self.get_assets() if asset['url']]

    def get_config(self):
        if self.stats:
            return self.stats.get('webpackConfig', None)

    def get_library(self):
        config = self.get_config()
        if config and 'output' in config:
            return config['output'].get('library', None)
    get_var = get_library  # Convenience alias


js_host_function = Function(settings.JS_HOST_FUNCTION)


def webpack(config_file, watch_config=None, watch_source=None):
    if not settings.BUNDLE_ROOT:
        raise ImproperlyConfigured('webpack.conf.settings.BUNDLE_ROOT has not been defined.')

    if not settings.BUNDLE_URL:
        raise ImproperlyConfigured('webpack.conf.settings.BUNDLE_URL has not been defined.')

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
            watchDelay=settings.WATCH_DELAY,
            watchConfig=watch_config,
            cache=False,
            fullStats=settings.OUTPUT_FULL_STATS,
            bundleDir=os.path.join(settings.BUNDLE_ROOT, settings.BUNDLE_DIR),
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

    # Generate contextual information about the generated assets
    stats['urlsToAssets'] = {}
    path_to_bundle_dir = os.path.join(settings.BUNDLE_ROOT, settings.BUNDLE_DIR)
    for asset, config_file in six.iteritems(stats['pathsToAssets']):
        if path_to_bundle_dir in config_file:
            rel_path = config_file[len(path_to_bundle_dir):]
            rel_url = pathname2url(rel_path)
            if rel_url.startswith('/'):
                rel_url = rel_url[1:]
            url = '{}{}/{}'.format(settings.BUNDLE_URL, settings.BUNDLE_DIR, rel_url)
            stats['urlsToAssets'][asset] = url

    return WebpackBundle(stats)