import json
from collections import OrderedDict

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import BaseStorageFinder
from django.contrib.staticfiles.storage import StaticFilesStorage

from .conf import settings
from .compiler import webpack

# XXX: We need to ensure that the configuration is triggered, if we in a
# management command (like collectstatic), it is possible that we don't get
# configured.
from js_host import models  # NOQA
from . import models  # NOQA


class WebpackFileStorage(FileSystemStorage):
    """
    Standard file system storage for files handled by django-webpack.
    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.STATIC_ROOT
        if base_url is None:
            base_url = settings.STATIC_URL
        super(WebpackFileStorage, self).__init__(location, base_url, *args, **kwargs)


class WebpackFinder(BaseStorageFinder):
    """
    A staticfiles finder that looks in webpack.conf.settings.STATIC_ROOT for generated bundles.

    To be used during development with staticfiles' development file server
    or during deployment.
    """
    storage = WebpackFileStorage

    def list(self, *args, **kwargs):
        return []


class WebpackOfflineStorageMixin(object):
    """
    A StaticFilesStorage mixin similar inspired by ManifestFilesMixin. It will
    compile all of the webpack bundles specified by the WEBPACK_OFFLINE_BUNDLES
    setting and then stores them in a manifest file to be read by the webpack
    templatetag.

    Usage:

        # myproject/storage.py
        from django.contrib.staticfiles.storage import StaticFilesStorage

        class MyStaticFilesStorage(WebpackOfflineStorageMixin, StaticFilesStorage):
            pass

        # settings.py
        WEBPACK = {
            # ...
            'COMPILE_OFFLINE': True,
            'OFFLINE_BUNDLES': [
                'path/to/webpack.config.js'
            ]
        }
    """
    webpack_bundle_stats_path = 'webpack-bundles.json'
    webpack_bundle_stats_version = '1.0'

    def load_webpack_bundle_stats(self):
        content = self._read_webpack_bundle_stats()
        if content is None:
            return OrderedDict()
        try:
            stored = json.loads(content, object_pairs_hook=OrderedDict)
        except ValueError:
            pass
        else:
            version = stored.get('version', None)
            if version == self.webpack_bundle_stats_version:
                return stored.get('stats', OrderedDict())
        raise ValueError("Couldn't load webpack bundle stats '%s' (version %s)" %
                         (self.webpack_bundle_stats_path, self.webpack_bundle_stats_version))

    def post_process(self, paths, dry_run=False, **kwargs):
        if dry_run or not settings.COMPILE_OFFLINE:
            return

        bundle_stats = OrderedDict()

        for config_path in settings.OFFLINE_BUNDLES:
            bundle = webpack(config_path)
            bundle_stats[config_path] = bundle.stats

            output_paths = ','.join(
                asset['path'] for asset in bundle.get_assets()
            )
            yield config_path, output_paths, True

        self._save_webpack_bundle_stats(bundle_stats)

        # Call super if it exists.
        sup = super(WebpackOfflineStorageMixin, self)
        if hasattr(sup, 'post_process'):
            processed_files = sup.post_process(paths, dry_run, **kwargs)
            for name, hashed_name, processed in processed_files:
                yield name, hashed_name, processed

    def _read_webpack_bundle_stats(self):
        try:
            with self.open(self.webpack_bundle_stats_path) as bundle_stats:
                return bundle_stats.read().decode('utf-8')
        except IOError:
            return None

    def _save_webpack_bundle_stats(self, bundle_stats):
        payload = {'stats': bundle_stats, 'version': self.webpack_bundle_stats_version}
        if self.exists(self.webpack_bundle_stats_path):
            self.delete(self.webpack_bundle_stats_path)
        contents = json.dumps(payload).encode('utf-8')
        self._save(self.webpack_bundle_stats_path, ContentFile(contents))


class WebpackOfflineStaticFilesStorage(WebpackOfflineStorageMixin, StaticFilesStorage):
    pass
