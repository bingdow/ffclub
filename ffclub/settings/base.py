# -*- coding: utf-8 -*-

# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

# Django settings file for a project based on the playdoh template.
# import * into your settings_local.py
import logging
import os
import socket
import djcelery

from django.utils.functional import lazy

from funfactory.manage import ROOT, path
from jinja2.environment import DEFAULT_FILTERS
from ffclub.person.utils import blackout_name, blackout_email


# Name of the top-level module where you put all your apps.
# If you did not install Playdoh with the funfactory installer script
# you may need to edit this value. See the docs about installing from a
# clone.

PROJECT_MODULE = 'ffclub'

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE


# For backwards compatability, (projects built based on cloning playdoh)
# we still have to have a ROOT_URLCONF.
# For new-style playdoh projects this will be overridden automatically
# by the new installer

# Is this a dev instance?
DEV = False

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

DATABASES = {}  # See settings_local.

SLAVE_DATABASES = []

# DATABASE_ROUTERS = ('multidb.PinningMasterSlaveRouter',)

# Site ID is used by Django's Sites framework.
SITE_ID = 1

## Logging
LOG_LEVEL = logging.INFO
HAS_SYSLOG = True
SYSLOG_TAG = "http_app_playdoh"  # Change this after you fork.
LOGGING_CONFIG = None
LOGGING = {
}

# CEF Logging
CEF_PRODUCT = 'Playdoh'
CEF_VENDOR = 'Mozilla'
CEF_VERSION = '0'
CEF_DEVICE_VERSION = '0'


## Internationalization.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Taipei'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Gettext text domain
TEXT_DOMAIN = 'messages'
STANDALONE_DOMAINS = [TEXT_DOMAIN, 'javascript']
TOWER_KEYWORDS = {'_lazy': None}
TOWER_ADD_HEADERS = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-TW'

## Accepted locales

# Tells the product_details module where to find our local JSON files.
# This ultimately controls how LANGUAGES are constructed.
PROD_DETAILS_DIR = path('lib/product_details_json')

# On dev instances, the list of accepted locales defaults to the contents of
# the `locale` directory within a project module or, for older Playdoh apps,
# the root locale directory.  A localizer can add their locale in the l10n
# repository (copy of which is checked out into `locale`) in order to start
# testing the localization on the dev server.
import glob
import itertools

try:
    DEV_LANGUAGES = [
        os.path.basename(loc).replace('_', '-')
        for loc in itertools.chain(glob.iglob(ROOT + '/locale/*'), # old style
                                   glob.iglob(ROOT + '/*/locale/*'))
        if (os.path.isdir(loc) and os.path.basename(loc) != 'templates')
    ]
except OSError:
    DEV_LANGUAGES = ('en-US',)

# On stage/prod, the list of accepted locales is manually maintained.  Only
# locales whose localizers have signed off on their work should be listed here.
PROD_LANGUAGES = (
    'zh-TW',
)


def lazy_lang_url_map():
    from django.conf import settings

    langs = settings.DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    return dict([(i.lower(), i) for i in langs])


LANGUAGE_URL_MAP = lazy(lazy_lang_url_map, dict)()


# Override Django's built-in with our native names
def lazy_langs():
    from django.conf import settings
    from product_details import product_details

    langs = DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    return dict([(lang.lower(), product_details.languages[lang]['native'])
                 for lang in langs if lang in product_details.languages])


LANGUAGES = lazy(lazy_langs, dict)()

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS = {
    'messages': [
        # Searching apps dirs only exists for historic playdoh apps.
        # See playdoh's base settings for how message paths are set.
        ('apps/**.py',
         'tower.management.commands.extract.extract_tower_python'),
        ('apps/**/templates/**.html',
         'tower.management.commands.extract.extract_tower_template'),
        ('templates/**.html',
         'tower.management.commands.extract.extract_tower_template'),
        ('%s/**.py' % PROJECT_MODULE,
         'tower.management.commands.extract.extract_tower_python'),
        ('%s/**/templates/**.html' % PROJECT_MODULE,
         'tower.management.commands.extract.extract_tower_template'),
        ('templates/**.html',
         'tower.management.commands.extract.extract_tower_template'),
    ],
}

# Paths that don't require a locale code in the URL.
SUPPORTED_NONLOCALES = ['media', 'static', 'admin']


