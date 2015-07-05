from django.core.management.base import BaseCommand, CommandError
from ...manifest import generate_manifest, write_manifest
from ...conf import settings


class Command(BaseCommand):
    help = 'Populates webpack\'s manifest file'

    def handle(self, *args, **options):
        if not settings.MANIFEST:
            raise CommandError('webpack\'s MANIFEST setting has not been defined')

        if not settings.MANIFEST_PATH:
            raise CommandError('webpack\'s MANIFEST_PATH setting has not been defined')

        manifest = generate_manifest(settings.MANIFEST, {
            'USE_MANIFEST': False,
            'HMR': False,
        })

        write_manifest(settings.MANIFEST_PATH, manifest)

        print('Manifest written to: {}'.format(settings.MANIFEST_PATH))
