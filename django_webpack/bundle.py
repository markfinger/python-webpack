import os
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe
import json
from django_node import npm, node
from .exceptions import NoEntryFileDefined, EntryFileNotFound, BundlingError
from .settings import (
    STATIC_ROOT, DEVTOOL, STATIC_URL, NODE_VERSION_REQUIRED, NPM_VERSION_REQUIRED, PATH_TO_BUNDLER, DEBUG, CACHE,
)

# Ensure that the external dependencies are met
node.ensure_version_gte(NODE_VERSION_REQUIRED)
npm.ensure_version_gte(NPM_VERSION_REQUIRED)

# Ensure that the required packages have been installed
npm.install(os.path.dirname(__file__))


_bundle_cache = {}


def bundle(
    path_to_entry, path_to_output, library=None, externals=None, loaders=None, paths_to_loaders=None, no_parse=None,
    devtool=None, bail=None,
):
    arguments = (
        PATH_TO_BUNDLER,
        '--entry', path_to_entry,
        '--output', path_to_output,
    )

    if library:
        arguments += ('--library', library,)

    if externals:
        arguments += ('--externals', json.dumps(externals),)

    if loaders:
        arguments += ('--loaders', json.dumps(loaders),)

    if paths_to_loaders:
        arguments += ('--paths-to-loaders', ':'.join(paths_to_loaders),)

    if no_parse:
        arguments += ('--no-parse', json.dumps(no_parse),)

    if devtool:
        arguments += ('--devtool', devtool,)

    if bail:
        arguments += ('--bail', 'true',)

    if CACHE and _bundle_cache.get(arguments, None):
        return _bundle_cache[arguments]

    # While rendering templates Django will silently ignore some types of exceptions,
    # so we need to intercept them and raise our own class of exception
    try:
        stderr, stdout = node.run(*arguments, production=DEBUG)
    except (TypeError, AttributeError) as e:
        raise BundlingError(e.__class__.__name__, *e.args)

    if stderr:
        raise BundlingError(stderr)

    # A trailing new line is appended by `console.log`
    path_to_bundle = stdout.strip()

    if CACHE:
        _bundle_cache[arguments] = path_to_bundle

    return path_to_bundle


class WebpackBundle(object):
    entry = None
    path_to_output = None
    library = None
    externals = None
    loaders = None
    paths_to_loaders = None
    no_parse = None
    devtool = DEVTOOL
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

        The url is inferred via Django's STATIC_ROOT and STATIC_URL
        """
        rel_path_to_bundle = self.get_rel_path()
        return os.path.join(STATIC_URL, rel_path_to_bundle)

    def get_path(self):
        """
        Returns an absolute path to the bundle's file on your filesystem.
        """
        if not self.path:
            self.path = bundle(
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
        _, rel_path_to_bundle = path.split(STATIC_ROOT)
        if rel_path_to_bundle.startswith('/') or rel_path_to_bundle.startswith('\\'):
            rel_path_to_bundle = rel_path_to_bundle[1:]
        return rel_path_to_bundle

    def get_entry(self):
        return self.entry

    def get_path_to_entry(self):
        entry = self.get_entry()
        if not entry:
            raise NoEntryFileDefined(self)
        path_to_entry = finders.find(entry)
        if not path_to_entry:
            raise EntryFileNotFound(entry)
        return path_to_entry

    def get_path_to_output(self):
        if not self.path_to_output:
            entry, _ = os.path.splitext(self.get_entry())
            rel_path = '{entry}-[hash].js'.format(
                entry=entry,
            )
            self.path_to_output = os.path.join(STATIC_ROOT, rel_path)
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