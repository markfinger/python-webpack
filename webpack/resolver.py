import os
from .exceptions import ConfigFileNotFound
from .conf import settings


def find_config_file(config_file):
    if not os.path.isabs(config_file) and settings.CONFIG_DIRS:
        for dir_path in settings.CONFIG_DIRS:
            abs_path = os.path.join(dir_path, config_file)
            if os.path.exists(abs_path):
                return abs_path

        config_dirs = ' tried: {}'.format(
            [os.path.join(dir_path, config_file) for dir_path in settings.CONFIG_DIRS]
        )
        raise ConfigFileNotFound('{}{}'.format(config_file, config_dirs))

    if not os.path.exists(config_file):
        raise ConfigFileNotFound(config_file)

    return config_file