from .base import *

DEBUG = True

ALLOWED_HOSTS += ['192.168.1.194']

INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

TEMPLATES[0]['OPTIONS']['loaders'] = [
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader"
                ]


##### Database #####
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_ROOT = BASE_DIR / 'static-files'

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # Console print