import unittest
from optional_django.env import DJANGO_CONFIGURED
from optional_django import staticfiles
from webpack.compiler import webpack
from webpack.exceptions import ConfigFileNotFound
from .settings import ConfigFiles
from .utils import clean_static_root


def render_template_tag(path):
    from django.template import Template, Context
    template = Template("""
        {% load webpack %}
        {% webpack path as bundle %}
        {{ bundle.render_js|safe }}
    """)
    return template.render(Context({
        'path': path,
    }))


class TestDjangoIntegration(unittest.TestCase):
    # Prevent nose from running these tests
    __test__ = DJANGO_CONFIGURED

    @classmethod
    def setUpClass(cls):
        clean_static_root()

    @classmethod
    def tearDownClass(cls):
        clean_static_root()

    def test_bundle_urls_can_be_resolved_via_the_static_file_finder_used_by_the_dev_server(self):
        bundle = webpack('django_test_app/webpack.config.js')
        urls = bundle.get_urls()
        self.assertTrue(len(urls['main']['js']), 1)
        relative_url = urls['main']['js'][0].split('/static/')[-1]
        self.assertEqual(staticfiles.find(relative_url), bundle.get_assets()[0])

    def test_template_tag_can_render_a_basic_bundle(self):
        rendered = render_template_tag('django_test_app/webpack.config.js')
        self.assertIn('bundle.js', rendered)

    def test_template_tag_can_render_multiple_assets(self):
        rendered = render_template_tag(ConfigFiles.MULTIPLE_BUNDLES_CONFIG)
        self.assertIn('bundle_1.js', rendered)
        self.assertIn('bundle_2.js', rendered)

    def test_template_tag_raises_on_errors(self):
        self.assertRaises(
            ConfigFileNotFound,
            render_template_tag,
            '/non_existent_path',
        )