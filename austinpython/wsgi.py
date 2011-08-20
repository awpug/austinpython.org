import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # outside project
os.environ['DJANGO_SETTINGS_MODULE'] = 'austinpython.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
