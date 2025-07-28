from pathlib import Path
from decouple import config
import dj_database_url
import os
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Secret key & debug
SECRET_KEY = config("SECRET_KEY", default="unsafe-dev-key")
DEBUG = config("DEBUG", default=False, cast=bool)

# ✅ Allowed hosts
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
    "0.0.0.0",
    "portfolio-backend-2s7t.onrender.com",  # 🔁 update if using Fly.io or custom domain
]

# ✅ Installed apps
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",

    # Your app
    "core",
]

# ✅ Middleware
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

ROOT_URLCONF = "portfolio_backend.urls"

# ✅ Templates
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

WSGI_APPLICATION = "portfolio_backend.wsgi.application"

# ✅ Database (Neon)
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# ✅ Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ✅ Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ✅ Static files (served via Whitenoise in production)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ✅ Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ✅ Email (Brevo)
DEFAULT_FROM_EMAIL = config("EMAIL_HOST_USER")
BREVO_API_KEY = config("BREVO_API_KEY")

# ✅ Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# ✅ CORS
CORS_ALLOW_ALL_ORIGINS = True

# ✅ CSRF (for production frontend domain)
CSRF_TRUSTED_ORIGINS = [
    "https://portfolio-backend-2s7t.onrender.com",  # 🔁 change if using Fly.io
]

# ✅ Secure cookies for production
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# ✅ Proxy SSL header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ✅ Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
