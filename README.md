python-webpack
==============

[![Build Status](https://travis-ci.org/markfinger/python-webpack.svg?branch=master)](https://travis-ci.org/markfinger/python-webpack)

Python bindings to webpack, via [webpack-build](https://github.com/markfinger/webpack-build)


Documentation
-------------

- [Installation](#installation)
- [Basic usage](#basic-usage)
- [Config files](#config-files)
- [Usage in production](#usage-in-production)
- [Settings](#settings)
- [Django integration](#django-integration)
- [Running the tests](#running-the-tests)


Installation
------------

```
pip install python-webpack
```

And install the JS dependencies with

```
npm install webpack webpack-build --save
```


Basic usage
-----------

python-webpack provides a high-level interface to a webpack-build server. To start the server, run
`node_modules/.bin/webpack-build`. Requests are sent to the build server and python-webpack returns objects 
that allows you to interact with the results of the build.

Build requests should be sent with the path to the config file

```python
from webpack.compiler import webpack

bundle = webpack('path/to/webpack.config.js')
```

Once the build has completed, you can pass the returned object directly into your templates. The object
provides two convenience methods, `render_css` and `render_js` which emit `<link>` and `<script>` elements
pointing to the generated assets.


Config files
------------

For webpack's config reference, refer to the [official docs](https://webpack.github.io/docs/configuration.html).

Be aware that webpack-build deviates slightly from webpack's CLI in that it requires config files
to export a function which accepts options and returns a config object. Consult 
[webpack-build's docs](https://github.com/markfinger/webpack-build) for more information.

If you want to use relative paths to config files, you should specify the `CONFIG_DIRS` setting.

Config functions are provided with the options sent from python-webpack, you can set conditionals to change
your setup based on the flags sent to webpack-build.

To pass context down to your config function, you can specify defaults in the `CONTEXT` setting. You can 
also provide per-build context by using the `context` argument on the `webpack.compiler.webpack` function.
In your config functions, you can access the context via the options object's `context` property.

Be aware that the `output.path` property on config objects is overridden. All output is automatically 
redirected to directories within the `STATIC_ROOT`.


Hot module replacement
----------------------

If you set the `HMR` setting to True, assets that are rendered on the client-side will open sockets to webpack-build's server and listen for change notifications. When the assets have been rebuilt, they
will attempt to automatically update themselves. If they are unable to, they will log to the console 
indicating that you will need to refresh.

If you want to change your config for situations where the python layer has requested HMR, use the `hmr` 
flag on the options argument provided to config functions.


Usage in production
-------------------

**TODO**


Settings
--------

Settings can be defined by calling `webpack.conf.settings.configure` with keyword arguments matching 
the setting that you want to define. For example

```python
from webpack.conf import settings

DEBUG = True

settings.configure(
    STATIC_ROOT='/path/to/your/projects/static_root',
    STATIC_URL='/static/',
    WATCH=DEBUG,
    HMR=DEBUG,
)
```

In a Django project, you should define the settings within your settings file. Add them to a dictionary 
named `WEBPACK` and python-webpack will introspect your settings during startup.


### STATIC_ROOT

An absolute path to the root directory that you use for static assets. For example, 
`'/path/to/your/projects/static_root'`.

This setting **must** be defined.

Default: `None`


### STATIC_URL

The root url that your static assets are served from. For example, `'/static/'`.

This setting **must** be defined.

Default: `None`


### CONFIG_DIRS

A list of paths that will be used to resolve relative paths to config files.

Default: `None`


### WATCH

A boolean flag which indicates that file watchers should be set to watch the assets's source
files. When a change is detected, the files which have changed are recompiled in the background
so that the assets are ready for the next request. Set this to `True` in development environments.

Default: `False`


### HMR

A boolean flag indicating that webpack-build should inject a hmr runtime into the generated assets.
Set this to `True` in development environments.

Default: `False`


### CONTEXT

The default context provided to config functions. You can use this to pass data and flags down to your 
config functions.

Default: `None`


### CONFIG_DIRS

An iterable of directories that python-webpack will use to resolve relative paths to config files.

Default: `None`


### MANIFEST

A dictionary of config files and context objects that is used to populate manifest files. The keys
should be paths to config files and the values should be either `None` or an iterable of context objects
that are used to generate unique builds of each config file.

Default: `None`


### USE_MANIFEST

A flag indicating that python-webpack should use the manifest file, rather than opening connections to
the build server.

Default: `False`


### MANIFEST_PATH

An absolute path to the file used to store the manifest.

Default: `None`


### CACHE

A flag indicating that webpack-build should maintain a persistent file cache. The file cache is used to 
improve response times for builds that have already been completed.

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


Django integration
------------------

### Installation and configuration

The following configuration should be placed in your settings files to enable python-webpack to function 
with Django.

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


Running the tests
-----------------

```bash
pip install -r requirements.txt
npm install
python runtests.py
```
