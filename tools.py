import os, sys, glob

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onspace.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
import django

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

### scripts ###
from utils.datasend import *
from utils.cleaner import Cleaner

if sys.argv[1] == 'cleanmigrations':
    c = Cleaner(start_path)
    c.clean_migrations()
    db = start_path + '/db.sqlite3'
    if os.path.exists(db):
        os.remove(db)
        print('Removed database')

elif sys.argv[1] == 'datasend':
    dart_send()
    resuce_send()
    print('information complete')
    invest_news_send()
    protfolio_send()
    LP_company_send()
    prof_send()
    main_company_send()
    print('news complete')
    print('datasend to database')