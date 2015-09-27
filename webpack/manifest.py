import json
import hashlib
import os
from optional_django import six
from . import conf
from .bundle import WebpackBundle
from .exceptions import ImproperlyConfigured, ManifestMissingEntry, ManifestDoesNotExist


def generate_key(config_file, context=None):
    if not context:
        return config_file

    hashable_context = json.dumps(context).encode('utf-8')
    context_hash = hashlib.md5(hashable_context).hexdigest()
    return '{}__{}'.format(config_file, context_hash)


def _add_entry_to_manifest(manifest, settings, config_file, context=None):
    from .compiler import webpack  # Avoiding a circular import

    key = generate_key(config_file, context)
    bundle = webpack(config_file, context=context, settings=settings)
    manifest[key] = bundle.data


def generate_manifest(entries, settings=None):
    manifest = {}

    if isinstance(entries, dict):
        for config_file, contexts in six.iteritems(entries):
            contexts = contexts or (None,)
            for context in contexts:
                _add_entry_to_manifest(manifest, settings, config_file, context)
    else:
        for config_file in entries:
            _add_entry_to_manifest(manifest, settings, config_file)

    return manifest


def write_manifest(path, manifest):
    content = json.dumps(manifest, indent=4, sort_keys=True)

    with open(path, 'w') as manifest_file:
        manifest_file.write(content)


def read_manifest(path):
    if not os.path.exists(path):
        raise ManifestDoesNotExist('Cannot find webpack manifest file at {}'.format(path))

    with open(path, 'r') as manifest_file:
        content = manifest_file.read()

    return json.loads(content)


def populate_manifest_file():
    if not conf.settings.MANIFEST:
        raise ImproperlyConfigured('webpack\'s MANIFEST setting has not been defined')

    if not conf.settings.MANIFEST_PATH:
        raise ImproperlyConfigured('webpack\'s MANIFEST_PATH setting has not been defined')

    manifest = generate_manifest(
        conf.settings.MANIFEST,
        conf.settings.MANIFEST_SETTINGS,
    )

    write_manifest(conf.settings.MANIFEST_PATH, manifest)


class ManifestReader(object):
    manifest = None

    def read(self, config_file, context):
        if self.manifest is None:
            self.manifest = read_manifest(path=conf.settings.MANIFEST_PATH)

        key = generate_key(config_file, context)

        if key not in self.manifest:
            raise ManifestMissingEntry(
                'Key "{}" missing from manifest file {}"'.format(key, conf.settings.MANIFEST_PATH)
            )

        data = self.manifest[key]

        return WebpackBundle(data)