python-webpack
==============

[![Build Status](https://travis-ci.org/markfinger/python-webpack.svg?branch=master)](https://travis-ci.org/markfinger/python-webpack)

Python bindings to [webpack](https://webpack.github.io). Parses modules with dependencies and 
generates static assets representing those modules, enabling you to package your assets so that 
they can be reused on the clientside.

```python
from webpack.compiler import webpack

bundle = webpack('/path/to/webpack.config.js')

# Returns a string containing <script> and <link> elements 
# pointing to the bundle's assets
bundle.render()
```

python-webpack uses [webpack-wrapper](https://github.com/markfinger/webpack-wrapper) to provide support
for multiple concurrent compilers, file caching, and change detection of files.


Documentation
-------------

- [Installation](#installation)
- [Settings](#settings)
- [Usage](#usage)
- [Output paths](#output-paths)
- [Precompiling assets for production](#precompiling-assets-for-production)
- [Django integration](#django-integration)
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
var webpack = require('webpack-wrapper');

module.exports = {
  functions: {
    // ...
    webpack: webpack
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
[Django integration](#django-integration) section of the documentation.

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


### CACHE

An iterable of config file paths which are used to populate a cache file. Using this setting enables
a production instance to precompile and cache webpack's output.

To assist with programatically generating config files, any functions provided in the iterable will
be called. The functions can return a path or a list of paths, which will be added to the list.

Default: `()`


### USE_CACHE_FILE

A flag denoting that the python process should use the config file, rather than communicating with
the js-host. If you request a build of a config file which was not precompiled, exceptions will be 
raised.

Default: `False`


### CACHE_FILE

A path to a file which will be used to store webpack's cache. If the path is relative, it is joined
to js-host's `SOURCE_ROOT` setting (which defaults to your current working directory).

Default: '.webpack_cache.json'

### OUTPUT_DIR

The directory in `STATIC_ROOT` which webpack will output any generated bundles or config files.

Default: `'webpack'`


### BUNDLE_DIR

The directory into which bundles are placed in the `OUTPUT_DIR`.

Default: `'bundles'`


### CONFIG_DIR

The directory into which bundles are placed in the `OUTPUT_DIR`.

Default: `'config_files'`


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


Usage
-----

python-webpack takes paths to [config files](https://webpack.github.io/docs/configuration.html) and passes
them to a compiler. Once the compiler has built the assets, they can be easily injected into your frontend
as rendered &lt;script&gt; and &lt;link&gt; elements.

```python
from webpack.compiler import webpack

bundle = webpack('/path/to/webpack.config.js')

# Returns a string containing <script> and <link> elements pointing 
# to the generated assets
bundle.render()

# Returns the paths and urls to the generated assets
bundle.get_assets()

# Returns absolute paths to the generated assets on your filesystem
bundle.get_paths()

# Returns urls pointing to the generated assets
bundle.get_urls()

# Returns the config object generated by the compiler
bundle.get_config()

# Returns a string matching the `library` property of your config file
bundle.get_library()
```


Output paths
------------

A helper is provided for configuring your bundle's output path, simply leave the setting undefined and 
it will be preprocessed before compilation begins.

The config's `output.path` property is generated by joining your `STATIC_ROOT`, `OUTPUT_DIR` and 
`BUNDLE_DIR` settings.


Development
-----------

During development, file watchers are used to detect changes to your source files. Whenever a change is
detected, the compilers starts rebuilding in the background. If a rebuild is underway, the compiler will 
block the request until the build has completed.


Precompiling assets for production
----------------------------------

You will generally want to precompile your assets for a production environment. To do so, add your 
config files to the `CACHE` setting, for example

```python
import os

webpack.conf.settings.configure(
  # ...
  CACHE=(
    os.path.join(PROJECT_ROOT, 'webpack.config.js'),
  ),
)
```

and then run the following

```python
from webpack.cache import populate_cache

populate_cache()
```

in a django project, you can run

```bash
./manage.py populate_webpack_cache
```

When your `USE_CACHE_FILE` setting is `True`, the python process will read data from the cache file, 
rather than relying on an active connection to the JS compiler.


Django integration
------------------


### Installation and configuration

The following configuration should be placed in to your settings files to enable webpack to function 
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


### Path resolution

When used in a Django project, Webpack allows you to specify relative paths to config files which will be 
resolved with Django's file finders.

For example, `webpack('app/webpack.config.js')` could match a file within an app's static directory, 
such as `/project/app/static/app/webpack.config.js`.


### Template tags

A template tag is provided as a shorthand for rendering a bundle.

```html
{% load webpack %}

{% webpack 'path/to/webpack.config.js' %}
```


### Management commands

A management command is provided for populating the cache.

```bash
./manage.py populate_webpack_cache
```

If `USE_CACHE_FILE` is `True`, ensure that you run this command before restarting a server.


Running the tests
-----------------

```bash
pip install -r requirements.txt
cd tests
npm install
cd ..
python runtests.py
```
