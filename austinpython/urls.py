from django.conf.urls.defaults import patterns, url, include
from austinpython.ap.views import HomeView
from austinpython.registration.views import TwitterRegistrationLink
from austinpython.registration.views import GitHubRegistrationLink
from austinpython.registration.views import GitHubRegistrationCallback

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^opportunities/', include('austinpython.opportunities.urls')),
    url(r'^register/austinpython$',
        'austinpython.registration.views.register_austinpython_get'),
    url(r'^register/austinpython/submit',
        'austinpython.registration.views.register_austinpython_post'),
    url(r'^register/twitter$', TwitterRegistrationLink.as_view()),
    url(r'^register/github$', GitHubRegistrationLink.as_view()),
    url(r'^register/github/callback$', GitHubRegistrationCallback.as_view())
)
