from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # app/static
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
