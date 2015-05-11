import unittest
import os
from webpack.config_file import ConfigFile, JS
from webpack.conf import settings
from .utils import clean_bundle_root


class TestConfigFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        clean_bundle_root()

    @classmethod
    def tearDownClass(cls):
        clean_bundle_root()

    def test_renders_strings(self):
        config_file = ConfigFile(
            "var foo = 'bar';"
        )
        self.assertEqual(config_file.render(), "var foo = 'bar';")

        config_file = ConfigFile(
            "var foo = 'bar';",
            "var woz = 2;"
        )
        self.assertEqual(config_file.render(), "var foo = 'bar';var woz = 2;")

    def test_renders_objects(self):
        config_file = ConfigFile(
            "var foo = 'bar';",
            'var woz = ', {
                'test': 'test'
            }, ';'
        )
        self.assertEqual(config_file.render(), """var foo = 'bar';var woz = {\n  "test": "test"\n};""")

    def test_renders_during_init(self):
        config_file = ConfigFile(
            "var foo = 'bar';",
            'var woz = ', {
                'test': 'test'
            }, ';'
        )
        rendered = config_file.rendered
        self.assertEqual(rendered, config_file.render())

    def test_renders_js_literals(self):
        config_file = ConfigFile(
            "\nvar path = require('path');\n",
            "module.exports = ", {
                'output': JS("path.join('abs', 'path', 'to', 'dir')"),
                'entry': JS("path.join('.', 'entry.js')"),
                'regex': JS("/foo$/"),
                'foo': {
                    'bar': {
                        'woz': [1, 2, 3]
                    }
                }
            }, ";"
        )
        self.assertEqual(config_file.render(), """
var path = require('path');
module.exports = {
  "entry": path.join('.', 'entry.js'),
  "foo": {
    "bar": {
      "woz": [
        1,
        2,
        3
      ]
    }
  },
  "output": path.join('abs', 'path', 'to', 'dir'),
  "regex": /foo$/
};""")

    def test_can_deterministically_generate_a_path_to_a_file(self):
        config_file = ConfigFile(
            "var foo = 'bar';",
            'var woz = ', {
                'test': 'test'
            }, ';'
        )
        self.assertEqual(
            config_file.generate_path_to_file(),
            os.path.join(settings.get_path_to_config_dir(), 'webpack.config.c6e5a2af68c60ee400e408c5638e1513.js')
        )
        self.assertEqual(
            config_file.generate_path_to_file(prefix='foo.'),
            os.path.join(settings.get_path_to_config_dir(), 'foo.webpack.config.c6e5a2af68c60ee400e408c5638e1513.js')
        )

    def test_can_write_a_file_containing_the_rendered_content(self):
        config_file = ConfigFile(
            "var foo = 'bar';",
            'var woz = ', {
                'test': 'test'
            }, ';'
        )
        path = config_file.generate_path_to_file()
        output = config_file.write(path)
        self.assertEqual(output, path)
        with open(path, 'r') as output_file:
            content = output_file.read()
        self.assertEqual(content, config_file.rendered)

    def test_can_only_write_a_file_if_it_does_not_exist(self):
        config_file = ConfigFile("var foo = 'bar';")
        path = config_file.generate_path_to_file()
        self.assertFalse(os.path.exists(path))

        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with open(path, 'w') as output_file:
            output_file.write('foo')

        output = config_file.write(path)
        self.assertEqual(output, path)

        with open(path, 'r') as output_file:
            content = output_file.read()
        self.assertEqual(content, config_file.rendered)

        with open(path, 'w') as output_file:
            output_file.write('foo')

        output = config_file.write(path, force=False)
        self.assertEqual(output, path)

        with open(path, 'r') as output_file:
            content = output_file.read()
        self.assertEqual(content, 'foo')
