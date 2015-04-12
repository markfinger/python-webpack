import os
from django.utils import six
if six.PY2:
    from urllib import pathname2url
else:
    from urllib.request import pathname2url
from django.utils.safestring import mark_safe
from django.contrib.staticfiles import finders
from optional_django import six
from .services import WebpackService
from .exceptions import ConfigNotFound
from .settings import BUNDLE_ROOT, BUNDLE_URL, BUNDLE_DIR, WATCH_CONFIG_FILES, WATCH_SOURCE_FILES

service = WebpackService()


class WebpackBundle(object):
    stats = None

    def __init__(self, stats):
        self.stats = stats

    def render(self):
        """
        Returns HTML script elements pointing to the bundle's assets
        """
        urls = self.get_urls()
        if urls:
            scripts = ['<script src="{url}"></script>'.format(url=url) for url in urls]
            return mark_safe(''.join(scripts))
        return ''

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
        return [asset['paths'] for asset in self.get_assets() if asset['paths']]

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


def webpack(path_to_config, watch_config=None, watch_source=None):
    if not os.path.isabs(path_to_config):
        absolute_path_to_config = finders.find(path_to_config)
        if not absolute_path_to_config:
            raise ConfigNotFound(path_to_config)
        path_to_config = absolute_path_to_config

    if not os.path.exists(path_to_config):
        raise ConfigNotFound(path_to_config)

    if watch_config is None:
        watch_config = WATCH_CONFIG_FILES

    if watch_source is None:
        watch_source = WATCH_SOURCE_FILES

    stats = service.compile(path_to_config, watch_config, watch_source)

    stats['urlsToAssets'] = {}

    # Generate contextual information about the generated assets
    path_to_bundle_dir = os.path.join(BUNDLE_ROOT, BUNDLE_DIR)
    for asset, path in six.iteritems(stats['pathsToAssets']):
        if path_to_bundle_dir in path:
            rel_path = path[len(path_to_bundle_dir):]
            rel_url = pathname2url(rel_path)
            if rel_url[0] == '/':
                rel_url = rel_url[1:]
            url = BUNDLE_URL + BUNDLE_DIR + '/' + rel_url
            stats['urlsToAssets'][asset] = url

    return WebpackBundle(stats)