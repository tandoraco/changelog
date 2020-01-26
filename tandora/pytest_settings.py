from .settings import *

TESTING = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
