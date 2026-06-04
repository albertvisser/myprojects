"""View for Myprojects startup screen
"""
from django.http import HttpResponseRedirect


def index(request):
    "startpage view"
    return HttpResponseRedirect('/docs/')
