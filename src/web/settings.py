from pathlib import Path

from core.config import GlobalConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = GlobalConfig["secret_key"]

DEBUG = True

ALLOWED_HOSTS = GlobalConfig.get("allowed_hosts", [])

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'front'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'web.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

_db_backend = GlobalConfig.get('db_backend', 'mysql')
if _db_backend == 'mysql':
    if not (GlobalConfig.get('db_user') and GlobalConfig.get('db_password')):
        exit(f"Please provide sufficient MySQL connection params (user/password)")

    default_db = {
        'ENGINE': 'mysql.connector.django',
        'HOST': GlobalConfig.get('db_host', 'localhost'),
        'PORT': GlobalConfig.get('db_port', '3306'),
        'NAME': GlobalConfig['db_name'],
        'USER': GlobalConfig['db_user'],
        'PASSWORD': GlobalConfig['db_password'],
    }
elif _db_backend == 'sqlite3' or _db_backend == 'sqlite':
    default_db = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / GlobalConfig['db_name']
    }
else:
    exit(f"DB backend {_db_backend} is not supported")

DATABASES = {'default': default_db}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
