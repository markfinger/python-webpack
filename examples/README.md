python-webpack examples
=======================

Illustrates how to integrate webpack into a python project. Hot module replacement is activated by default,
so your changes to the js and css files will be applied live.

Before running any of the examples:

```
# install the dependencies
npm install

# start the build server
npm start
```

An example Flask project lives in ./flask

An example Django project lives in ./django

Both projects use a shared JS codebase, which lives in ./app, and a shared config file, ./example.webpack.js