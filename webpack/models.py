from optional_django.env import DJANGO_CONFIGURED
from .django_integration import validate_settings

if DJANGO_CONFIGURED:
    validate_settings()