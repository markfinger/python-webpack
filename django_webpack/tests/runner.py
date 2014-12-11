import sys
from django.conf import settings
import test_settings

settings.configure(**test_settings.settings)

from django.test.runner import DiscoverRunner
test_runner = DiscoverRunner()
failures = test_runner.run_tests(['django_webpack'])
if failures:
    sys.exit(failures)