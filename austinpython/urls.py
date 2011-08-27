from django.conf.urls.defaults import patterns, url, include
from austinpython.ap.views import HomeView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^opportunities/', include('austinpython.opportunities.urls')),
    url(r'^register/austinpython$',
        'austinpython.registration.views.register_austinpython_get'),
    url(r'^register/austinpython/submit',
        'austinpython.registration.views.register_austinpython_post')
)
