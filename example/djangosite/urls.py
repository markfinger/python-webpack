from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'example_app.views.example',)
)