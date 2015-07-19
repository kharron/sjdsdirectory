import os, sys
sys.path.append('/www/sites/sjdsdirectory')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sjdsdirectory.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
