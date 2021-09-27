"""Url configuration for MyProjects application
"""
from django.urls import path, include
from django.views.static import serve as serve_static
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Example:
    # path('magiokis/', include('magiokis.foo.urls')),
    path('', views.index),      # start
    path('proj/new/', views.new_project),              # nieuw project
    path('<int:proj>/', views.detail),                 # homepage project
    path('<int:proj>/edit/', views.edit_project),      # homepage project opengezet voor wijzigen
    path('<int:proj>/meld/<meld>/', views.detail),     # homepage project met melding
    path('proj/mut/', views.add_new_proj),             # nieuw project (wijzigingen doorvoeren)
    path('<int:proj>/mut/', views.edit_item),          # homepage project (wijzigen doorvoeren)
    path('<int:proj>/<slug:soort>/', views.lijst),     # lijst documenten bij project
    path('<int:proj>/<slug:soort>/new/', views.new_document),           # nieuw document bij project
    path('<int:proj>/<slug:soort>/<int:id>/', views.detail),            # document bij project
    path('<int:proj>/<slug:soort>/<int:id>/msg/<meld>', views.detail),  # document bij project
    # document bij project opengezet voor wijzigen
    path('<int:proj>/<slug:soort>/<int:id>/edit/', views.edit_document),
    path('<int:proj>/<slug:soort>/<int:id>/meld/', views.meld),
    path('<int:proj>/<slug:soort>/<int:id>/koppel/', views.koppel),
    # deze extra views is om vast te houden vanuit welle selectie je komt
    path('<int:proj>/<slug:soort>/<int:id>/meld/<slug:arstat>/<slug:arfrom>/<int:arid>/',
        views.meld),
    path('<int:proj>/<slug:soort>/<int:id>/koppel/<slug:arid>)/<slug:arnum>/',
        views.koppel),
    path('<int:proj>/<slug:soort>/mut/', views.edit_item),  # nieuw doc bij proj - wijz doorvoeren
    path('<int:proj>/<slug:soort>/<int:id>/mut/', views.edit_item),  # doc bij proj wijz doorvoeren

    # opvoeren/wijzigen attribuut/element bij entiteit/dataitem
    path('<int:proj>/<slug:srt1>)/<int:id1>)/<slug:srt2>/add/', views.edit_sub),
    path('<int:proj>/<slug:srt1>)/<int:id1>)/<slug:srt2>)/<int:id2>/mut/', views.edit_sub),

    # opvoeren document via link vanuit ander document (bv. funcproc bij functaak)
    path('<int:proj>/<slug:soort>/new/<slug:srt>/<int:verw>/', views.new_from_relation),
    path('<int:proj>/<slug:soort>/mut/<slug:srt>/<int:verw>/', views.edit_item),

    # relateren document aan ander document
    path('<int:proj>/<slug:soort>/rel/<slug:srt>/<int:id>/', views.lijst, {'rel': 'from'}),
    path('<int:proj>/<slug:srt>)/<int:id>/rel/<slug:soort>/', views.lijst, {'rel': 'to'}),
    path('<int:proj>/<slug:srt>)/<int:id>/rel/<slug:rel>/<slug:soort>/<int:verw>/',
        views.maak_rel),
    path('<int:proj>/<slug:rt>)/<int:id>/unrel/<slug:rel>/<slug:soort>/<int:verw>/',
        views.unrelate),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    path('admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),

    # media - static files to be served from development server
    path('files/(<slug:path>/)', serve_static,
        {'document_root': '/home/albert/www/django/myprojects/files'}),
]
