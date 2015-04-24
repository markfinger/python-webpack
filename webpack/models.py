# Django hook to validate the settings on startup

from optional_django.env import DJANGO_CONFIGURED

if DJANGO_CONFIGURED:
    from .django_integration import validate_settings
    validate_settings()