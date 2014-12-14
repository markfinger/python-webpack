import os
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe
import exceptions
import settings
import webpack


class WebpackBundle(object):
    entry = None
    path_to_output = None
    library = None
    externals = None
    loaders = None
    paths_to_loaders = None
    no_parse = None
    devtool = 'eval-entry-map' if settings.DEBUG else None
    bail = True
    path = None

    def __init__(
        self, entry=None, path_to_output=None, library=None, externals=None, loaders=None, paths_to_loaders=None, no_parse=None,
        devtool=None, bail=None
    ):
        if entry is not None:
            self.entry = entry
        if path_to_output is not None:
            self.path_to_output = path_to_output
        if library is not None:
            self.library = library
        if externals is not None:
            self.externals = externals
        if loaders is not None:
            self.loaders = loaders
        if paths_to_loaders is not None:
            self.paths_to_loaders = paths_to_loaders
        if no_parse is not None:
            self.no_parse = no_parse
        if devtool is not None:
            self.devtool = devtool
        if bail is not None:
            self.bail = bail

    def render(self):
        """
        Returns a HTML script element with a src attribute pointing to the bundle.
        """
        rendered = '<script src="{url}"></script>'.format(
            url=self.get_url()
        )
        return mark_safe(rendered)

    def get_url(self):
        """
        Returns a url to the bundle.

        The url is inferred via Django's STATIC_ROOT and STATIC_URL settings.
        """
        rel_path_to_bundle = self.get_rel_path()
        return os.path.join(settings.STATIC_URL, rel_path_to_bundle)

    def get_path(self):
        """
        Returns an absolute path to the bundle's file on your filesystem.
        """
        if not self.path:
            self.path = webpack.bundle(
                path_to_entry=self.get_path_to_entry(),
                path_to_output=self.get_path_to_output(),
                library=self.get_library(),
                externals=self.get_externals(),
                loaders=self.get_loaders(),
                paths_to_loaders=self.get_paths_to_loaders(),
                no_parse=self.get_no_parse(),
                devtool=self.get_devtool(),
                bail=self.get_bail(),
            )
        return self.path

    def get_rel_path(self):
        """
        Returns a path to the bundle's file relative to the STATIC_ROOT.
        """
        path = self.get_path()
        _, rel_path_to_bundle = path.split(settings.STATIC_ROOT)
        if rel_path_to_bundle.startswith('/') or rel_path_to_bundle.startswith('\\'):
            rel_path_to_bundle = rel_path_to_bundle[1:]
        return rel_path_to_bundle

    def get_entry(self):
        return self.entry

    def get_path_to_entry(self):
        entry = self.get_entry()
        if not entry:
            raise exceptions.NoEntryFileDefined(self)
        path_to_entry = finders.find(entry)
        if not path_to_entry:
            raise exceptions.EntryFileNotFound(entry)
        return path_to_entry

    def get_path_to_output(self):
        if not self.path_to_output:
            entry, _ = os.path.splitext(self.get_entry())
            rel_path = '{entry}-[hash].js'.format(
                entry=entry,
            )
            self.path_to_output = os.path.join(settings.STATIC_ROOT, rel_path)
        return self.path_to_output

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