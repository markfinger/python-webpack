class WebpackBundle(object):
    def __init__(self, data, options=None):
        self.data = data
        self.options = options

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

    def get_output_options(self):
        return self.data['outputOptions']

    def get_library(self):
        return self.get_output_options().get('library', None)