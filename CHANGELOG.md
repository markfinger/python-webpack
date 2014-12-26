Changelog
=========

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
