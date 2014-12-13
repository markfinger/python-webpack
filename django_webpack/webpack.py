import os
import json
from django_node import npm, node
import settings
import exceptions

# Ensure that the external dependencies are met
node.ensure_version_gte(settings.NODE_VERSION_REQUIRED)
npm.ensure_version_gte(settings.NPM_VERSION_REQUIRED)

# Ensure that the required packages have been installed
npm.install(os.path.dirname(__file__))


def bundle(
    entry, output, library=None, externals=None, loaders=None, paths_to_loaders=None, no_parse=None,
    devtool=None, bail=None,
):
    arguments = (
        settings.PATH_TO_BUNDLER,
        '--entry', entry,
        '--output', output,
    )

    if library:
        arguments += ('--library', library,)

    if externals:
        arguments += ('--externals', json.dumps(externals),)

    if loaders:
        arguments += ('--loaders', json.dumps(loaders),)

    if paths_to_loaders:
        arguments += ('--paths-to-loaders', ':'.join(paths_to_loaders),)

    if no_parse:
        arguments += ('--no-parse', json.dumps(no_parse),)

    if devtool:
        arguments += ('--devtool', devtool,)

    if bail:
        arguments += ('--bail', 'true',)

    # While rendering templates Django will silently ignore some types of exceptions,
    # so we need to intercept them and raise our own class of exception
    try:
        stderr, stdout = node.run(*arguments)
    except (TypeError, AttributeError) as e:
        raise exceptions.BundlingError(e.__class__.__name__, *e.args)

    if stderr:
        raise exceptions.BundlingError(stderr)

    path_to_bundle = stdout.strip()

    return path_to_bundle