"""
Django settings for LibertyNET project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(os.path.dirname(__file__))
#PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = SETTINGS_DIR
#PROJECT_PATH = os.path.abspath(PROJECT_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!l9x6@yxzmwtfhx@i3p%e-$9g)#l$d9r&7fqbo1da294@58^(e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'Client',
    'Common',
    'Employee',
    'Equipment',
    'Site',
    'Vendor',
    'Work',
    'south',
    'bootstrap3',
    'bootstrap_toolkit',
    'LibertyNET',
    'PIL',
    'dajaxice',
    'dajax',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

ROOT_URLCONF = 'LibertyNET.urls'

WSGI_APPLICATION = 'LibertyNET.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'LibertyNET12',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

TIME_INPUT_FORMATS = (
    '%H:%M',
)

DATE_INPUT_FORMATS = (
    '%Y-%m-%d',
)

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/common/login/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#Directory string
DIRECTORY_STRING = '/Users/taiowawaner/Documents/LibertyNET/LibertyNetProject/LibertyNET/'


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = '/Users/taiowawaner/Documents/LibertyNET/Django Projects/LibertySecurity/liberty/static/media/'
MEDIA_ROOT_PATH = os.path.join(PROJECT_PATH, 'static/media/')
MEDIA_ROOT = (
    #DIRECTORY_STRING + 'static/media/'
    MEDIA_ROOT_PATH
)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'static/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/static/'

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

STATICFILES_DIRS_PATH = os.path.join(PROJECT_PATH, 'static')
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #DIRECTORY_STRING + 'static',
    #os.path.join(PROJECT_DIR), 'static',
    STATICFILES_DIRS_PATH,
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates/')
TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

DAJAXICE_MEDIA_PREFIX = "dajaxice"

SOUTH_TESTS_MIGRATE = False