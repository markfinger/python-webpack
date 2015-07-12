import warnings
from . import conf
from .exceptions import BundlingError, WebpackWarning
from .bundle import WebpackBundle
from .build_server import BuildServer
from .options import generate_compiler_options
from .manifest import ManifestReader

manifest_reader = ManifestReader()
build_server = BuildServer(conf.settings.BUILD_URL)


def webpack(config_file, context=None, settings=None, manifest=manifest_reader, compiler=build_server):
    use_manifest = conf.settings.USE_MANIFEST

    # Allow the USE_MANIFEST setting to be overridden when populating the manifest
    if settings:
        use_manifest = settings.get('USE_MANIFEST', use_manifest)

    if use_manifest:
        data = manifest.read(config_file, context)
        return WebpackBundle(data)

    options = generate_compiler_options(
        config_file=config_file,
        extra_context=context,
        setting_overrides=settings,
    )

    output = compiler.build(options)

    error = output['error']
    data = output['data']
    stats = data and data.get('stats', None)

    if stats:
        for warning in stats['warnings']:
            warnings.warn(warning, WebpackWarning)

    if error:
        # webpack-build spits up the first error that it sees, but sometimes the most
        # informative errors are in the `stats.errors` object
        if stats and stats['errors']:
            error_objects = stats['errors']
        else:
            error_objects = [error]

        errors = []
        for err in error_objects:
            if isinstance(err, dict):
                message = err.get('message', None)
                stack = err.get('stack', None)
                if message and stack:
                    errors.append('Message: {}\n\nStack trace: {}'.format(message, stack))
                elif stack:
                    errors.append(stack)
                else:
                    errors.append(message)
            else:
                errors.append(err)

        message = 'Tried to build {}'.format(options['config'])
        if errors:
            message += '\n\n' + '\n\n'.join(errors)

        raise BundlingError(message)

    return WebpackBundle(data, options)