from webpack.cache import populate_cache
from webpack.conf import settings
from settings import CONFIG_FILE

assert CONFIG_FILE in settings.CACHE

# Build the assets and generate the cache file
populate_cache()

print('Precompiled {}'.format(settings.CACHE))