python-webpack
==============

[![Build Status](https://travis-ci.org/markfinger/python-webpack.svg?branch=master)](https://travis-ci.org/markfinger/python-webpack)

Python bindings to [webpack](https://webpack.github.io). 

Bundles your assets so that they can be reused on the clientside. Watches your files for changes and 
rebuilds the bundle whenever they change.

Just point webpack at your [config files](https://webpack.github.io/docs/configuration.html) and plug
the rendered elements into your front end.

```python
from webpack.compiler import webpack

bundle = webpack('/path/to/webpack.config.js')

# Returns a string containing <script> and <link> elements 
# pointing to the bundle's assets
bundle.render()
```


Documentation
-------------

- [Installation](#installation)
- [Settings](#settings)
- [Settings for Django projects](#settings-for-django-projects)
- [Usage](#usage)
- [Running the tests](#running-the-tests)


Installation
------------

Webpack depends on [js-host](https://github.com/markfinger/python-js-host/) to provide
interoperability with JavaScript. Complete its 
[quick start](https://github.com/markfinger/python-js-host/#quick-start) before continuing.

Install webpack's JS dependencies

```bash
npm install --save webpack webpack-service
```

Add webpack-service to the functions definition of your `host.config.js` file

```javascript
var webpackService = require('webpack-service');

module.exports = {
  functions: {
    // ...
    webpack: webpackService
  }
};
```

And install python-webpack

```bash
pip install webpack
```


Settings
--------

If you are using this library in a Django project, please refer to the 
[settings for Django projects](#settings-for-django-projects) section of the documentation.

Settings can be defined by calling `webpack.conf.settings.configure` with keyword arguments matching 
the setting that you want to define. For example

```python
from webpack.conf import settings

DEBUG = True

settings.configure(
    BUNDLE_ROOT='/path/to/your/projects/static_root',
    BUNDLE_URL='/static/',
    WATCH_CONFIG_FILES=DEBUG,
    WATCH_SOURCE_FILES=DEBUG,
)
```


### BUNDLE_ROOT

An absolute path to the root directory that you use for static assets.

For example, `'/path/to/your/projects/static_root'`.

This setting **must** be defined.

Default: `None`


### BUNDLE_URL

The root url that your static assets are served from.

For example, `'/static/`.

This setting **must** be defined.

Default: `None`


### BUNDLE_DIR

The directory into which bundles are placed in the `BUNDLE_ROOT`.

Default: `'webpack'`


### WATCH_CONFIG_FILES

A boolean flag which indicates that file watchers should be set to watch config files and 
rebuild the resulting bundle whenever it changes. Set this to `True` in development environments.

Bundles are rebuilt in the background. If webpack is still rebuilding when a request comes in, it will 
block until the build has completed.

Default: `False`


### WATCH_SOURCE_FILES

A boolean flag which indicates that file watchers should be set to watch the bundle's
source files and rebuild the bundle whenever it changes. Set this to `True` in development environments.

Bundles are rebuilt in the background. If webpack is still rebuilding when a request comes in, it will 
block until the build has completed.

Default: `False`


### WATCH_DELAY

The number of milliseconds before any changes to your source files will trigger the bundle
to be rebuilt.

Default: `200`


Settings for Django projects
----------------------------

The following configuration should be placed in your settings files to enable webpack to function 
seamlessly in a Django project.

Add `'webpack'` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    # ...
    'webpack',
)
```

Add `'webpack.django_integration.WebpackFinder'` to your `STATICFILES_FINDERS`

```python
STATICFILES_FINDERS = (
    # ...
    'webpack.django_integration.WebpackFinder',
)
```

Configure webpack to respect your project's configuration

```python
WEBPACK = {
    'BUNDLE_ROOT': STATIC_ROOT,
    'BUNDLE_URL': STATIC_URL,
    'WATCH_CONFIG_FILES': DEBUG,
    'WATCH_SOURCE_FILES': DEBUG,
}
```

When used in a Django project, Webpack allows you to specify paths to config files which will be 
resolved with Django's file finders.

For example, `webpack('my_app/webpack.config.js')` could match a file within an app's static directory, 
such as `my_app/static/my_app/webpack.config.js`.


Usage
-----

```python
from webpack.compiler import webpack

bundle = webpack('/path/to/webpack.config.js')

# Returns a string containing <script> and <link> elements pointing 
# to the generated assets
bundle.render()

# An object providing information about the compilation process
bundle.output

# Returns the paths and urls to the generated assets
bundle.get_assets()

# Returns urls pointing to the generated assets
bundle.get_urls()

# Returns a string matching the `library` property of your config file
bundle.get_library()
```

A helper is provided for configuring your bundle's output path: the substring `[bundle_dir]` 
will be replaced with an absolute path generated by joining your `BUNDLE_ROOT` and `BUNDLE_DIR`
settings.

```javascript
module.exports = {
  // ...
  output: {
    path: '[bundle_dir]',
    // ..
  }
};
```


Running the tests
-----------------

```bash
pip install -r requirements.txt
cd tests
npm install
cd ..
python runtests.py
```
