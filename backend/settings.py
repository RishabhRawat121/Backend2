from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-default-key")
DEBUG = True
ALLOWED_HOSTS = ["*"]  # For development only

# SUPABASE
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://dcssjbdtwofaaiyyfzit.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<your-key>")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "avatars")

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get(
            "DATABASE_URL",
            "postgresql://postgres:Deanambrose%4012345@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
        ),
        conn_max_age=60,
        ssl_require=True
    )
}


# MEDIA (user uploads like avatars)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# STATIC (CSS, JS, images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # additional folders for dev
STATIC_ROOT = BASE_DIR / "staticfiles"    # collectstatic destination

# EMAIL (development)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@example.com"

# ROOT URL
ROOT_URLCONF = 'backend.urls'  # Replace 'backend' with your project folder

# INSTALLED APPS
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
    "rest_framework_simplejwt",
    "corsheaders",
    
    # Channels
    "channels",

    # Your apps
    "users",
    "posts",
]

# MIDDLEWARE
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS / CSRF
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = False

# REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

# TEMPLATES
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

# DEFAULT PK
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# TIMEZONE / I18N
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Channels
ASGI_APPLICATION = 'yourproject.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
