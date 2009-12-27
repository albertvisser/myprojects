from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^magiokis/', include('magiokis.foo.urls')),
    (r'^$',                                                         'views.index'), # start
    (r'^proj/$',                                                    'views.detail'), # start
    (r'^(?P<proj>proj)/(?P<edit>new)/$',                            'views.detail'), # nieuw project
    (r'^(?P<proj>\d+)/$',                                           'views.detail'),  # homepage project
    (r'^(?P<proj>\d+)/(?P<edit>edit)/$',                            'views.detail'),  # homepage project opengezet voor wijzigen
    (r'^(?P<proj>proj)/mut/$',                                      'views.edit_item'),# nieuw project (wijzigingen doorvoeren)
    (r'^(?P<proj>\d+)/mut/$',                                       'views.edit_item'),# homepage project (wijzigen doorvoeren)
    (r'^(?P<proj>\d+)/(?P<soort>\w+)/$',                            'views.lijst'), # lijst documenten bij project
    (r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<edit>new)/$',              'views.detail'), # nieuw document  bij project
    (r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/$',                'views.detail'), # document  bij project
    (r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/(?P<edit>edit)/$', 'views.detail'), # document  bij project  opengezet voor wijzigen
    (r'^(?P<proj>\d+)/(?P<soort>\w+)/mut/$',                        'views.edit_item'), # nieuw document  bij project (wijzigingen doorvoeren)
    (r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<id>\d+)/mut/$',            'views.edit_item'), # document  bij project (wijzigingen doorvoeren)

    # opvoeren/wijzigen attribuut/element bij entiteit/dataitem
    (r'^(?P<proj>\d+)/(?P<srt1>\w+)/(?P<id1>\d+)/(?P<srt2>\w+)/add/',             'views.edit_sub'),
    (r'^(?P<proj>\d+)/(?P<srt1>\w+)/(?P<id1>\d+)/(?P<srt2>\w+)/(?P<id2>\d+)/mut/', 'views.edit_sub'),

    # opvoeren document via link vanuit ander document (bv. funcproc bij functaak)
    (r'^(?P<proj>\d+)/(?P<soort>\w+)/(?P<edit>new)/(?P<srt>\w+)/(?P<verw>\d+)/$', 'views.detail'),
    (r'^(?P<proj>\d+)/(?P<soort>\w+)/mut/(?P<srt>\w+)/(?P<verw>\d+)/$',           'views.edit_item'),

    # relateren document aan ander document
    (r'^(?P<proj>\d+)/(?P<srt>\w+)/(?P<id>\d+)/(?P<edit>rel)/(?P<soort>\w+)/$',     'views.lijst'),
    (r'^(?P<proj>\d+)/(?P<srt>\w+)/(?P<id>\d+)/rel/(?P<soort>\w+)/(?P<verw>\d+)/$', 'views.maak_rel'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    # media - static files to be served from development server
    (r'^files/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'I:/www/django/doctool/files'}),
)
