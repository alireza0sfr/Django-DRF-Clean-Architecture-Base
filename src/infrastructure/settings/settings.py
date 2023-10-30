"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from datetime import datetime
from datetime import timedelta
from pathlib import Path

from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "corsheaders",
    "django_celery_beat",
    # Authentication
    "rest_framework_simplejwt",
    "djoser",
    # Apps
    ## Django apps will be auto registered!
]

APPS_DIRECTORY = "domain/apps"

for app_path in (BASE_DIR / APPS_DIRECTORY).iterdir():
    # Check if it's a directory and contains an 'apps.py' file
    if app_path.is_dir() and (app_path / "apps.py").exists():
        app = app_path.relative_to(BASE_DIR).as_posix().replace("/", ".")
        INSTALLED_APPS.append(app)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "infrastructure.middlewares.ban.BanMiddleware",
]

ROOT_URLCONF = "presentation.api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "presentation/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "infrastructure.server.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", cast=int),
        "CONN_HEALTH_CHECKS": True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "presentation/static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "presentation/media"

STATICFILES_DIRS = [BASE_DIR / "presentation/staticfiles"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "presentation.renderers.camelize_renderer.CamelizeRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        # Any other renders
    ),
    "DEFAULT_PARSER_CLASSES": (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        # Any other parsers
    ),
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "infrastructure.exceptions.custom_handlers.custom_exception_handler",
}

# Authentication
DJOSER = {
    "HIDE_USERS": True,
    "LOGIN_ON_REGISTER": True,
    "LOGIN_FIELD": "username",
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "USER_CREATE_PASSWORD_RETYPE": False,
    "SET_USERNAME_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "USERNAME_RESET_CONFIRM_RETYPE": True,
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "PASSWORD_RESET_CONFIRM_URL": "frontend-url-for-password-change/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "frontend-url-for-username-change/{uid}/{token}",
    "SERIALIZERS": {
        "activation": "infrastructure.serializers.identity.serializers.IdTokenSerializer",
        "password_reset_confirm": "infrastructure.serializers.identity.serializers.PasswordResetConfirmSerializer",
        "password_reset_confirm_retype": "infrastructure.serializers.identity.serializers.PasswordResetRetypeConfirmSerializer",
        "user": "infrastructure.serializers.identity.serializers.UserModelSerializer",
        "current_user": "infrastructure.serializers.identity.serializers.UserModelSerializer",
        "user_create": "infrastructure.serializers.identity.serializers.UserRegisterSerializer",
    },
    "PERMISSIONS": {
        "activation": ["application.permissions.permissions.CurrentUserOrAdmin"],
        "password_reset": ["application.permissions.permissions.CurrentUserOrAdmin"],
        "password_reset_confirm": [
            "application.permissions.permissions.CurrentUserOrAdmin"
        ],
        "set_password": ["application.permissions.permissions.CurrentUserOrAdmin"],
        "username_reset": ["application.permissions.permissions.CurrentUserOrAdmin"],
        "username_reset_confirm": [
            "application.permissions.permissions.CurrentUserOrAdmin"
        ],
        "set_username": ["application.permissions.permissions.CurrentUserOrAdmin"],
        "user_create": ["rest_framework.permissions.AllowAny"],
        "user_delete": ["application.permissions.permissions.CurrentUserOrAdmin"],
        "user": ["application.permissions.permissions.CurrentUserOrAdmin"],
        "user_list": ["rest_framework.permissions.AllowAny"],
    },
}

# Jwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "TOKEN_OBTAIN_SERIALIZER": "infrastructure.serializers.identity.serializers.TokenObtainPairSerializer",
}

# Authentication
AUTH_USER_MODEL = "identity.User"

# DRF spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Django-DRF-Clean-Architecture-Base",
    "DESCRIPTION": "Lorem",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9].[0-9]/",
    "SERVE_PERMISSIONS": ["application.permissions.permissions.IsAdminUser"],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
}

# Logging

# Create the "logs" directory if it doesn't exist
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} | {asctime} | {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": config("CONSOLE_LOG_LEVEL"),
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": config("FILE_LOG_LEVEL"),
            "class": "logging.FileHandler",
            "filename": Path(LOGS_DIR)
            / f'{config("APP_NAME")}-{datetime.now():%Y-%m-%d}.log',
            "formatter": "verbose",
        },
        "seq": {
            "level": config("SEQ_LOG_LEVEL"),
            "class": "seqlog.SeqLogHandler",
            "server_url": "http://seq:5341",
        },
    },
    "root": {
        "handlers": config("LOG_HANDLERS", cast=Csv()),
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": config("LOG_HANDLERS", cast=Csv()),
            "level": config("CONSOLE_LOG_LEVEL"),
            "propagate": False,
        },
    },
}

# security configs for production
if not DEBUG:
    # Https settings
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # more security settings
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "SAMEORIGIN"
    SECURE_REFERRER_POLICY = "strict-origin"
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CORS
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:8080',
#     'http://localhost:8081'
# ]
CORS_ALLOW_ALL_ORIGINS = True

# Celery Configs
CELERY_BROKER_URL = "redis://redis:6379/1"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Email Configurations for production and development
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = False
    EMAIL_HOST = "smtp4dev"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 25
else:
    EMAIL_BACKEND = config(
        "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
    )
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    DEFAULT_FROM_EMAIL = config("EMAIL_DEFAULT_FROM_EMAIL")
