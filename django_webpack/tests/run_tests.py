import os
import sys

import django


if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_webpack.tests.test_settings'
    if hasattr(django, 'setup'):  # Only compatible with Django >= 1.7
        django.setup()

    # For Django 1.6, need to import after setting DJANGO_SETTINGS_MODULE.
    from django.conf import settings
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['django_webpack'])
    sys.exit(bool(failures))