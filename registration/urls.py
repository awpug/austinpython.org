from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('registration.views',
    url(r'^register/$', 'register', name='register'),
)
