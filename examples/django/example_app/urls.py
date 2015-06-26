from django.views.generic import TemplateView
from django.conf.urls import url


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='example_app/index.html')),
]
