from django.conf.urls.defaults import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'rasp.views.home', name='home'),
    url(r'^table$', 'main.views.table', name='table'),
    url(r'^stand$', 'main.views.stand', name='stand'),
    url(r'^$', 'main.views.groups_list', name='groups_list'),
    url(r'^preps$', 'main.views.preps_list', name='preps_list'),
    url(r'^(\w+)/(\d+)$', 'main.views.pairs_list', name='pairs_list'),
    url(r'^(\w+)/(\d+)/(\d+)$', 'main.views.pairs_list', name='pairs_list'),
    url(r'^ical/(\w+)/(\d+).ical$', 'main.views.ical', name='ical'),
    # url(r'^rasp/', include('rasp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
