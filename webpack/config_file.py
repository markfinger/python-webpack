import json
import hashlib
import os
from json.encoder import JSONEncoder
from optional_django import six
from .conf import settings


class JS(object):
    def __init__(self, content):
        self.content = content
        self.token = '__js_literal__{}__{}__'.format(
            id(self),
            hashlib.md5(self.content.encode('utf-8')).hexdigest(),
        )


def config_file_encoder_factory():
    js_literals = []

    class ConfigFileEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, JS):
                js_literals.append(o)
                return o.token
            return super(ConfigFileEncoder, self).default(o)

    return js_literals, ConfigFileEncoder


class ConfigFile(object):
    def __init__(self, *args):
        self.content = args
        self.rendered = self.render()

    def render(self):
        js_literals, encoder = config_file_encoder_factory()
        content = ''

        for obj in self.content:
            if isinstance(obj, six.string_types):
                content += obj
            else:
                content += json.dumps(
                    obj,
                    cls=encoder,
                    indent=2,
                    separators=(',', ': '),
                    sort_keys=True
                )

        for js_literal in js_literals:
            content = content.replace('"{}"'.format(js_literal.token), js_literal.content)

        return content

    def generate_path_to_file(self, prefix=None):
        rendered = self.rendered

        if not six.PY2:
            rendered = rendered.encode('utf-8')

        filename = 'webpack.config.{}.js'.format(
            hashlib.md5(rendered).hexdigest()
        )

        if prefix:
            filename = prefix + filename

        return os.path.join(settings.get_path_to_config_files_dir(), filename)

    def write(self, path, force=True):
        if not os.path.exists(path) or force:
            dirname = os.path.dirname(path)

            if not os.path.isdir(dirname):
                os.makedirs(dirname)

            with open(path, 'w') as config_file:
                config_file.write(self.rendered)

        return path