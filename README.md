django-webpack
==============

[![Build Status](https://travis-ci.org/markfinger/django-webpack.svg?branch=master)](https://travis-ci.org/markfinger/django-webpack)

Generate webpack bundles from your
[webpack config files](webpack.github.io/docs/configuration.html).

```python
from django_webpack.compiler import webpack

bundle = webpack('path/to/webpack.config.js')

# Returns a string containing <script> elements pointing to the bundle
bundle.render()
```

Behind the scenes, your config and source files are watched and 
every time a change is detected the bundle will be rebuilt ready 
for the next request. If a request comes in while the bundle is
being rebuilt, webpack will block until the process has completed.


Documentation
-------------

- [Installation](#installation)
- [Usage](#usage)
- [Settings](#settings)
  - [BUNDLE_ROOT](#django_webpackbundle_root)
  - [BUNDLE_URL](#django_webpackbundle_url)
  - [BUNDLE_DIR](#django_webpackbundle_dir)
  - [WATCH_CONFIG_FILES](#django_webpackwatch_config_files)
  - [WATCH_SOURCE_FILES](#django_webpackwatch_source_files)
- [Running the tests](#running-the-tests)


Installation
------------

```bash
pip install django-webpack
```

You will also need to add the following to your settings.

```python
# in settings.py

INSTALLED_APPS = (
    # ...
    'django_node',
    'django_webpack',
)

STATICFILES_FINDERS = (
    # ...
    'django_webpack.staticfiles.WebpackFinder',
)

# Instruct django-node to host the webpack service
DJANGO_NODE = {
    'SERVICES': (
        'django_webpack.services',
    ),
}
```


Usage
-----

```python
from django_webpack.compiler import webpack

bundle = webpack('path/to/webpack.config.js')

# An object providing information about the compilation process
bundle.output

# Returns a list of objects containing names and paths
assets = bundle.get_assets()

# Returns a list of urls pointing to each asset
urls = bundle.get_urls()

# Returns a string containing <script> elements pointing to each asset
html = bundle.render()
```

A helper is provided for [configuring](webpack.github.io/docs/configuration.html) 
your bundle's output path, the substring `[bundle_dir]` 
will be replaced with a path to the static directory where 
django-webpack looks for generated files.

```javascript
module.exports = {
  // ...
  output: {
    path: '[bundle_dir]',
    // ..
  }
};
```

If you provide a relative path to a config file to a 
WebpackBundle, django-webpack will attempt to use django's 
static file finders to resolve the file's location. 
For example, `webpack('my_app/webpack.config.js')` could 
match a file within an app's static directory - 
eg: `my_app/static/my_app/webpack.config.js`.


Settings
--------

To change the settings, define a dictionary named `DJANGO_WEBPACK` in your settings file.

```python
# For example, to turn off the watchers
DJANGO_WEBPACK = {
    'BUNDLE_ROOT': '/path/to/bundle/root',
}
```

### DJANGO_WEBPACK['BUNDLE_ROOT']

An absolute path to the directory which django-webpack will assume files are placed into.

Defaults to `STATIC_ROOT`.

### DJANGO_WEBPACK['BUNDLE_URL']

The url which is prepended to the relative paths of bundles.

Defaults to `STATIC_URL`.

### DJANGO_WEBPACK['BUNDLE_DIR']

The directory into which bundles are placed in the `BUNDLE_ROOT`.

Defaults to `'webpack'`.

### DJANGO_WEBPACK['WATCH_CONFIG_FILES']

A boolean flag which indicates that file watchers should be set to watch config
files and rebuild the resulting bundle whenever it changes.

Defaults to `DEBUG`.

### DJANGO_WEBPACK['WATCH_SOURCE_FILES']

A boolean flag which indicates that file watchers should be set to watch the bundle's
source files and rebuild the bundle whenever it changes.

Defaults to `DEBUG`.


Running the tests
-----------------

```bash
mkvirtualenv django-webpack
pip install -r requirements.txt
python runtests.py

# Note that the tests include functionality relating to file watching,
# the behaviour of which is inconsistent across environments. If you
# wish to suppress the file watching tests, the test runner takes an
# optional argument '--no-watch-tests', for example:
# `python runtests.py --no-watch-tests`
```
