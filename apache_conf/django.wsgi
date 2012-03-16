import os
import sys
sys.path.append('/var/www/triple-t/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'webnotepad.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
