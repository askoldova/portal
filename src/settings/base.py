import os
from django.utils.translation import ugettext_lazy as _
from core import env, int_env, bool_env, list_env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ADMINS = (
    ('Andriy G', 'andriy.gushuley@gmail.com'),
)

DEFAULT_FROM_EMAIL = 'askoldova@andriydc.eu'

SERVER_EMAIL = DEFAULT_FROM_EMAIL
MANAGERS = ADMINS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', '-')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool_env('DJANGO_DEBUG_ENABLED', False)
ENABLE_MEDIA = DEBUG

ALLOWED_HOSTS = list_env('DJANGO_ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'filebrowser',
    'tinymce',

    'portal',
    'publications',
    'generation',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATES = (
    dict(
        BACKEND='django.template.backends.django.DjangoTemplates',
        DIRS=(
            os.path.join(BASE_DIR, "templates"),
        ),
        APP_DIRS=True,
        OPTIONS=dict(
            context_processors=(
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ),
        ),
    ),
)

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = dict(
    default=dict(
        ENGINE='django.db.backends.mysql',
        HOST=env('DJANGO_DATABASE_HOST', 'db.andriydc.eu'),
        NAME=env('DJANGO_DATABASE_NAME', 'askoldova'),
        USER=env('DJANGO_DATABASE_USER', 'askoldova'),
        PASSWORD=env('DJANGO_DATABASE_PASSWORD', None),
        PORT=env('DJANGO_DATABASE_PORT', None),
    )
)


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'uk-ua'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'htdocs')

MEDIA_URL = '/'

# === django sites configuration
SITE_ID = int_env('DJANGO_SITE_ID', 1)

# === django logging configuration
LOGGING = dict(
    version=1,
    disable_existing_loggers=False,
    handlers=dict(
        console={
            'class': 'logging.StreamHandler'
        },
    ),
    loggers=dict(
        django=dict(
            handlers=['console'],
            level=os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        ),
    ),
)

# === filebrowser configuration
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_DIRECTORY = ''

FILEBROWSER_VERSIONS = dict(
    fb=dict(verbose_name=_('Admin Thumbnail'), width=60, height=60, opts='crop'),
    smallIx=dict(verbose_name=_('Smaill index'), width=150, height=150, opts=''),
    smallIxCr=dict(verbose_name=_('Smaill index crop'), width=150, height=150, opts='crop'),
    galIx=dict(verbose_name=_('Gallery index'), width=200, height=200, opts=''),
    galIxCr=dict(verbose_name=_('Gallery index cropped'), width=200, height=200, opts='crop'),
    ix=dict(verbose_name=_('Index'), width=300, height=300, opts='upscale'),
    gallery=dict(verbose_name=_('Gallery item'), width=1024, height=800, opts=''),
)

FILEBROWSER_ADMIN_VERSIONS = ['smallIx', 'smallIxCr', 'ix', 'galIx', 'galIxCr', 'gallery']
FILEBROWSER_LIGHTBOX_VERSION = 'gallery'

FILEBROWSER_ADMIN_THUMBNAIL = 'fb'
FILEBROWSER_PREVIEW_VERSION = 'index'

# == Celery configuration
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'yaml']
CELERY_TASK_SERIALIZER = 'pickle'

# === tinymce configuration

TINYMCE_DEFAULT_CONFIG = dict(
    theme="advanced",
    mode="exact",
    plugins="safari,style,layer,table,save,advhr,advimage,advlink,inlinepopups,preview,media,searchreplace,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,",

    language="uk",

    # Theme options
    theme_advanced_buttons1="save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect,|,styleprops,spellchecker",
    theme_advanced_buttons2="cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor,|,visualchars,nonbreaking,template,blockquote,pagebreak",
    theme_advanced_buttons3="tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,insertlayer,moveforward,movebackward,absolute,|,fullscreen",
    theme_advanced_toolbar_location="top",
    theme_advanced_toolbar_align="left",
    theme_advanced_statusbar_location="bottom",
    theme_advanced_resizing=True,
    theme_advanced_styles='Left float=l;Right float=r;Left float + lightbox=ll;Right float + lightbox=rl;Lightbox=lb',

    content_css="/css/template.css",

    relative_urls=False,
    convert_urls=False,
)

TINYMCE_FILEBROWSER = True

# portal configuration

PORTAL_DEFAULT_REDIRECT_VIEW = 'pubs_all_publications'

REDIRECT_HTML_TIMEOUT = 30

FORCE_DISABLE_MEDIA = bool_env("DJANGO_DISABLE_MEDIA", False)