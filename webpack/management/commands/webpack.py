from django.core.management.base import BaseCommand
from ...manifest import populate_manifest_file
from ...conf import settings


class Command(BaseCommand):
    help = 'Populates webpack\'s manifest file'

    def handle(self, *args, **options):
        populate_manifest_file()
        print('Manifest written to: {}'.format(settings.MANIFEST_PATH))
