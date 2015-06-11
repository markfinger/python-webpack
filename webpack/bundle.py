from optional_django.safestring import mark_safe


class WebpackBundle(object):
    stats = None

    def __init__(self, data, options):
        self.data = data
        self.options = options

    def __str__(self):
        return mark_safe(self.render())

    def __unicode__(self):
        return mark_safe(unicode(self.render()))

    def render(self):
        css = self.render_css()
        js = self.render_js()
        return '{}{}'.format(css, js)

    def render_css(self):
        urls = []
        for entry in self.get_urls().values():
            urls += entry['css']
        rendered = ['<link rel="stylesheet" href="{}">'.format(url) for url in urls]
        return '\n'.join(rendered)

    def render_js(self):
        urls = []
        for entry in self.get_urls().values():
            urls += entry['js']
        rendered = ['<script src="{}"></script>'.format(url) for url in urls]
        return '\n'.join(rendered)

    def get_assets(self):
        return self.data['assets']

    def get_output(self):
        return self.data['output']

    def get_urls(self):
        return self.data['urls']

    def get_config(self):
        return self.data['webpackConfig']

    def get_library(self):
        config = self.get_config()
        if config and 'output' in config:
            return config['output'].get('library', None)
    get_var = get_library  # Convenience alias