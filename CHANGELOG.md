Change log
==========

### 6.0.0 (24/12/2015)

Updated to support webpack-build@1.0.0. Note that webpack-build needs to be invoked with
the `-s` flag to boot the server. For example, `node_modules/.bin/webpack-build -s`.


### 5.0.0 (12/7/2015)

#### ADDITIONS

**API**

- Added the `populate_manifest_file` function

**Settings**

- Added the `HMR` setting, which toggles support for hot module replacement
- Added the `USE_MANIFEST`, `MANIFEST`, `MANIFEST_PATH`, and `MANIFEST_SETTINGS` settings, which provide
  support for offline manifests
- Added the `POLL` setting, which toggles the behaviour of webpack's file watcher in non-OSX environments
- Added the `BUILD_URL` setting, which denotes a url to an endpoint exposing webpack-build
- Added the `CONFIG_DIRS` setting, which enables lookups for relative paths to config files
- Added the `CONTEXT` setting, which denotes the default context sent to config functions
- Added the `CACHE` and `CACHE_DIR` settings, which control webpack-build's persistent file cache

**Dependencies**

- Added a dependency on the webpack-build JS package


#### CHANGES

**API**

- `webpack.compiler.webpack` now accepts the signature `(config_file, [context], [settings], [manifest], [compiler])`

**Settings**

- `OUTPUT_DIR` now defaults to 'webpack_assets'
- `BUNDLE_URL` is now `STATIC_URL`
- `BUNDLE_ROOT` is now `STATIC_ROOT`
- `WATCH_SOURCE_FILES` is now `WATCH`
- `WATCH_DELAY` is now `AGGREGATE_TIMEOUT`


#### REMOVED

**API**

- Removed the undocumented config file writer

**Settings**

- Removed the BUNDLE_DIR and CONFIG_DIR settings
- Removed the WATCH_CONFIG_FILES setting. In practice it proved to introduced memory leaks leading to
  inevitable segmentation faults

**Dependencies**

- Removed the js-host dependency.
- Removed the python-js-host dependency.
- Removed the webpack-wrapper dependency.


### 4.1.1 (11/5/2015)

- Python 3 fixes.

### 4.1.0 (11/5/2015)

- Added a config file writer.
- The directory specified by the BUNDLE_DIR setting is now nested in another directory specified by OUTPUT_DIR.
- Added a setting CONFIG_DIR, which is nested in OUTPUT_DIR.

### 4.0.1 (4/5/2015)

- Fixed an import error when configuring webpack from django.

### 4.0.0 (3/5/2015)

- Renamed the project from django-webpack to python-webpack.
- The django dependency is no longer required, comparable functionality is still preserved if you choose
  to use django.
- The project is now imported as `webpack`, formerly it was `django_webpack`.
- Ported the JS dependency from django-node to js-host.
- The django staticfiles helpers are now located in `webpack.django_integration`.

### 3.1.0 (21/4/2015)

- Bug fixes and improvements to the JS service

### 3.0.1 (1/4/2015)

- The API is now oriented around config files, rather than programmatically generating config. 
- Updated django-node dependency to latest

### 2.1.2 (1/2/2015)

- Updated django-node dependency to latest

### 2.1.1 (1/2/2015)

- Updated django-node dependency to latest

### 2.1.0 (1/2/2015)

- Python 3 fixes

### 2.0.0 (26/12/2014)

- `django_webpack.webpack.bundle` is now available at `django_webpack.bundle`.
- `django_webpack.models.WebpackBundle` is now available at `django_webpack.WebpackBundle`.

### 1.0.1 (14/12/2014)

- Improving the test harness and updating django-node to the latest.

### 1.0.0 (14/12/2014)

- The default value for `WebpackBundle.devtool` is now defined by a setting, DJANGO_WEBPACK['DEVTOOL']
- The default value for the `DJANGO_WEBPACK['CACHE']` setting is now toggled by `DJANGO_WEBPACK['DEBUG']`, rather than `django.conf.settings.DEBUG`.

### 0.2.0 (14/12/2014)

- API changes:
  - `django_webpack.models.WebpackBundle.output` is now `django_webpack.models.WebpackBundle.path_to_output`
  - `django_webpack.models.WebpackBundle.get_output` is now `django_webpack.models.WebpackBundle.get_path_to_output`
- Added an optional in-memory cache, triggered by the setting `DJANGO_REACT['CACHE']`.

### 0.1.0 (13/12/2014)

- django_webpack.models.WebpackBundle can now be invoked directly. `WebpackBundle(entry='path/to/file.js')`

### 0.0.2 (11/12/2014)

- Added a test suite.
- `django_webpack.webpack.bundle` now offers trivial programmatic access to webpack.
- Moved the Webpack configuration settings from settings.py to `django_webpack.models.WebpackBundle`.

### 0.0.1 (7/12/2014)

- Initial release
