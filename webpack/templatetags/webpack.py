from __future__ import absolute_import

import logging

from django.template import Library
from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles.storage import staticfiles_storage

from ..conf import settings
from ..compiler import webpack, WebpackBundle
from ..exceptions import BundlingError

register = Library()

logger = logging.getLogger(__name__)


@register.simple_tag(name='webpack')
def do_webpack(path_to_config):
    """
    A template tag that will output a webpack bundle. To be used in combination
    with the OfflineWebpackStorageMixin.

    Usage:

        {% load webpack %}
        {% webpack 'path/to/webpack.config.js' %}
    """
    if settings.COMPILE_OFFLINE:
        if not hasattr(staticfiles_storage, 'load_webpack_bundle_stats'):
            raise ImproperlyConfigured(
                "Your STATICFILES_STORAGE is not a subclass of"
                " OfflineWebpackStorageMixin. Please make sure to use it or"
                " implement the load_webpack_bundle_stats method on your"
                " class."
            )
        elif path_to_config not in settings.OFFLINE_BUNDLES:
            raise ImproperlyConfigured(
                "'{}' was not found in the webpack bundle stats manifest, did"
                " you include it in WEBPACK_OFFLINE_BUNDLES?".format(path_to_config)
            )
        stats = staticfiles_storage.load_webpack_bundle_stats()
        if stats is None:
            raise BundlingError(
                "Could not find the webpack bundle stats manifest, did you"
                " run collectstatic?"
            )
        elif path_to_config not in stats:
            raise BundlingError(
                "Could not find the webpack bundle stats manifest, I'm not"
                " sure what the error was. Please run collectstatic again,"
                " if the problem persists, report a bug."
            )
        # Re-instantiate from the cache.
        bundle = WebpackBundle(stats[path_to_config])
    else:
        bundle = webpack(path_to_config)

    return bundle.render()
