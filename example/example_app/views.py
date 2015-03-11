from django.shortcuts import render
from django_webpack.compiler import webpack


def example(request):
    webpack_bundle = webpack('example_app/webpack.config.js')
    return render(request, 'example_app/index.html', {
        'webpack_bundle': webpack_bundle,
    })