import warnings
from .exceptions import BundlingError, WebpackWarning
from .bundle import WebpackBundle
from .server import server
from .options import generate_compiler_options


def webpack(config_file, watch=None, env=None, cache=None):
    options = generate_compiler_options(
        config_file=config_file,
        watch=watch,
        env=env,
        cache=cache,
    )

    output = server.build(options)

    error = output['error']
    data = output['data']
    stats = data and data.get('stats', None)

    if error:
        message = 'Tried to build {}\n\n'.format(options['config'])

        if stats and stats['errors']:
            raise BundlingError('{}{}'.format(message, '\n\n'.join(stats['errors'])))

        raise BundlingError('{}{}'.format(message, error))

    for warning in data['stats']['warnings']:
        warnings.warn(warning, WebpackWarning)

    return WebpackBundle(data, options)