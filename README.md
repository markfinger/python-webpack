python-webpack
==============

[![Build Status](https://travis-ci.org/markfinger/python-webpack.svg?branch=master)](https://travis-ci.org/markfinger/python-webpack)

Python bindings to [webpack](https://webpack.github.io). 

Bundles your assets so that they can be reused on the client-side. Watches your files for changes and 
rebuilds the bundle whenever they change.

Just point webpack at your [config files](https://webpack.github.io/docs/configuration.html) and plug
the rendered elements into the client-side.

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

```bash
pip install webpack
```

python-webpack depends on [js-host](https://github.com/markfinger/python-js-host/) to provide a 
JavaScript environment that python can interact with. 
[Install](https://github.com/markfinger/python-js-host/#installation) the library and complete the 
[quick start](https://github.com/markfinger/python-js-host/#quick-start).

Install the JavaScript packages [webpack](https://webpack.github.io) and 
[webpack-service](https://github.com/markfinger/webpack-service).

```bash
npm install --save webpack webpack-service
```

In your `host.config.js` file, add `webpackService` as a function named `webpack`. For example

```javascript
var webpackService = require('webpack-service');

module.exports = {
  functions: {
    // ...
    webpack: webpackService
  }
};
```


Settings
--------

If you are using this library in a Django project, please refer to the 
[settings for Django projects](#settings-for-django-projects) section of the documentation.

In normal python systems, settings can be defined by importing `webpack.conf.settings` and calling 
the `configure` method with keyword arguments matching the name of the setting that you want to 
define. For example

```
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

An absolute path to a directory where you static assets are served from.

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
rebuild the resulting bundle whenever it changes. Set this to `True` in development.

Bundles are rebuilt in the background. If webpack is still rebuilding when a request comes in, it will 
block until the build has completed.

Default: `False`


### WATCH_SOURCE_FILES

A boolean flag which indicates that file watchers should be set to watch the bundle's
source files and rebuild the bundle whenever it changes. Set this to `True` in development.

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

Add the following to inform webpack to respect your Django project's configuration

```python
WEBPACK = {
    BUNDLE_ROOT: STATIC_ROOT,
    BUNDLE_URL: STATIC_URL,
    WATCH_CONFIG_FILES: DEBUG,
    WATCH_SOURCE_FILES: DEBUG,
}
```

Note: when you specify a path to a config file, you can provide a relative path to a config file 
and webpack will use django's static file finders to resolve the file's location. For example, 
`webpack('my_app/webpack.config.js')` could match a file within an app's static directory, 
eg: `my_app/static/my_app/webpack.config.js`.


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
