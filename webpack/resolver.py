import os
from optional_django import staticfiles
from .exceptions import ConfigFileNotFound
from .conf import settings


def find_config_file(config_file):
    if not os.path.isabs(config_file):
        if settings.CONFIG_DIRS:
            for dir_path in settings.CONFIG_DIRS:
                abs_path = os.path.join(dir_path, config_file)
                if os.path.exists(abs_path):
                    return abs_path

        abs_path = staticfiles.find(config_file)
        if not abs_path or not os.path.exists(abs_path):
            config_dirs = ''
            if settings.CONFIG_DIRS:
                config_dirs += ' tried: '
                for dir_path in settings.CONFIG_DIRS:
                    config_dirs += os.path.join(dir_path, config_file)
            raise ConfigFileNotFound('{}{}'.format(config_file, config_dirs))

        return abs_path

    if not os.path.exists(config_file):
        raise ConfigFileNotFound(config_file)

    return config_file