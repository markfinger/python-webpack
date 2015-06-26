import os
from optional_django import staticfiles
from .exceptions import ConfigFileNotFound
from .conf import settings


def find_config_file(config_file):
    if not os.path.isabs(config_file):
        if settings.CONFIG_DIRS:
            for dir_path in settings.CONFIG_DIRS:
                path = os.path.join(dir_path, config_file)
                if os.path.exists(path):
                    return path

        abs_path = staticfiles.find(config_file)
        if not abs_path or not os.path.exists(abs_path):
            raise ConfigFileNotFound(config_file)

        return abs_path

    if not os.path.exists(config_file):
        raise ConfigFileNotFound(config_file)

    return config_file