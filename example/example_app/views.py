import os
from django.shortcuts import render
from django_node import npm
from django_webpack import WebpackBundle

npm.install(os.path.dirname(__file__))


def index(request):
    webpack_bundle = WebpackBundle('example_app/webpack.config.js')
    return render(request, 'index.html', {
        'webpack_bundle': webpack_bundle,
    })