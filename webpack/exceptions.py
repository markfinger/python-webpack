class ImproperlyConfigured(Exception):
    pass


class ConfigFileNotFound(Exception):
    pass


class BundlingError(Exception):
    pass


class WebpackWarning(Warning):
    pass


class BuildServerConnectionError(Exception):
    pass


class BuildServerUnexpectedResponse(Exception):
    pass


class ManifestMissingEntry(Exception):
    pass


class ManifestDoesNotExist(Exception):
    pass