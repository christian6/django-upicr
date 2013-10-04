import os
import sys

sys.path.append('/home/adminweb/dev/icrperu.com')
sys.path.append('/home/adminweb/dev/icrperu.com/icrperu')

os.environ['DJANGO_SETTINGS_MODULE'] = 'icrperu.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
