import os
from datetime import timedelta
from pathlib import Path
from configurations import Configuration
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class CommonConfig(Configuration):
    # Application definition

    INSTALLED_APPS = [
        "whitenoise.runserver_nostatic",
        "admin_interface",
        "colorfield",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "cloudinary_storage",
        "django.contrib.staticfiles",
        "cloudinary",
        "core.apps.CoreConfig",
        "customauth.apps.CustomauthConfig",
        "rest_framework",
        "rest_framework.authtoken",
        "dj_rest_auth",
        "corsheaders",
        "django.contrib.sites",
        "allauth",
        "allauth.account",
        "allauth.socialaccount",
        "dj_rest_auth.registration",
        "allauth.socialaccount.providers.github",
        "drf_spectacular",
        "django_nose",
    ]

    X_FRAME_OPTIONS = "SAMEORIGIN"
    SILENCED_SYSTEM_CHECKS = ["security.W019"]

    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.environ.get("CLOUDINARY_NAME"),
        "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
        "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
    }

    SOCIAL_ACCOUNT_PROVIDERS = {
        "github": {
            "SCOPE": [
                "user",
                "repo",
                "read:org",
            ],
        },
    }

    SOCIALACCOUNT_LOGIN_ON_GET = True

    SITE_ID = 2

    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "backend.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
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

    WSGI_APPLICATION = "backend.wsgi.application"

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

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    STATIC_URL = "static/"

    REST_AUTH = {
        "SESSION_LOGIN": False,
        "USE_JWT": True,
        "JWT_AUTH_COOKIE": "access_token",
        "JWT_AUTH_HTTPONLY": False,
    }

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_AUTHENTICATION_METHOD = "email"

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.environ.get("EMAIL_PORT")

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework.authentication.TokenAuthentication",
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }

    SPECTACULAR_SETTINGS = {
        "TITLE": "Going-Once",
        "DESCRIPTION": "E-Commerce Auction Site",
        "VERSION": "1.0.0",
        "SERVE_INCLUDE_SCHEMA": False,
        # 'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
        # 'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
        # 'REDOC_DIST': 'SIDECAR',
        "SERVE_PUBLIC": True,
        # OTHER SETTINGS
    }

    # Use nose to run all tests
    TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

    # Tell nose to measure coverage on the 'foo' and 'bar' apps
    NOSE_ARGS = [
        "--with-coverage",
        "--cover-package=core",
    ]

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=600),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
        "ROTATE_REFRESH_TOKENS": False,
        "BLACKLIST_AFTER_ROTATION": False,
        "UPDATE_LAST_LOGIN": False,
        "ALGORITHM": "HS256",
        "SIGNING_KEY": os.environ.get("SECRET_KEY"),
        "VERIFYING_KEY": "",
        "AUDIENCE": None,
        "ISSUER": None,
        "JSON_ENCODER": None,
        "JWK_URL": None,
        "LEEWAY": 0,
        "AUTH_HEADER_TYPES": ("Bearer",),
        "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
        "USER_ID_FIELD": "id",
        "USER_ID_CLAIM": "user_id",
        "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
        "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
        "TOKEN_TYPE_CLAIM": "token_type",
        "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
        "JTI_CLAIM": "jti",
        "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
        "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
        "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
        "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
        "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
        "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
        "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
        "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
        "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
    }

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    SESSION_COOKIE_SECURE = False

    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = "/login"

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

    MEDIA_URL = "/media/"

    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

    STATIC_ROOT = BASE_DIR / "staticfiles"


    # WHITENOISE_MANIFEST_STRICT = True

    AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

    AUTH_USER_MODEL = "customauth.User"

    CELERY_ACCEPT_CONTENT = ["application/json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = "UTC"

    CELERY_BEAT_SCHEDULE = {
        "check_expired_items": {
            "task": "core.tasks.check_expired_items",
            "schedule": timedelta(minutes=30),
        },
    }


class DevConfig(CommonConfig):
    SECRET_KEY = os.environ.get("DEV_SECRET_KEY")

    DEBUG = True

    # DEBUG_PROPAGATE_EXCEPTIONS = True

    ALLOWED_HOSTS = ["*"]

    DATABASES = {
        "default": dj_database_url.config(default="sqlite:///db.sqlite3"),
    }

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ]

    # CORS_ALLOW_ALL_ORIGINS: True

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = os.environ.get("DEV_EMAIL_HOST")
    EMAIL_HOST_USER = os.environ.get("DEV_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("DEV_EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.environ.get("DEV_EMAIL_PORT")

    REDIS_URL = os.environ.get("DEV_REDIS_URL")

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL


class ProdConfig(CommonConfig):
    SECRET_KEY = os.environ.get("PROD_SECRET_KEY")

    DEBUG = False

    DEBUG_PROPAGATE_EXCEPTIONS = True

    ALLOWED_HOSTS = ["*"]

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ]

    # CORS_ALLOW_ALL_ORIGINS: True

    DATABASES = {
        "default": dj_database_url.config(default=os.environ.get("POSTGRES_URI")),
    }

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = os.environ.get("PROD_EMAIL_HOST")
    EMAIL_HOST_USER = os.environ.get("PROD_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("PROD_EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.environ.get("PROD_EMAIL_PORT")

    REDIS_URL = os.environ.get("PROD_REDIS_URL")

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
