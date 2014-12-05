import os
import subprocess
import tempfile
from django_node.environment import ensure_node_version_gte, ensure_npm_version_gte
from django_node.utils import npm_install
from .settings import (
    PATH_TO_NODE, BUNDLER, NODE_VERSION_REQUIRED, NPM_VERSION_REQUIRED, CHECK_DEPENDENCIES,
    CHECK_PACKAGES
)
from .exceptions import BundlingError


# Ensure that the external dependencies are met
if CHECK_DEPENDENCIES:
    ensure_node_version_gte(NODE_VERSION_REQUIRED)
    ensure_npm_version_gte(NPM_VERSION_REQUIRED)

# Ensure that the required packages have been installed
if CHECK_PACKAGES:
    npm_install(os.path.dirname(__file__))


def bundle(entry, library=None):
    with tempfile.NamedTemporaryFile() as output_file:

        cmd_to_run = (
            PATH_TO_NODE,
            BUNDLER,
            '--entry', entry,
            '--output', output_file.name,
        )

        if library:
            cmd_to_run += ('--library', library,)

        # Call the bundler
        popen = subprocess.Popen(cmd_to_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        popen.wait()

        # Ensure that an exception is thrown if the bundler throws an error
        stderr = popen.stderr.read()
        if stderr:
            raise BundlingError(stderr)

        output_file.seek(0)

        return output_file.read()