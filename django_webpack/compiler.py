import os
from django.utils import six
if six.PY2:
    from urllib import pathname2url
else:
    from urllib.request import pathname2url
from django.utils.safestring import mark_safe
from django.contrib.staticfiles import finders
from .services import WebpackService
from .exceptions import ConfigNotFound
from .settings import BUNDLE_ROOT, BUNDLE_URL, BUNDLE_DIR, WATCH_CONFIG_FILES, WATCH_SOURCE_FILES

service = WebpackService()


class WebpackBundle(object):
    output = None

    def __init__(self, output):
        self.output = output

    def render(self):
        """
        Returns HTML script elements pointing to the bundle's assets
        """
        urls = self.get_urls()
        if urls:
            scripts = ['<script src="{url}"></script>'.format(url=url) for url in urls]
            return mark_safe(''.join(scripts))
        return ''

    def get_urls(self):
        """
        Returns urls to the bundle's assets
        """
        assets = self.get_assets()
        if assets:
            return [asset['url'] for asset in assets]

    def get_assets(self):
        return self.output.get('assets', None)

    def get_config(self):
        return self.output.get('config', None)

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

    output = service.compile(path_to_config, watch_config, watch_source)

    output_path = output['config']['output']['path']

    # Generate contextual information about the generated assets
    output['assets'] = []
    path_to_bundle_dir = os.path.join(BUNDLE_ROOT, BUNDLE_DIR)
    for asset in output['stats']['assets']:
        path = os.path.join(output_path, asset['name'])
        url = None
        if path_to_bundle_dir in path:
            rel_path = path[len(path_to_bundle_dir):]
            rel_url = pathname2url(rel_path)
            if rel_url[0] == '/':
                rel_url = rel_url[1:]
            url = BUNDLE_URL + BUNDLE_DIR + '/' + rel_url
        output['assets'].append({
            'name': asset['name'],
            'path': path,
            'url': url,
        })

    return WebpackBundle(output)