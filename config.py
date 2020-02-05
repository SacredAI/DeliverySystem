import os
import sys

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

# Secret key for signing cookies
SECRET_KEY = b',chks\x9f|\x08\x94c-\x94\x90\xa5\xa2\xbd'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
GOOGLEMAPS_KEY = "AIzaSyCnv7-DdoGnfoGl--j7ShuFi7_FJ9QSW4E"