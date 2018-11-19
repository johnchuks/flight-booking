from .base import *
from dj_database_url import config, parse
from dotenv import load_dotenv

load_dotenv()

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.getenv('SECRET_KEY')


## Database config
DATABASES = {
 'default': parse(os.getenv('PROD_DB_URL'))
}

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')