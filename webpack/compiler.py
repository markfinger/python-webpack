from . import conf
from .build_server import BuildServer
from .manifest import ManifestReader

manifest_reader = ManifestReader()
build_server = BuildServer(conf.settings.BUILD_URL)


def webpack(config_file, context=None, settings=None, manifest=manifest_reader, compiler=build_server):
    use_manifest = conf.settings.USE_MANIFEST

    # Allow the USE_MANIFEST setting to be overridden when populating the manifest
    if settings:
        use_manifest = settings.get('USE_MANIFEST', use_manifest)

    if use_manifest:
        return manifest.read(config_file, context)

    return compiler.build(
        config_file=config_file,
        extra_context=context,
        setting_overrides=settings,
    )