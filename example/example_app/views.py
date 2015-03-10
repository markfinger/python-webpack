from django.shortcuts import render
from django_webpack.compiler import webpack


def index(request):
    webpack_bundle = webpack('example_app/webpack.config.js')
    return render(request, 'index.html', {
        'webpack_bundle': webpack_bundle,
    })