## Media and templates.

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
# Set this in your local settings which is not committed to version control.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'session_csrf.context_processor',
    'django.contrib.messages.context_processors.messages',
    # 'funfactory.context_processors.i18n',
    # 'funfactory.context_processors.globals',
    'jingo_minify.helpers.build_ids',
    'django_browserid.context_processors.browserid_form',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_login_redirect',
    'ffclub.base.context_processors.constants',
)


def get_template_context_processors(exclude=(), append=(),
                                    current={'processors': TEMPLATE_CONTEXT_PROCESSORS}):
    """
    Returns TEMPLATE_CONTEXT_PROCESSORS without the processors listed in
    exclude and with the processors listed in append.

    The use of a mutable dict is intentional, in order to preserve the state of
    the TEMPLATE_CONTEXT_PROCESSORS tuple across multiple settings files.
    """

    current['processors'] = tuple(
        [p for p in current['processors'] if p not in exclude]
    ) + tuple(append)

    return current['processors']


TEMPLATE_DIRS = (
    path('templates'),
)

# Storage of static files
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
)
COMPRESS_PRECOMPILERS = (
    #('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
    #('text/x-sass', 'sass {infile} {outfile}'),
    #('text/x-scss', 'sass --scss {infile} {outfile}'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


def JINJA_CONFIG():
    #    from caching.base import cache
    config = {'extensions': ['tower.template.i18n', 'jinja2.ext.do',
                             'jinja2.ext.with_', 'jinja2.ext.loopcontrols'],
              'finalize': lambda x: x if x is not None else ''}
    #    if 'memcached' in cache.scheme and not settings.DEBUG:
    # We're passing the _cache object directly to jinja because
    # Django can't store binary directly; it enforces unicode on it.
    # Details: http://jinja.pocoo.org/2/documentation/api#bytecode-cache
    # and in the errors you get when you try it the other way.
    #        bc = jinja2.MemcachedBytecodeCache(cache._cache,
    #                                           "%sj2:" % settings.CACHE_PREFIX)
    #        config['cache_size'] = -1 # Never clear the cache
    #        config['bytecode_cache'] = bc
    return config


## Middlewares, apps, URL configs.

MIDDLEWARE_CLASSES = (
    # 'funfactory.middleware.LocaleURLMiddleware',
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'ffclub.base.middleware.BrowserDetectionMiddleware',
    'multidb.middleware.PinningRouterMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_csrf.CsrfMiddleware', # Must be after auth middleware.
    'django.contrib.messages.middleware.MessageMiddleware',
    'commonware.middleware.FrameOptionsHeader',
    'mobility.middleware.DetectMobileMiddleware',
    'mobility.middleware.XMobileMiddleware',
    'ffclub.base.middleware.UserFullnameMiddleware',
    'ffclub.base.middleware.LoggingMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
)


def get_middleware(exclude=(), append=(),
                   current={'middleware': MIDDLEWARE_CLASSES}):
    """
    Returns MIDDLEWARE_CLASSES without the middlewares listed in exclude and
    with the middlewares listed in append.

    The use of a mutable dict is intentional, in order to preserve the state of
    the MIDDLEWARE_CLASSES tuple across multiple settings files.
    """

    current['middleware'] = tuple(
        [m for m in current['middleware'] if m not in exclude]
    ) + tuple(append)
    return current['middleware']


INSTALLED_APPS = (
    # Web server
    'gunicorn',
    # Local apps
    'funfactory', # Content common to most playdoh-based apps.
    'jingo_minify',

    # 'compressor',

    'tower', # for ./manage.py extract (L10n)
    'cronjobs', # for ./manage.py cron * cmd line tasks
    'django_browserid',
    'social_auth',

    # Django contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'django.contrib.admin',

    # Application base, containing global templates.
    'sandstone',
    '%s.base' % PROJECT_MODULE,
    '%s.upload' % PROJECT_MODULE,
    '%s.intro' % PROJECT_MODULE,
    '%s.person' % PROJECT_MODULE,
    '%s.product' % PROJECT_MODULE,
    '%s.event' % PROJECT_MODULE,
    '%s.newsletter' % PROJECT_MODULE,
    '%s.event.templatetags' % PROJECT_MODULE,

    # Third-party apps, patches, fixes
    'commonware.response.cookies',
    'djcelery',
    'kombu.transport.django',
    'django_nose',
    'session_csrf',
    'south',

    # L10n
    'product_details',

    # 'raven.contrib.django.raven_compat',
)


def get_apps(exclude=(), append=(), current={'apps': INSTALLED_APPS}):
    """
    Returns INSTALLED_APPS without the apps listed in exclude and with the apps
    listed in append.

    The use of a mutable dict is intentional, in order to preserve the state of
    the INSTALLED_APPS tuple across multiple settings files.
    """

    current['apps'] = tuple(
        [a for a in current['apps'] if a not in exclude]
    ) + tuple(append)
    return current['apps']

# Path to Java. Used for compress_assets.
# JAVA_BIN = '/usr/bin/java'

# Sessions
#
# By default, be at least somewhat secure with our session cookies.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

## Auth
# The first hasher in this list will be used for new passwords.
# Any other hasher in the list can be used for existing passwords.
# Playdoh ships with Bcrypt+HMAC by default because it's the most secure.
# To use bcrypt, fill in a secret HMAC key in your local settings.
BASE_PASSWORD_HASHERS = (
    'django_sha2.hashers.BcryptHMACCombinedPasswordVerifier',
    'django_sha2.hashers.SHA512PasswordHasher',
    'django_sha2.hashers.SHA256PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)
HMAC_KEYS = {# for bcrypt only
    #'2012-06-06': 'cheesecake',
}

from django_sha2 import get_password_hashers

PASSWORD_HASHERS = get_password_hashers(BASE_PASSWORD_HASHERS, HMAC_KEYS)

## Tests
TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'

## Celery

djcelery.setup_loader()

BROKER_URL = 'django://localhost//'

# CELERY_IMPORTS = ('ffclub.product.tasks',)

# True says to simulate background tasks without actually using celeryd.
# Good for local development in case celeryd is not running.
CELERY_ALWAYS_EAGER = False

BROKER_CONNECTION_TIMEOUT = 0.1
CELERY_RESULT_BACKEND = 'database'
# CELERY_RESULT_DBURI = "mysql://root:root@localhost:3306"
CELERY_IGNORE_RESULT = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# CELERY_ANNOTATIONS = {"tasks.add": {"rate_limit": "10/s"}}
# Time in seconds before celery.exceptions.SoftTimeLimitExceeded is raised.
# The task can catch that and recover but should exit ASAP.
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 2

## Arecibo
# when ARECIBO_SERVER_URL is set, it can use celery or the regular wrapper
ARECIBO_USES_CELERY = True

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# For absolute urls
try:
    DOMAIN = socket.gethostname()
except socket.error:
    DOMAIN = 'localhost'
PROTOCOL = "http://"
PORT = 80

## django-mobility
MOBILE_COOKIE = 'mobile'

LOCALE_PATHS = (
    os.path.join(ROOT, PROJECT_MODULE, 'locale'),
)

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'sitemap.xml',
    'admin',
    'registration',
    'browserid',
]

# AUTH_USER_MODEL = "ffclub.person.models.CustomUser"
AUTH_PROFILE_MODULE = "person.Person"

# BrowserID configuration
AUTHENTICATION_BACKENDS = [
    'django_browserid.auth.BrowserIDBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# SITE_URL = 'http://127.0.0.1:8000'
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = 'login.redirect'
LOGIN_REDIRECT_URL_FAILURE = 'login.redirect'

# Should robots.txt deny everything or disallow a calculated list of URLs we
# don't want to be crawled?  Default is false, disallow everything.
# Also see http://www.google.com/support/webmasters/bin/answer.py?answer=93710
ENGAGE_ROBOTS = False

# Always generate a CSRF token for anonymous users.
ANON_ALWAYS = True

CSRF_FAILURE_VIEW = 'ffclub.base.views.csrf_failure'
# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# jingo-minify settings
MINIFY_BUNDLES = {
    'css': {
        # 'site' is automatically included across whole site
        'site': (
            'css/normalize.css',
            'css/sandstone/tabzilla.less.css',
            'css/sandstone/navigator.less.css',
            'css/sandstone/footer.less.css',
            'css/persona-buttons.css',
            'css/slides.css',
            # imported using less
            # 'css/ffcstyle.css',
        ),
        'admin': (
            'css/admin/login.less',
            'css/admin/activity_forms.less',
        ),
        'base': (
            'css/base.less',
        ),
        'tos': (
            'css/tos.less',
        ),
        'intro': (
            'css/intro.less',
        ),
        # 'person': (
        # ),
        'register': (
            'css/register.less',
        ),
        'register.complete': (
            'css/register.complete.less',
        ),
        'order.complete': (
            'css/order.complete.less',
        ),
        'order.verify': (
            'css/order.verify.less',
        ),
        'event': (
            'css/event.less',
        ),
        'event_photo': (
            'css/event_photo.less',
        ),
        'event_register': (
            'css/event_register.less',
        ),
        'campaign_claim_award': (
            'css/campaign_claim_award.less',
        ),
        'product': (
            'css/product.less',
        ),
        'product_photos': (
            'css/product_photos.less',
        ),
        'error': (
            'css/error.less',
        ),
        'attack-on-web': (
            'css/event/attack-on-web.less',
        ),
        'applyform': (
            'css/event/3904611051-formview_ltr.css',
            'css/event/722395648-mobile_formview_ltr.css',
        ),
        'coming-soon': (
            'css/event/coming-soon.less',        
        ),
        'film': (
            'css/event/film.less',
        ),
        'every-moment': (
            'css/event/every-moment.less',
        ),
        'every-moment-upload': (
            'css/event/every-moment-upload.less',
        ),
        'every-moment-wall': (
            'css/libs/jquery-ui-1.10.3.custom.css',
            'css/event/every-moment-wall.less',
        ),
        'every-moment-photo': (
            'css/event/every-moment-photo.less',
        ),
        'every-moment-exceed': (
            'css/event/every-moment-exceed.less',
        ),
        'every-moment-result': (
            'css/event/every-moment-result.less',
        ),
        'microfilm-vote':{
            'css/event/microfilm-vote.less'
        },
        'demo':{
            'css/event/demo.less',
            'https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css'
        },
        'yaml':{
            'css/event/yaml/core/base.min.css',
            'css/event/yaml/forms/gray-theme.css',        
        }
    },
    'js': {
        # 'site' is automatically included across whole site
        'site': (
            'js/libs/jquery-1.9.1.js',
            'js/global.js',
            'js/sandstone/sandstone-tabzilla-nav-all.js',
            'js/main.js',
            'js/slides.js',
        ),
        'browserid': (
            'js/browserid.js',
            'https://browserid.org/include.js',
        ),
        # 'base': (
        # ),
        'intro': (
            'js/intro.js',
        ),
        # 'person': (
        # ),
        'event': (
            'js/libs/jquery.masonry.min.js',
            'js/libs/jquery.imagesloaded.min.js',
            'js/libs/jquery.infinitescroll.js',
            'js/pretty.date.js',
            'js/event.js',
            'js/fb-share.js',
        ),
        'product': (
            'js/product.js',
        ),
        'attack-on-web': (
            'js/main.js',
            'js/event/attack-on-web.js',
        ),
        'applyform': (
            'js/event/3661387036-formviewer_prd__zh_tw.js',
        ),
        'coming-soon': (
            'js/event/coming-soon.js',
        ),
        'every-moment': (
            'js/libs/jquery.scrollTo.js',
            'js/libs/jquery.localScroll.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/libs/jquery.pageslide.min.js',
            'js/libs/tweenmax.1.9.7.min.js',
            'js/libs/superscrollorama-1.0.1.js',
            'js/libs/jquery.plusslider.js',
            'js/libs/jquery.color.js',
            'js/libs/script.js',
            # 'js/libs/socialshare.min.js',
            'js/event/every-moment.js',
        ),
        'every-moment-upload': (
            'js/libs/jquery-ui.js',
            'js/libs/exif.js',
            'js/libs/binaryajax.js',
            'js/event/every-moment-upload.js',
            'js/fb-share.js',
        ),
        'every-moment-wall': (
            'js/libs/jquery-ui.js',
            'js/libs/jquery.masonry.min.js',
            'js/libs/jquery.imagesloaded.min.js',
            'js/libs/jquery.infinitescroll.js',
            'js/event/every-moment-wall.js',
        ),
        'microfilm-vote':{
            'js/main.js',
            'js/event/microfilm-vote.js'
        },
        'demo':{
            'js/event/demo.js'
        }
    }
}

LESS_PREPROCESS = True
# LESS_BIN = '/usr/local/bin/lessc'


# Cache
# some johnny settings
CACHES = {
    'default': {
        'BACKEND': 'johnny.backends.memcached.PyLibMCCache',
        'LOCATION': ['127.0.0.1:11211'],
        'JOHNNY_CACHE': True,
    }
}
JOHNNY_MIDDLEWARE_KEY_PREFIX='ffclub'



CUSTOM_PRODUCT_KEYWORDS = {
    '1': u'Firefox 宣傳品, Firefox 推廣物, Firefox 貼紙, Firefox sticker, Firefox 酷炫貼紙, Firefox 推廣貼紙, Firefox 衍生物, Firefox 輔銷品',
    '2': u'Firefox 宣傳品, Firefox 推廣物, Firefox 明信片, Firefox postcard,  Firefox 衍生物, Firefox 贈品, Firefox 輔銷品',
    '3': u'Firefox 宣傳品, Firefox 推廣物, Firefox 海報, Firefox poster,  Firefox 衍生物, Firefox 贈品, Firefox 輔銷品',
    '4': u'Firefox 宣傳品, Firefox 推廣物, Firefox 型錄, Firefox catalogue,  Firefox 衍生物, Firefox 贈品, Firefox 輔銷品',
}

CUSTOM_ORDER_DETAIL_CHOICES = {
    1: ((0, '0張'), (10, '10張'), (20, '20張'), (30, '30張')),
    2: ((0, '0張'), (10, '10張'), (20, '20張'), (30, '30張')),
    3: ((0, '0張'), (1, '1張'), (2, '2張'), (3, '3張')),
    4: ((0, '0份'), (5, '5份'), (10, '10份')),
}

ALL_ORDER_DETAIL_CHOICES = []
for product_id in CUSTOM_ORDER_DETAIL_CHOICES:
    for choice in CUSTOM_ORDER_DETAIL_CHOICES[product_id]:
        (value, label) = choice
        defaultChoice = (value, value)
        if defaultChoice not in ALL_ORDER_DETAIL_CHOICES:
            ALL_ORDER_DETAIL_CHOICES.append(defaultChoice)
ALL_ORDER_DETAIL_CHOICES = tuple(ALL_ORDER_DETAIL_CHOICES)

PRODUCT_INVENTORY_SHEET_NAME = u'Inventory_B'
PRODUCT_INVENTORY_QTY_ROW_NAME = u'Current Qty'
PRODUCT_INVENTORY_MAPPING = {
    u'A5貼紙': 1,
    u'B2G DM': 2,
    u'釋出週期海報': 3,
    u'宣傳小冊子Brochur': 4,
}

EVENT_WALL_PHOTOS_PER_PAGE = 15

FB_APP_ID = 'DUMMY_APP_ID'
FB_APP_SECRET = 'DUMMY_APP_SECRET'

PRODUCT_INVENTORY_PATH = u'/Users/yshlin/Desktop/2013 宣傳品庫存.xlsx'
PRODUCT_INVENTORY_MIN = 50
SUBSCRIBER_EMAILS_PATH = 'subscribers.txt'

FILE_PATH = 'uploads/'


# Uncomment this and set to all slave DBs in use on the site.
# SLAVE_DATABASES = ['slave']

DEFAULT_FROM_EMAIL = 'no-reply@mozilla.com.tw'
DEFAULT_REPLY_EMAIL = 'no-reply@mozilla.com'
DEFAULT_NOTIFY_EMAIL = ('no-reply@mozilla.com',)

EMAIL_HOST = 'mail.mozilla.com.tw'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'moz2000tw'
# EMAIL_HOST_PASSWORD = 'mozillaNEW2013'
EMAIL_USE_TLS = True

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'http://74876894ee994abcad98819694957f2f:bc278ae9652b43e19857089446fa74ba@sentry.inspire.mozilla.com.tw:9000/2',
}

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

SHARE_FILE_PATH = 'share/'

API_SECRET = 'hush'

DEFAULT_FILTERS['blackout_name'] = blackout_name
DEFAULT_FILTERS['blackout_email'] = blackout_email
