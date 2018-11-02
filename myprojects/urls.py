"""Url configuration for MyProjects application
"""
from django.conf.urls import url, include
from django.views.static import serve as serve_static
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Example:
    # url(r'^magiokis/', include('magiokis.foo.urls')),
    url(r'^$',
        views.index),      # start
    url(r'^(?P<proj>proj)/(?P<edit>new)/$',
        views.detail),     # nieuw project
    url(r'^(?P<proj>\d+)/$',
        views.detail),     # homepage project
    url(r'^(?P<proj>\d+)/(?P<edit>edit)/$',
        views.detail),     # homepage project opengezet voor wijzigen
    url(r'^(?P<proj>\d+)/meld/(?P<meld>.+)/$',
        views.detail),     # homepage project met melding
    url(r'^(?P<proj>proj)/mut/$',
        views.edit_item),  # nieuw project (wijzigingen doorvoeren)
    url(r'^(?P<proj>\d+)/mut/$',
        views.edit_item),  # homepage project (wijzigen doorvoeren)
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/$',
        views.lijst),      # lijst documenten bij project
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<edit>new)/$',
        views.detail),     # nieuw document  bij project
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/$',
        views.detail),     # document  bij project
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/msg/(?P<meld>.+)$',
        views.detail),     # document  bij project
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/(?P<edit>edit)/$',
        views.detail),     # document  bij project  opengezet voor wijzigen
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/meld/$',
        views.meld),       # document  bij project  opengezet voor wijzigen
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/meld/'
        r'(?P<arstat>\w+)/(?P<arfrom>\w+)/(?P<arid>\d+)/$',
        views.meld),       # document  bij project  opengezet voor wijzigen
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/koppel/$',
        views.koppel),     # document  bij project  opengezet voor wijzigen
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/koppel/'
        r'(?P<arid>\d+)/(?P<arnum>.+)/$',
        views.koppel),     # document  bij project  opengezet voor wijzigen
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/mut/$',
        views.edit_item),  # nieuw document  bij project (wijzigingen doorvoeren)
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/mut/$',
        views.edit_item),  # document  bij project (wijzigingen doorvoeren)

    # opvoeren/wijzigen attribuut/element bij entiteit/dataitem
    url(r'^(?P<proj>\d+)/(?P<srt1>\w+)/(?P<id1>\d+)/(?P<srt2>\w+)/add/',
        views.edit_sub),
    url(r'^(?P<proj>\d+)/(?P<srt1>\w+)/(?P<id1>\d+)/(?P<srt2>\w+)/(?P<id2>\d+)/mut/',
        views.edit_sub),

    # opvoeren document via link vanuit ander document (bv. funcproc bij functaak)
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<edit>new)/(?P<srt>\w+)/(?P<verw>\d+)/$',
        views.detail),
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/mut/(?P<srt>\w+)/(?P<verw>\d+)/$',
        views.edit_item),

    # relateren document aan ander document
    url(r'^(?P<proj>\d+)/(?P<soort>\w+)/rel/(?P<srt>\w+)/(?P<id>\d+)/$',
        views.lijst, {'rel': 'from'}),
    url(r'^(?P<proj>\d+)/(?P<srt>\w+)/(?P<id>\d+)/rel/(?P<soort>\w+)/$',
        views.lijst, {'rel': 'to'}),
    url(r'^(?P<proj>\d+)/(?P<srt>\w+)/(?P<id>\d+)/rel/(?P<rel>\w+)/(?P<soort>\w+)/(?P<verw>\d+)/$',
        views.maak_rel),
    url(r'^(?P<proj>\d+)/(?P<srt>\w+)/(?P<id>\d+)/unrel/(?P<rel>\w+)/(?P<soort>\w+)/(?P<verw>\d+)/$',
        views.unrelate),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # media - static files to be served from development server
    url(r'^files/(?P<path>.+)$', serve_static,
        {'document_root': '/home/albert/www/django/myprojects/files'}),
]
