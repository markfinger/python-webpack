Django Webpack
==============

An interface to leverage Webpack's frontend tooling and Django's static asset
configuration and introspection.


```python
from django_webpack.models import WebpackBundle

# Define your bundle
bundle = WebpackBundle(entry='path/to/entry.js')
```

```html
{# Render a script element pointing to the bundle #}

{{ bundle.render }}
```

Documentation
-------------

- [Installation](#installation)
- [Basic Usage](#basicusage)
- [WebpackBundle](#webpackbundle)
  - [is_installed](#django_webpacknodeis_installed)
- [bundle()](#bundle)
  - [is_installed](#django_webpacknpmis_installed)
- [Settings](#settings)
  - [PATH_TO_NODE](#django_webpackpath_to_node)
- [Running the tests](#running-the-tests)


Installation
------------

```bash
pip install django-webpack
```


WebpackBundle
-------------

`django_webpack.models.WebpackBundle` provide a simple, yet extensible, interface to Webpack's
frontend tooling.

A `WebpackBundle` instance must be instantiated with argument or attribute named `entry` which
is a relative path to the entry file of a bundle. The file will be resolved via Django's static
file finders.

A `WebpackBundle` will accept configuration options via keyword arguments or attributes which
correspond to the options specified in (Bundle configuration)[#bundleconfiguration].

### Basic usage

Bundles can be defined by invoking `WebpackBundle` with a path to an entry file.

```python
from django_webpack.models import WebpackBundle

bundle = WebpackBundle(entry='path/to/entry.js')
```

Alternatively, you can inherit from `WebpackBundle`.

```python
from django_webpack.models import WebpackBundle

class SomeBundle(WebpackBundle):
    entry='path/to/entry.js'

bundle = SomeBundle()
```

The easiest way to integrate a bundle into your frontend is to pass the bundle into your template's
context and invoke its `render` method, which will output a script element.

```html
{{ bundle.render }}
```

### render()

Returns a HTML script element with a src attribute pointing to the bundle.

```html
{{ bundle.render }}
```

### get_url()

Returns a url to the bundle.

The url is inferred from Django's STATIC_ROOT and STATIC_URL settings.

```python
bundle.get_url()
```

### get_path()

Returns an absolute path to the bundle's file on your filesystem.

```python
bundle.get_path()
```

### get_rel_path()

Returns a path to the bundle's file relative to the STATIC_ROOT.

```python
bundle.get_rel_path()
```


bundle()
--------

A method that allows you to invoke Webpack more directly.

Arguments:

- `path_to_entry`: an absolute path to the entry file of the bundle.
- `path_to_output`: an absolute path to the output file of the bundle. The output filename may take advantage of
  Webpack's file hashing by including a `[hash]` substring within the path - for example:
  `'/path/to/file/bundle-[hash].js'`.
- `bundle` will also accept keyword arguments corresponding to the options specified in
  (Bundle configuration)[#bundleconfiguration].

```python
from django_webpack import webpack

path_to_bundle = webpack.bundle(
    path_to_entry='/path/to/entry.js'),
    path_to_output='/path/to/output-[hash].js'),
)
```


Bundle configuration
--------------------

The following options can be either passed into the constructor of a `WebpackBundle`,
defined as attributes on a class inheriting from `WebpackBundle`, or passed into
`django_webpack.webpack.bundle` as keyword arguments.

### path_to_output

An absolute path to the output of your bundle. Output filenames can take advantage of
Webpack's filename hashing to easily circumvent stale file caches. If you wish to take advantage
of the rendering or urls of `WebpackBundle`, the path should include your `STATIC_ROOT`.

```python
from django.conf.settings import STATIC_ROOT
from django_webpack import WebpackBundle

class MyBundle(WebpackBundle):
    path_to_output = os.path.join(STATIC_ROOT, 'path/to/output-[hash].js')
```

### library

A variable name which your bundle will expose to the global scope. Using `library`
will allow your bundle to be accessible via a browser global.

```python
from django_webpack import WebpackBundle

class MyBundle(WebpackBundle):
    library = 'someVariableName'
```

### externals

A dictionary of packages which will be not be bundled, instead the `require('package')` statements will
resolve to the corresponding variable within the browser's global scope. This is useful for accessing 3rd-party
libraries.

```python
from django_webpack import WebpackBundle

class MyBundle(WebpackBundle):
    externals = {
        # Rather than bundling jQuery, we rely on its global variable
        'jquery': 'window.$',
    }
```

### loaders

A tuple of dictionaries that define which Webpack loader to use for loading particular types of files.

```python
from django_webpack import WebpackBundle

class MyBundle(WebpackBundle):
    loaders = (
        {'loader': 'jsx', 'test': '.jsx$'},
    )
```

### paths_to_loaders

A tuple of paths that will be used to resolve Webpack loaders. If your project uses loaders that are not
available by default, you will have to provide paths to the directories where Webpack can find them.

```python
import os
from django_webpack import WebpackBundle

location_of_loader_packages = '/path/to/node_modules'

class MyBundle(WebpackBundle):
    paths_to_loaders = (location_of_loader_packages,)
```

### no_parse

A tuple of package name that Webpack will not parse for 'require' calls. This can help to improve the
performance of bundling an asset which depends on large packages such as jQuery.

```python
from django_webpack import WebpackBundle

class MyBundle(WebpackBundle):
    no_parse = ('jquery',)
```

### devtool

A string that defines the tool that Webpack will use to assist with development. By default, this will
be `'eval-entry-map'` if `DEBUG` is `True`.

```python
from django_webpack import WebpackBundle

class MyBundle(WebpackBundle):
    devtool = 'inline-source-map'
```

### bail

A boolean that indicates if Webpack should raise an error when it first encounters a problem. By default, this is
`True`.

```python
from django_webpack import WebpackBundle

class MyBundle(WebpackBundle):
    bail = True
```


Settings
--------

Settings can be overridden by defining a dictionary named `DJANGO_WEBPACK` in your settings file.

```python
DJANGO_WEBPACK = {
    'NODE_VERSION_REQUIRED': (0, 12, 0,),
}
```

### DJANGO_WEBPACK['NODE_VERSION_REQUIRED']

The version of Node.js required to use Django Webpack. Dependencies are checked when Django Webpack is
first initialised.

Default:
```python
(0, 10, 0)
```

### DJANGO_WEBPACK['NPM_VERSION_REQUIRED']

The version of NPM required to use Django Webpack. Dependencies are checked when Django Webpack is
first initialised.

Default:
```python
(1, 2, 0)
```

### DJANGO_WEBPACK['PATH_TO_BUNDLER']

An absolute path to the bundler which is used as a JS interface to Webpack.

Default:
```python
# __file__ = `django_webpack.settings`
os.path.abspath(os.path.join(os.path.dirname(__file__), 'bundle.js'))
```

### DJANGO_WEBPACK['STATIC_ROOT']

An absolute path to the directory which Django Webpack's static file helpers
should consider to be the root.

Default:
```python
django.conf.settings.STATIC_ROOT
```

### DJANGO_WEBPACK['STATIC_URL']

The url which is prepended to the relative path of bundle in order to generate a url.

Default:
```python
django.conf.settings.STATIC_URL
```

### DJANGO_WEBPACK['DEBUG']

If True, Django Webpack activate more tooling to assist development.

Default:
```python
django.conf.settings.DEBUG
```

### DJANGO_WEBPACK['CACHE']

If `True`, Django Webpack will maintain an in-memory cache of the output generated by
Webpack and immediately return the path to the bundle. This can massively improve the speed
of rendering bundles, but is obviously not recommended for development. In order to prevent
collisions, cache keys are generated from the arguments piped to Webpack.

Default:
```python
not django.conf.settings.DEBUG
```


Running the tests
-----------------

```bash
python django_webpack/tests/runner.py
```