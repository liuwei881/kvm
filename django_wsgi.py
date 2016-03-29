#coding=utf-8

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zcloud.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
