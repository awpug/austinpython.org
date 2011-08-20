import os

def map_path(directory_name):
    return os.path.join(os.path.dirname(__file__), directory_name).replace('\\', '/')

DEBUG = False
SERVE_STATIC_MEDIA = False
COMPRESS = True
TEMPLATE_DEBUG = DEBUG
MAINTENANCE_MODE = False

ADMINS = (
    ('', ''),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': map_path('bootstrap/austinpython.db'), # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

SESSION_COOKIE_NAME = 'awpug.org'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = map_path('static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

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
SECRET_KEY = '+2da+j)g)kdd^r)cate_sbdd201sa$i+9e1_5tg780wk4&o77h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.media.PlaceholderMediaMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
#    'maintenancemode.middleware.MaintenanceModeMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.media',
)

ROOT_URLCONF = 'awpug.urls'

TEMPLATE_DIRS = (
    map_path('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.redirects',
    'django.contrib.sitemaps',

    'appmedia',
    'cms',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'compressor',
    'filebrowser',
    'menus',
    'mptt',
    'robots',
#    'sorl.thumbnail',
    'south',
    'tinymce',
    'lib.widget_tweaks',
)

CMS_TEMPLATES = (
    ('home.html', 'Home'),
)

CMS_SEO_FIELDS = True
CMS_REDIRECTS = True

LANGUAGES = [
    ('en', 'English'),
]

TINYMCE_COMPRESSOR = True
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'table,template,paste,advlink,advimage',
    'theme': "advanced",
    'theme_advanced_blockformats' : 'p,div,pre,h1,h2,h3,h4,h5,h6,blockquote,dt,dd',
    'theme_advanced_toolbar_location' : 'bottom',
    'theme_advanced_toolbar_align' : 'left',
    'theme_advanced_buttons1' : 'bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,|,bullist,numlist,|,outdent,indent,|,styleselect,formatselect',
    'theme_advanced_buttons2' : 'link,unlink,|,anchor,image,|,cleanup,help,|,code,|,sub,sup,charmap,|,pasteword,removeformat',
    'theme_advanced_buttons3' : "template,|,tablecontrols",
    'extended_valid_elements' : 'iframe[*],section[*],article[*],header[*],aside[*],hgroup[*]',
#    'content_css' : '%scss/editor.css' % MEDIA_URL,
    'doctype' : '<!DOCTYPE html>',
    'element_format' : 'html',
    'fix_list_elements' : True,
    'forced_root_block' : False,
    'theme_advanced_styles' : '',
    'width': '100%',
    'height': '400',
    'verify_html' : True,
    'relative_urls' : False,
    'remove_script_host' : True,
    'template_external_list_url' : '/admin/tinymce/templates/'
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

FILEBROWSER_URL_WWW = '/static/uploads'
FILEBROWSER_URL_FILEBROWSER_MEDIA = '/static/filebrowser/'
FILEBROWSER_PATH_MEDIA = os.path.join(MEDIA_ROOT, 'filebrowser/')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

try:
    from local_settings import *
except ImportError:
    pass
