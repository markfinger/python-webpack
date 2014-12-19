Django Webpack
==============

Generate Webpack bundles from a Django application.
```python
from django_webpack.models import WebpackBundle

bundle = WebpackBundle(entry='path/to/entry.js')

url_to_bundle = bundle.get_url()
path_to_bundle = bundle.get_path()
```

You can also render a `<script>` element pointing to your bundle
```html
{{ bundle.render }}
```

Documentation
-------------

- [Installation](#installation)
- [WebpackBundle](#webpackbundle)
  - [Basic usage](#basic-usage)
  - [WebpackBundle.render()](#webpackbundlerender)
  - [WebpackBundle.get_url()](#webpackbundleget_url)
  - [WebpackBundle.get_path()](#webpackbundleget_path)
  - [WebpackBundle.get_rel_path()](#webpackbundleget_rel_path)
- [webpack.bundle()](#webpackbundle-1)
- [Bundle configuration](#bundle-configuration)
  - [path_to_output](#path_to_output)
  - [library](#library)
  - [externals](#externals)
  - [loaders](#loaders)
  - [paths_to_loaders](#paths_to_loaders)
  - [no_parse](#no_parse)
  - [devtool](#devtool)
  - [bail](#bail)
- [Settings](#settings)
  - [NODE_VERSION_REQUIRED](#django_webpacknode_version_required)
  - [NPM_VERSION_REQUIRED](#django_webpacknpm_version_required)
  - [PATH_TO_BUNDLER](#django_webpackpath_to_bundler)
  - [STATIC_ROOT](#django_webpackstatic_root)
  - [STATIC_URL](#django_webpackstatic_url)
  - [DEBUG](#django_webpackdebug)
  - [CACHE](#django_webpackcache)
  - [DEVTOOL](#django_webpackdevtool)
- [Running the tests](#running-the-tests)


Installation
------------

```bash
pip install django-webpack
```


WebpackBundle
-------------

`django_webpack.models.WebpackBundle` provide a simple, yet extensible, interface to Webpack's
frontend tooling and Django's static asset configuration and introspection.

A `WebpackBundle` instance must be instantiated with an argument or attribute named `entry` which
is a relative path to the entry file of a bundle. The absolute path to the file will be resolved 
via Django's static file finders.

A `WebpackBundle` will also accept the configuration options specified in [Bundle configuration](#bundle-configuration).
Options must be provided as either keyword arguments or attributes.

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

### WebpackBundle.render()

Returns a HTML script element with a src attribute pointing to the bundle.

```html
{{ bundle.render }}
```

### WebpackBundle.get_url()

Returns a url to the bundle.

The url is inferred from Django's STATIC_ROOT and STATIC_URL settings.

```python
bundle.get_url()
```

### WebpackBundle.get_path()

Returns an absolute path to the bundle's file on your filesystem.

```python
bundle.get_path()
```

### WebpackBundle.get_rel_path()

Returns a path to the bundle's file relative to the STATIC_ROOT.

```python
bundle.get_rel_path()
```


webpack.bundle()
----------------

A method which allows you to interface with Webpack more directly.

Arguments:

- `path_to_entry`: an absolute path to the entry file of the bundle.
- `path_to_output`: an absolute path to the output file of the bundle. The output filename may take advantage of
  Webpack's file hashing by including a `[hash]` substring within the path - for example:
  `'/path/to/output-[hash].js'`.

`bundle` will also accept keyword arguments corresponding to the options specified in [Bundle configuration](#bundle-configuration).

```python
from django_webpack import webpack

path_to_bundle = webpack.bundle(
    path_to_entry='/path/to/entry.js',
    path_to_output='/path/to/output-[hash].js',
)
```


Bundle configuration
--------------------

The following options can be passed into the constructor of a [WebpackBundle](#webpackbundle),
defined as attributes on a class inheriting from [WebpackBundle](#webpackbundle), or passed into
[webpack.bundle()](#webpackbundle-1) as keyword arguments.

### path_to_output

An absolute path to the output of your bundle. Output filenames can take advantage of
Webpack's filename hashing to easily circumvent stale file caches. If you wish to take advantage
of the rendering or urls of [WebpackBundle](#webpackbundle), the path should include your `STATIC_ROOT`.

```python
import os
from django.conf.settings import STATIC_ROOT
from django_webpack.models import WebpackBundle

class MyBundle(WebpackBundle):
    path_to_output = os.path.join(STATIC_ROOT, 'path/to/output-[hash].js')
```

### library

A variable name which your bundle will expose to the global scope. Use `library`
to allow your bundle to be accessed from the browser's global scope.

```python
from django_webpack.models import WebpackBundle

class MyBundle(WebpackBundle):
    library = 'someVariableName'
```

### externals

A dictionary of packages which will not be bundled, instead the `require('package')` statements will
resolve to the specified variable from the browser's global scope. This is useful for accessing 3rd-party
libraries or integrating bundles into environments with pre-defined libraries.

```python
from django_webpack.models import WebpackBundle

class MyBundle(WebpackBundle):
    externals = {
        # Rather than bundling jQuery, we rely on its global variable
        'jquery': 'window.$',
    }
```

### loaders

A tuple of dictionaries that define which Webpack loader to use for loading particular types of files.

```python
from django_webpack.models import WebpackBundle

class MyBundle(WebpackBundle):
    loaders = (
        {'loader': 'jsx', 'test': '.jsx$'},
    )
```

### paths_to_loaders

A tuple of paths that will be used to resolve Webpack loaders. If your project uses loaders that are not
available by default, you will have to provide paths to the directories where Webpack can find them.

```python
from django_webpack.models import WebpackBundle

path_to_loader_packages = '/path/to/node_modules'

class MyBundle(WebpackBundle):
    paths_to_loaders = (path_to_loader_packages,)
```

### no_parse

A tuple of package names that Webpack will not parse for 'require' calls. This can help to improve the
performance of building a bundle that depends on large packages such as jQuery.

```python
from django_webpack.models import WebpackBundle

class MyBundle(WebpackBundle):
    no_parse = ('jquery',)
```

### devtool

A string that defines a tool which Webpack will use to assist with development. The default value is defined by [`DJANGO_WEBPACK['DEVTOOL']`](#django_webpackdevtool).

```python
from django_webpack.models import WebpackBundle

class MyBundle(WebpackBundle):
    devtool = 'inline-source-map'
```

### bail

A boolean that indicates if Webpack should raise an error when it first encounters a problem. By default, this is
`True`. Setting this to `False` may cause Webpack to silently fail.

```python
from django_webpack.models import WebpackBundle

class MyBundle(WebpackBundle):
    bail = False
```


Settings
--------

Settings can be overridden by defining a dictionary named `DJANGO_WEBPACK` in your settings file.

```python
DJANGO_WEBPACK = {
    'DEBUG': False,
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

An absolute path to the bundler which is used as an interface to Webpack.

Default:
```python
# __file__ = django_webpack.settings.__file__
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

The url which is prepended to the relative path of bundle in order to generate a bundle's url.

Default:
```python
django.conf.settings.STATIC_URL
```

### DJANGO_WEBPACK['DEBUG']

If True, Django Webpack activates more tooling to assist development. Setting this to `False` is recommended
for production, but may introduce problems during development.

Default:
```python
django.conf.settings.DEBUG
```

### DJANGO_WEBPACK['CACHE']

If `True`, Django Webpack will maintain an in-memory cache of the output generated by
Webpack and immediately return a path to a previously-generated bundle. This can massively 
improve the speed of rendering bundles, but is obviously not recommended for development. 
Cache keys are generated from the arguments piped to Webpack, which include entry/output
files and the bundle's configuration options.

Default:
```python
not django_webpack.settings.DEBUG
```

### DJANGO_WEBPACK['DEVTOOL']

The default tool that [WebpackBundles](#webpackbundle) will use to assist in development.

Default:
```python
'eval-entry-map' if django_webpack.settings.DEBUG else None
```


Running the tests
-----------------

```bash
mkvirtualenv django-webpack
pip install -r requirements.txt
python django_webpack/tests/runner.py
```
