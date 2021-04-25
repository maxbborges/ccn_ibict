import os
import sys

sys.path.append('./ccn_ibit')
sys.path.append('./ccn')
sys.path.append('./venv/lib/python3.6/site-package')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ccn_ibict.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()