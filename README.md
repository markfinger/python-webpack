python-webpack
==============

[![Build Status](https://travis-ci.org/markfinger/python-webpack.svg?branch=master)](https://travis-ci.org/markfinger/python-webpack)

Python bindings to webpack via [webpack-build](https://github.com/markfinger/webpack-build).

Parses modules with dependencies and generates static assets representing those modules, enabling you 
to package your assets so that they can be reused on the client-side.


Documentation
-------------

- [Installation](#installation)
- [Usage](#usage)
- [Django integration](#django-integration)
- [Settings](#settings)
- [Running the tests](#running-the-tests)


Installation
------------

```
pip install python-webpack

npm install webpack webpack-build --save
```


Usage
-----

python-webpack provides a high-level interface to a webpack-build server. To start the server, run
`node_modules/.bin/webpack-build`.

The build server is fed [config files](https://webpack.github.io/docs/configuration.html) and python-webpack
returns an object which allows you to interact with the results of the build.

```python
from webpack.compiler import webpack

bundle = webpack('/path/to/webpack.config.js')

# The raw data returned from webpack-build
bundle.data

# Returns a string containing <link> elements pointing to any css assets
bundle.render_css()

# Returns a string containing <script> elements pointing to any js assets
bundle.render_js()

# Returns absolute paths to the generated assets on your filesystem
bundle.get_assets()

# Returns absolute paths to the generated assets, grouped by entry
bundle.get_output()

# Returns urls to the generated assets, grouped by entry
bundle.get_urls()

# Returns a string matching the `library` property of your config file
bundle.get_library()
```

Be aware that webpack-build deviates slightly from webpack's CLI in that it requires config files
to export a function which accepts options and returns a config object.

To use relative paths to config files, you should specify the `CONFIG_DIRS` setting.

To pass context down to the config function, you can specify it in the `CONTEXT` setting. You can also
provide context by using the `extra_context` argument on the `webpack.compiler.webpack` function.

Be aware that the `output.path` property is overridden on config objects. You can leave the property
undefined and everything will be written within the directory specified by the `STATIC_ROOT` setting.


Django integration
------------------

### Installation and configuration

The following configuration should be placed in your settings files to enable webpack to function with Django.

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
    'WATCH': DEBUG,
    'HMR': DEBUG,
    'CONTEXT': {
        'DEBUG': DEBUG,
    },
}
```


### Template tags

A template tag is provided to integrate webpack at the template layer.

```html
{% load webpack %}

{% webpack 'path/to/webpack.config.js' as bundle %}

{{ bundle.render_css|safe }}

{{ bundle.render_js|safe }}
```


Settings
--------

If you are using this library in a Django project, please refer to the [Django integration](#django-integration)
section of the documentation for the incantation necessary to declare settings. For non-django projects, settings
can be defined by calling `webpack.conf.settings.configure` with keyword arguments matching the setting that you
want to define. For example

```python
from webpack.conf import settings

DEBUG = True

settings.configure(
    STATIC_ROOT='/path/to/your/projects/static_root',
    STATIC_URL='/static/',
    WATCH=DEBUG,
    HMR=DEBUG,
    CONTEXT: {
        'DEBUG': DEBUG,
    },
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


### CONFIG_DIRS

A list of paths that will be used to resolve relative paths to config files.

Default: `None`


### WATCH

A boolean flag which indicates that file watchers should be set to watch the assets's source
files. When a change is detected, the files which have changed are recompiled in the background
so that the assets are ready for the next request.

Set this to `True` in development environments.

Default: `False`


### HMR

A boolean flag indicating that webpack-build should inject a hmr runtime into the generate bundle.
When the runtime is loaded on a page, it opens sockets to the build server and wait for signals
that the assets have changed. When a change signal is received, the hmr runtime will attempt to
safely update the page. If the page cannot be updated safely, console logs will indicate that
a refresh is required.

Set this to `True` in development environments.

Default: `False`


### CONTEXT

The default context provided to config functions. This sets default values for the context object
passed to webpack-build.

Default: `None`


### CACHE

A flag indicating that webpack-build should maintain a persistent file cache.

Default: `True`


### CACHE_DIR

An override for the directory that webpack-build uses to store cache files.

Default: `None`


### OUTPUT_DIR

The directory in `STATIC_ROOT` which webpack will output all assets to.

Default: `'webpack_assets'`


### AGGREGATE_TIMEOUT

The delay between the detection of a change in your source files and the start of a compiler's
rebuild process.

Default: `200`


### POLL

If defined, this is a flag which indicates that watching compilers should poll for file changes, rather
than relying on the OS for notifications.

If the compiler is not detecting changes to your files, setting this to `True` may resolve the problem.

Default: `None`


Running the tests
-----------------

```bash
pip install -r requirements.txt
npm install
python runtests.py
```
