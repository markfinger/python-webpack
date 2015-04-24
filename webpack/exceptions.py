class ImproperlyConfigured(Exception):
    pass


class ConfigFileNotFound(Exception):
    pass


class BundlingError(Exception):
    pass


class WebpackWarning(Warning):
    pass