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

    if error:
        if data and data.get('stats', None) and data['stats'].get('errors', None):
            raise BundlingError(
                '{}\n\n{}'.format(options['config'], '\n\n'.join(data['stats']['errors']))
            )
        raise BundlingError(error)

    if data['stats']['warnings']:
        warnings.warn(data['stats']['warnings'], WebpackWarning)

    return WebpackBundle(data, options)