import os
from django.utils.safestring import mark_safe
from django.contrib.staticfiles import finders
from django.utils import six
if six.PY2:
    from urlparse import urljoin
elif six.PY3:
    from urllib.parse import urljoin
from .services import WebpackService
from .exceptions import ConfigNotFound
from .settings import BUNDLE_ROOT, BUNDLE_URL, WATCH_CONFIG_FILES, WATCH_SOURCE_FILES

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
            urls = []
            for asset in self.get_assets():
                rel_path = asset['path'].split(BUNDLE_ROOT)[-1]
                if rel_path.startswith('/'):
                    rel_path = rel_path[1:]
                url = urljoin(BUNDLE_URL, rel_path)
                urls.append(url)
            return urls

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

    # Indicate the bundles generated
    output['assets'] = []
    for asset in output['stats']['assets']:
        output['assets'].append({
            'name': asset['name'],
            'path': os.path.join(output_path, asset['name'])
        })

    return WebpackBundle(output)