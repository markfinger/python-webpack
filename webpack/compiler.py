import warnings
from .exceptions import BundlingError, WebpackWarning
from .bundle import WebpackBundle
from .server import server
from .options import generate_compiler_options


def webpack(config_file, context=None, settings=None):
    options = generate_compiler_options(
        config_file=config_file,
        extra_context=context,
        setting_overrides=settings,
    )

    output = server.build(options)

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