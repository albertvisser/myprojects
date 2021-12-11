"""Url configuration for MyProjects application  - betere namen
"""
from django.urls import path, include
from django.views.static import serve as serve_static
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('', views.index),      # start

    # project homepage
    path('proj/new/', views.new_project),                 # nieuw (opengezet voor wijzigen)
    path('proj/mut/', views.add_new_proj),                # nieuw (wijzigingen doorvoeren)
    path('<int:proj>/', views.view_project),              # raadplegen
    path('<int:proj>/meld/<meld>/', views.view_project),  # raadplegen met melding
    path('<int:proj>/edit/', views.edit_project),         # opengezet voor wijzigen
    path('<int:proj>/mut/', views.update_project),        # wijzigen doorvoeren

    path('<int:proj>/<slug:soort>/', views.lijst),        # lijst documenten bij project

    # document details
    path('<int:proj>/<slug:soort>/new/', views.new_document),  # nieuw (opengezet voor wijzigen)
    path('<int:proj>/<slug:soort>/mut/', views.update_document),  # nieuw (wijzigingen doorvoeren)
    path('<int:proj>/<slug:soort>/<int:id>/', views.view_document),            # raadplegen
    path('<int:proj>/<slug:soort>/<int:id>/msg/<meld>', views.view_document),  # idem met melding
    path('<int:proj>/<slug:soort>/<int:id>/edit/', views.edit_document), # opengezet voor wijzigen
    path('<int:proj>/<slug:soort>/<int:id>/mut/', views.update_document),  # wijzigingen doorvoeren

    # relateren document aan ander document
    path('<int:proj>/<slug:soort>/rel/<slug:srt>/<int:id>/', views.lijst, {'rel': 'from'}),
    path('<int:proj>/<slug:srt>/<int:id>/rel/<slug:soort>/', views.lijst, {'rel': 'to'}),
    path('<int:proj>/<slug:srt>/<int:id>/rel/<slug:rel>/<slug:soort>/<int:verw>/',
        views.maak_rel),
    path('<int:proj>/<slug:srt>/<int:id>/unrel/<slug:rel>/<slug:soort>/<int:verw>/',
        views.unrelate),

    # opvoeren document via link vanuit ander document (bv. funcproc bij functaak)
    path('<int:proj>/<slug:soort>/new/<slug:srt>/<int:verw>/', views.new_from_relation),
    path('<int:proj>/<slug:soort>/mut/<slug:srt>/<int:verw>/', views.update_document),

    # koppeling met actiereg
    # deze extra views is om vast te houden vanuit welle selectie je komt
    path('<int:proj>/<slug:soort>/<int:id>/koppel/', views.koppel),
    path('<int:proj>/<slug:soort>/<int:id>/koppel/<slug:arid>/<slug:arnum>/',
        views.koppel),
    path('<int:proj>/<slug:soort>/<int:id>/meld/', views.meld),
    path('<int:proj>/<slug:soort>/<int:id>/meld/<slug:arstat>/<slug:arfrom>/<int:arid>/',
        views.meld),

    # opvoeren/wijzigen attribuut/element bij entiteit/dataitem
    path('<int:proj>/<slug:srt1>/<int:id1>/<slug:srt2>/add/', views.edit_sub),
    path('<int:proj>/<slug:srt1>/<int:id1>/<slug:srt2>/<int:id2>/mut/', views.edit_sub),

    # # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # # to INSTALLED_APPS to enable admin documentation:
    # path('admin/doc/', include('django.contrib.admindocs.urls')),

    # # Uncomment the next line to enable the admin:
    # path('admin/', admin.site.urls),

    # media - static files to be served from development server
    path('files/<path>', serve_static,
        {'document_root': '/home/albert/www/django/myprojects/files'}),
]
