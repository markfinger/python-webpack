import warnings
from optional_django import six
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

    if data:
        for warning in data['stats']['warnings']:
            warnings.warn(warning, WebpackWarning)

    if error:
        message = 'Tried to build {}\n\n'.format(options['config'])

        if stats and stats['errors']:
            error_objects = stats['errors']
        else:
            error_objects = [error]

        errors = []
        for err in error_objects:
            if isinstance(err, six.string_types):
                errors.append(err)
            elif err.get('stack', None):
                errors.append(err['stack'])
            elif err.get('message', None):
                errors.append(err['message'])
            else:
                errors.append(err)

        raise BundlingError('{}{}'.format(message, '\n\n'.join(errors)))

    return WebpackBundle(data, options)