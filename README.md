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
- [Extras for Django](#extras-for-django)
- [Usage](#usage)
- [Running the tests](#running-the-tests)


Installation
------------

Webpack depends on [js-host](https://github.com/markfinger/python-js-host/) to provide
interoperability with JavaScript. Complete its 
[quick start](https://github.com/markfinger/python-js-host/#quick-start) before continuing.

Install webpack's JS dependencies

```bash
npm install --save webpack webpack-wrapper
```

Add webpack-wrapper to the functions definition of your `host.config.js` file

```javascript
var webpackWrapper = require('webpack-wrapper');

module.exports = {
  functions: {
    // ...
    webpack: webpackWrapper
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
    STATIC_ROOT='/path/to/your/projects/static_root',
    STATIC_URL='/static/',
    WATCH_CONFIG_FILES=DEBUG,
    WATCH_SOURCE_FILES=DEBUG,
)
```


### STATIC_ROOT

An absolute path to the root directory that you use for static assets.

For example, `'/path/to/your/projects/static_root'`.

This setting **must** be defined.

Default: `None`


### STATIC_URL

The root url that your static assets are served from.

For example, `'/static/'`.

This setting **must** be defined.

Default: `None`


### OUTPUT_DIR

The directory in `STATIC_ROOT` which webpack will output any generated bundles or config files.

Default: `'webpack'`


### BUNDLE_DIR

The directory into which bundles are placed in the `OUTPUT_DIR`.

Default: `'bundles'`


### CONFIG_DIR

The directory into which bundles are placed in the `OUTPUT_DIR`.

Default: `'config_files'`


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


### AGGREGATE_TIMEOUT

The delay between the detection of a change in your source files and the start of a watcher's rebuild process.

Default: `200`


### POLL

Indicates if the watcher should poll for changes, rather than relying on the OS for notifications.

Default: `False`


### TAG_TEMPLATES

String templates which are used when rendering compiled assets. `'js'` is used if there is no matching
extension.

Default:
```python
{
    'css': '<link rel="stylesheet" href="{url}">',
    'js': '<script src="{url}"></script>',
}
```


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
    'STATIC_ROOT': STATIC_ROOT,
    'STATIC_URL': STATIC_URL,
    'WATCH_CONFIG_FILES': DEBUG,
    'WATCH_SOURCE_FILES': DEBUG,
}
```

When used in a Django project, Webpack allows you to specify paths to config files which will be 
resolved with Django's file finders.

For example, `webpack('my_app/webpack.config.js')` could match a file within an app's static directory, 
such as `my_app/static/my_app/webpack.config.js`.


Extras for Django
-----------------

python-webpack also provides a template tag and storage backend for compiling
during collectstatic.

You can use the template tag like this:

```html+django
{% load webpack %}

{% webpack 'path/to/webpack.config.js' %}
```

If you wish to pre-compile your webpack bundles during `collecstatic`, you can
use the special storage backend.

```python
# settings.py

WEBPACK = {
    # ...

    # defines whether or not we should compile during collectstatic
    'COMPILE_OFFLINE': True

    # a list of all webpack configs to compile during collectstatic
    'OFFLINE_BUNDLES': [
        'path/to/webpack.config.js',
    ]
}

STATICFILES_STORAGE = 'webpack.django_integration.WebpackOfflineStaticFilesStorage'
```

If `COMPILE_OFFLINE` is set to `True`, the template tag will check the
pre-compiled bundles. Otherwise, it will compile the files during the request.


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

# Returns absolute paths to the generated assets on your filesystem
bundle.get_paths()

# Returns urls pointing to the generated assets
bundle.get_urls()

# Returns a string matching the `library` property of your config file
bundle.get_library()
```

A helper is provided for configuring your bundle's output path, simply leave the setting
undefined and it will be preprocessed before compilation begins. The value applied is
generated by joining your `STATIC_ROOT`, `OUTPUT_DIR` and `BUNDLE_DIR` settings.


Running the tests
-----------------

```bash
pip install -r requirements.txt
cd tests
npm install
cd ..
python runtests.py
```
