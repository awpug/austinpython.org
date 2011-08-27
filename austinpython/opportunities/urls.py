""" The urls for the opportunities views. """

from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView
from austinpython.opportunities.models import Opportunity

urlpatterns = patterns('',
    url("^$", ListView.as_view(model=Opportunity)),
    #url("^(?P<uid>[a-f0-9]{10})\/(?P<slug>[a-z0-9\-]+)$", DetailView.as_view(
)
