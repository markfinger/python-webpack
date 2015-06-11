class ImproperlyConfigured(Exception):
    pass


class ConfigFileNotFound(Exception):
    pass


class BundlingError(Exception):
    pass


class WebpackWarning(Warning):
    pass


class ConfigFileMissingFromCache(Exception):
    pass


class BuildServerConnectionError(Exception):
    pass


class BuildServerUnexpectedResponse(Exception):
    pass