from optional_django.safestring import mark_safe
from .conf import settings


class WebpackBundle(object):
    stats = None

    def __init__(self, stats, options):
        self.stats = stats
        self.options = options

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