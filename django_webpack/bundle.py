import os
from django.utils.safestring import mark_safe
from django.utils import six
if six.PY2:
    from urlparse import urljoin
elif six.PY3:
    from urllib.parse import urljoin
from .services import WebpackService
from .exceptions import ConfigNotFound
from .settings import BUNDLE_ROOT, BUNDLE_URL, CACHE

webpack_service = WebpackService()
cache = {}


def bundle(path_to_config):
    if not os.path.exists(path_to_config):
        raise ConfigNotFound(path_to_config)

    if CACHE and cache.get(path_to_config, None):
        return cache[path_to_config]

    stats = webpack_service.bundle(path_to_config)

    asset_names = [asset['name'] for asset in stats['assets']]

    assets = []

    for asset_name in asset_names:
        assets.append({
            'name': asset_name,
            'path': os.path.join(BUNDLE_ROOT, asset_name)
        })

    if CACHE:
        cache[path_to_config] = assets

    return assets


class WebpackBundle(object):
    path_to_config = None
    assets = None

    def __init__(self, path_to_config):
        self.path_to_config = path_to_config

    def render(self):
        """
        Returns HTML script elements pointing to the assets generated by webpack.
        """
        scripts = []
        for url in self.get_urls():
            scripts.append(
                '<script src="{url}"></script>'.format(url=url)
            )
        return mark_safe(''.join(scripts))

    def get_urls(self):
        """
        Returns a url to the bundle.

        The url is inferred via Django's STATIC_ROOT and STATIC_URL
        """
        urls = []
        for asset in self.get_assets():
            rel_path = asset['path'].split(BUNDLE_ROOT)[-1]
            if rel_path.startswith('/'):
                rel_path = rel_path[1:]
            url = urljoin(BUNDLE_URL, rel_path)
            urls.append(url)
        return urls

    def get_assets(self):
        if self.assets is None:
            self.assets = bundle(self.path_to_config)
        return self.assets