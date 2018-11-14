import os
from dotenv import load_dotenv
from config.settings.base import *

load_dotenv()

# DEBUG config

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY')
## Database config
DATABASES = {
 'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': os.getenv('DB_NAME'),
      'USER': os.getenv('DB_USER'),
      'PASSWORD': os.getenv('DB_PASSWORD'),
      'PORT': os.getenv('DB_PORT'),
 }
}
