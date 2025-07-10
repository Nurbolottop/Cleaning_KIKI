<<<<<<< HEAD
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise Exception("SECRET_KEY не задан в переменных окружения")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

=======
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise Exception("SECRET_KEY не задан в переменных окружения")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

>>>>>>> 3da9a24fed32cd4ff816f1cc31908e8e39f2cc4a
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')