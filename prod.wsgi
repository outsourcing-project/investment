import os
import sys
sys.stdout = sys.stderr
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/bddyq/envs/investment/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/bddyq/workspace/investment')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/bddyq/envs/investment/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()
