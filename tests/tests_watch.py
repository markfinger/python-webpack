import sys

# Optionally prevent the watch tests from running
if '--no-watch-tests' not in sys.argv:
    from ._tests_watch import *