import os
import shutil
from webpack.conf import settings


def write_file(file_name, content):
    with open(file_name, 'w') as _file:
        _file.write(content)


def read_file(file_name):
    with open(file_name, 'r') as _file:
        return _file.read()


def clean_bundle_root():
    # Clean out any files generated from previous test runs
    if os.path.exists(settings.BUNDLE_ROOT):
        shutil.rmtree(settings.BUNDLE_ROOT)