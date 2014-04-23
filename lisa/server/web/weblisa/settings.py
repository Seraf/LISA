# Django settings for blog project.
import os, json
from lisa.server.service import configuration
APP_DIR = os.path.dirname( globals()['__file__'] )
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__) + '/../')
LISA_PATH = os.path.abspath(os.path.dirname(__file__) + '../../../')

if os.path.exists('/etc/lisa/server/configuration/lisa.json'):
    configuration = json.load(open('/etc/lisa/server/configuration/lisa.json'))

DBNAME = 'lisa'

from mongoengine import connect
connect(DBNAME, host=configuration['database']['server'], port=configuration['database']['port'])

LOGIN_REDIRECT_URL='/'
LOGIN_URL='login'
LOGOUT_URL='logout'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Julien Syx', 'julien.syx@lisa-project.net'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.

    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/upload/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"


STATIC_ROOT = LISA_PATH + '/web/interface/static'


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@5dpi3h(s-s$**o9jimdh5@vth4ax5q3+h79rl0b1n(xp9r&amp;f-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'web.lisa.utils.loaders.AbsolutePath.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

ROOT_URLCONF = 'lisa.server.web.weblisa.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'lisa.server.web.weblisa.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'ENABLE_STACKTRACES' : True,
    }
INSTALLED_APPS = (
    'django.contrib.auth',
    'mongoengine.django.mongo_auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'tastypie',
    'tastypie_mongoengine',
    'tastypie_swagger',
    'interface',
    'manageplugins',
    'googlespeech',
)

# Sequence for each optional app as a dict containing info about the app.
OPTIONAL_APPS = (
    {"import": "debug_toolbar", "apps": ("debug_toolbar",),
        "middleware": ("debug_toolbar.middleware.DebugToolbarMiddleware",)},
)

# Set up each optional app if available.
for app in OPTIONAL_APPS:
    if app.get("condition", True):
        try:
            __import__(app["import"])
        except ImportError:
            pass
        else:
            INSTALLED_APPS += app.get("apps", ())
            MIDDLEWARE_CLASSES += app.get("middleware", ())


AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
TASTYPIE_SWAGGER_API_MODULE = 'lisa.server.web.weblisa.urls.v1_api'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
