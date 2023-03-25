from pathlib import Path
from environs import Env
import os

# Initialize enviornment variables
env = Env()
env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.str("DEBUG", default=False)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    # Local
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
    "menu.apps.MenuConfig",
    "cart.apps.CartConfig",
    "orders.apps.OrdersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "orders.request_object.RequestObjectMiddleware",
]

ROOT_URLCONF = "restaurant_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.get_restaurant",
                "accounts.context_processors.get_user_profile",
                "accounts.context_processors.get_google_api_key",
                "accounts.context_processors.get_paypal_client_id",
                "cart.context_processors.get_cart_counter",
                "cart.context_processors.get_cart_amounts",
            ],
        },
    },
]

WSGI_APPLICATION = "restaurant_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.postgresql",
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env.str("DATABASE_NAME"),
        "PORT": env.int("DATABASE_PORT"),
        "HOST": env.str("DATABASE_HOST"),
        "USER": env.str("DATABASE_USER"),
        "PASSWORD": env.str("DATABASE_PASSWORD"),
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

TIME_ZONE = "Asia/Karachi"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Register Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Change error message tag to danger
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_USE_TLS = True
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "FoodOnline MarketPlace"

# Google API Key
GOOGLE_API_KEY = env.str("GOOGLE_API_KEY")

# GDAL Configurations
os.environ["PATH"] = (
    os.path.join(BASE_DIR, "env\Lib\site-packages\osgeo") + ";" + os.environ["PATH"]
)
os.environ["PROJ_LIB"] = (
    os.path.join(BASE_DIR, "env\Lib\site-packages\osgeo\data\proj")
    + ";"
    + os.environ["PATH"]
)
GDAL_LIBRARY_PATH = os.path.join(BASE_DIR, "env\Lib\site-packages\osgeo\gdal304.dll")


# PayPal
PAYPAL_CLIENT_ID = env.str("PAYPAL_CLIENT_ID")
# To unblock popups
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"


# Security Settings
# Security Settings
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=2592000)  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
