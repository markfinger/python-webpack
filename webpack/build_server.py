import requests
import warnings
from .exceptions import BundlingError, WebpackWarning
from .bundle import WebpackBundle
from .exceptions import BuildServerConnectionError, BuildServerUnexpectedResponse
from .options import generate_compiler_options


class BuildServer(object):
    def __init__(self, url):
        self.url = url

    def is_running(self):
        try:
            res = requests.get(self.url)
        except requests.ConnectionError:
            return False

        return res.status_code == 200 and 'webpack-build' in res.text

    def build(self, config_file, extra_context, setting_overrides):
        options = generate_compiler_options(
            config_file=config_file,
            extra_context=extra_context,
            setting_overrides=setting_overrides,
        )

        try:
            res = requests.post(self.url, json=options)
        except requests.ConnectionError:
            raise BuildServerConnectionError('Tried to send build request to {}'.format(self.url))

        if res.status_code != 200:
            raise BuildServerUnexpectedResponse(
                'Unexpected response from {} - {}: {}'.format(self.url, res.status_code, res.text)
            )

        output = res.json()

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
