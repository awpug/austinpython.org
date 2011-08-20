from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
#from django.views.generic.simple import direct_to_template

from cms.sitemaps import CMSSitemap

admin.autodiscover()
sitemaps = {
    'cmspages' : CMSSitemap,
}

urlpatterns = patterns('',
#    (r'^admin/tinymce/templates/$', direct_to_template, {'template' : 'admin/tinymce/templates.js'}),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^robots.txt$', include('robots.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)


if settings.SERVE_STATIC_MEDIA:
    urlpatterns += patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    )

urlpatterns += patterns('',
    (r'^', include('cms.urls')),
)
