import os
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe
import exceptions
import settings
import webpack


class WebpackBundle(object):
    source = None
    path_to_output = None
    path_to_bundle = None
    library = None
    externals = None
    loaders = None
    no_parse = None
    paths_to_loaders = None
    devtool = 'eval-source-map' if settings.DEBUG else None
    bail = True

    def render_bundle(self):
        rendered_source = '<script src="{url_to_bundled_source}"></script>'.format(
            url_to_bundled_source=self.get_url_to_bundle()
        )
        return mark_safe(rendered_source)

    def get_source(self):
        if not self.source:
            raise exceptions.BundleHasNoSourceFile(self)
        return self.source

    def get_path_to_source(self):
        source = self.get_source()
        path_to_source = finders.find(source)
        if not path_to_source or not os.path.exists(path_to_source):
            raise exceptions.SourceFileNotFound(path_to_source)
        return path_to_source

    def get_path_to_output(self):
        if self.path_to_output:
            return self.path_to_output
        source, _ = os.path.splitext(self.get_source())
        rel_path = '{source}-[hash].js'.format(
            source=source,
        )
        return os.path.join(settings.STATIC_ROOT, rel_path)

    def get_library(self):
        return self.library

    def get_externals(self):
        return self.externals

    def get_loaders(self):
        return self.loaders

    def get_paths_to_loaders(self):
        return self.paths_to_loaders

    def get_no_parse(self):
        return self.no_parse

    def get_devtool(self):
        return self.devtool

    def get_bail(self):
        return self.bail

    def generate_bundle(self):
        return webpack.bundle(
            entry=self.get_path_to_source(),
            output=self.get_path_to_output(),
            library=self.get_library(),
            externals=self.get_externals(),
            loaders=self.get_loaders(),
            paths_to_loaders=self.get_paths_to_loaders(),
            no_parse=self.get_no_parse(),
            devtool=self.get_devtool(),
            bail=self.get_bail(),
        )

    def get_path_to_bundle(self):
        if not self.path_to_bundle:
            self.path_to_bundle = self.generate_bundle()
        return self.path_to_bundle

    def get_rel_path_to_bundle(self):
        path_to_bundle = self.get_path_to_bundle()
        _, rel_path_to_bundle = path_to_bundle.split(settings.STATIC_ROOT)
        if rel_path_to_bundle.startswith('/') or rel_path_to_bundle.startswith('\\'):
            rel_path_to_bundle = rel_path_to_bundle[1:]
        return rel_path_to_bundle

    def get_url_to_bundle(self):
        rel_path_to_bundle = self.get_rel_path_to_bundle()
        return os.path.join(settings.STATIC_URL, rel_path_to_bundle)