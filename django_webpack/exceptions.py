class BundleHasNoSourceFile(Exception):
    pass


class SourceFileNotFound(Exception):
    pass


class BundlingError(Exception):
    pass


class LoaderAlreadyDefined(Exception):
    pass