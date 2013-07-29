#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'myprojects.settings'

from django.core.servers.fastcgi import runfastcgi

runfastcgi(method="threaded", daemonize="false")
