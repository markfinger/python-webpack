from django.core.management.base import BaseCommand
from optional_django import six
import webpack.conf
from webpack.cache import populate_cache


class Command(BaseCommand):
    help = 'Populate webpack\'s cache'

    def handle(self, *args, **options):
        entries = populate_cache()

        if options['verbosity']:
            self.sep()

            self.stdout.write('Populated cache file {}...'.format(webpack.conf.settings.get_path_to_cache_file()))

            self.div()

            for config_file, entry in six.iteritems(entries):
                self.stdout.write('Config file: {}:'.format(config_file))

                assets = entry['stats']['pathsToAssets'].values()
                if assets:
                    if len(assets) == 1:
                        self.stdout.write('Asset: {}'.format(assets[0]))
                    else:
                        self.stdout.write('Assets...'.format(config_file))
                        for path in assets:
                            self.stdout.write(path)

                self.div()

            self.sep()

    def sep(self):
        self.stdout.write('-' * 80)

    def div(self):
        self.stdout.write('~' * 80)