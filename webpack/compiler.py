import warnings
from .exceptions import BundlingError, WebpackWarning
from .bundle import WebpackBundle
from .server import server
from .options import generate_compiler_options


def webpack(config_file, extra_context=None, setting_overrides=None):
    options = generate_compiler_options(
        config_file=config_file,
        extra_context=extra_context,
        overrides=setting_overrides,
    )

    output = server.build(options)

    error = output['error']
    data = output['data']
    stats = data and data.get('stats', None)

    if stats:
        for warning in stats['warnings']:
            warnings.warn(warning, WebpackWarning)

    if error:
        message = 'Tried to build {}\n\n'.format(options['config'])

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
                    errors.append('{}\n{}'.format(message, stack))
                elif stack:
                    errors.append(stack)
                else:
                    errors.append(message)
            else:
                errors.append(err)

        if errors:
            message = message + '\n\n' + '\n\n'.join(errors)

        raise BundlingError(message)

    return WebpackBundle(data, options)