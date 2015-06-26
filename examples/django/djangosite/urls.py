from django.views.generic import TemplateView
from django.conf.urls import url, include
from webpack.compiler import webpack


class IndexView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['bundle'] = webpack('example.webpack.js')
        return context

urlpatterns = [
    url(r'^$', include('example_app.urls')),
]
