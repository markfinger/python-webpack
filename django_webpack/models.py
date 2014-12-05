import os
import hashlib
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe
from .exceptions import SourceFileNotFound
from .settings import STATIC_URL, STATIC_ROOT
from .utils import bundle


class WebpackBundle(object):
    source = None
    path_to_bundled_source = None
    bundle_variable = None

    def render_source(self):
        rendered_source = '<script src="{url_to_bundled_source}"></script>'.format(
            url_to_bundled_source=self.get_url_to_bundled_source()
        )
        return mark_safe(rendered_source)

    def get_source(self):
        return self.source

    def get_path_to_source(self):
        source = self.get_source()
        path_to_source = finders.find(source)
        if not os.path.exists(path_to_source):
            raise SourceFileNotFound(path_to_source)
        return path_to_source

    def generate_bundle_source_hash(self, bundled_source):
        md5 = hashlib.md5()
        md5.update(bundled_source)
        return md5.hexdigest()

    def generate_bundle_source_filename(self, bundled_source):
        # TODO: should use the relative path of self.get_source(), rather than just the filename
        filename_with_extension = os.path.basename(self.get_path_to_source())
        filename, _ = os.path.splitext(filename_with_extension)
        return '{filename}-{hash}.js'.format(
            filename=filename,
            hash=self.generate_bundle_source_hash(bundled_source)
        )

    def generate_path_to_bundled_source(self, bundled_source):
        filename = self.generate_bundle_source_filename(bundled_source)
        rel_path = os.path.join('django_react', 'bundles', filename)
        return os.path.join(STATIC_ROOT, rel_path)

    def write_bundled_source_file(self, bundled_source, path_to_file):
        directory = os.path.dirname(path_to_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(path_to_file, 'w+') as bundled_source_file:
            bundled_source_file.write(bundled_source)
        return path_to_file

    def get_bundle_variable(self):
        if self.bundle_variable:
            return self.bundle_variable

    def generate_bundled_source_file(self):
        bundled_source = bundle(
            entry=self.get_path_to_source(),
            library=self.get_bundle_variable(),
        )
        path_to_bundled_source = self.generate_path_to_bundled_source(bundled_source)
        return self.write_bundled_source_file(bundled_source, path_to_bundled_source)

    def get_path_to_bundled_source(self):
        if not self.path_to_bundled_source:
            self.path_to_bundled_source = self.generate_bundled_source_file()
        return self.path_to_bundled_source

    def get_rel_path_to_bundled_source(self):
        path_to_bundled_source = self.get_path_to_bundled_source()
        _, rel_path = path_to_bundled_source.split(STATIC_ROOT)
        if rel_path.startswith('/') or rel_path.startswith('\\'):
            rel_path = rel_path[1:]
        return rel_path

    def get_url_to_bundled_source(self):
        rel_path_to_bundled_source = self.get_rel_path_to_bundled_source()
        return os.path.join(STATIC_URL, rel_path_to_bundled_source)