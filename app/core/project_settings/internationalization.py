<<<<<<< HEAD
from dotenv import load_dotenv
import os

load_dotenv()

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'ru')

TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Bishkek')

USE_I18N = True

=======
from dotenv import load_dotenv
import os

load_dotenv()

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'ru')

TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Bishkek')

USE_I18N = True

>>>>>>> 3da9a24fed32cd4ff816f1cc31908e8e39f2cc4a
USE_TZ = True