import json
import hashlib
from optional_django import six
from .compiler import webpack
from .options import generate_compiler_options


def generate_key(config_file, context=None):
    options = generate_compiler_options(config_file, context)

    abs_path = options['config']
    context_hash = hashlib.md5(json.dumps(context)).hexdigest()

    return '{}__{}'.format(abs_path, context_hash)


def generate_manifest(entries, settings=None):
    manifest = {}

    for config_file, contexts in six.iteritems(entries):
        contexts = contexts or (None,)
        for context in contexts:
            key = generate_key(config_file, context)
            bundle = webpack(config_file, context=context, settings=settings)
            manifest[key] = bundle.data

    return manifest


def write_manifest(path, manifest):
    content = json.dumps(manifest, indent=4, sort_keys=True)

    with open(path, 'w') as manifest_file:
        manifest_file.write(content)


def read_manifest(path):
    with open(path, 'r') as manifest_file:
        content = manifest_file.read()

    return json.loads(content)