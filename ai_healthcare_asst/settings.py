from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("TOP_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tenant',
    'api',
    'rest_framework',
    'rest_framework.authtoken',
    "corsheaders",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Custom middleware placed after Authentication
    'tenant.middleware.MultiTenantMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAuthenticated',
    ]
}
ROOT_URLCONF = 'ai_healthcare_asst.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # This should be added otherwise the tenant will not be available on request.
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai_healthcare_asst.wsgi.application'

# Database
# if DEBUG:
DATABASES = {
    'default': {
        'ENGINE': os.getenv("ENGINE"),
    'NAME': os.getenv("DB_NAME"),     
    'USER': os.getenv("DB_USER"),          
    'PASSWORD': os.getenv("DB_PASSWORD"),      
    'HOST': os.getenv("DB_HOST"),              
    'PORT': os.getenv("DB_PORT"),                   
}
}


# Database routers
# DATABASE_ROUTERS = (
#     'django_tenants.routers.TenantSyncRouter',
# )

# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "tenant.TenantUser"

# Email Settings
if DEBUG:
    EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")
else:
    EMAIL_BACKEND = os.getenv("P_EMAIL_BACKEND")
    EMAIL_HOST = os.getenv("P_EMAIL_HOST")
    EMAIL_PORT = os.getenv("P_EMAIL_PORT")
    EMAIL_HOST_USER = os.getenv("P_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("P_EMAIL_HOST_PASSWORD")
    EMAIL_USE_SSL = os.getenv("P_EMAIL_USE_SSL")

LOGIN_URL = "/tenant/login/"
LOGOUT_REDIRECT_URL = "/tenant/login/"

CELERY_BROKER_URL="redis://localhost:6379/0"

SIMPLE_JWT = {
        'SIGNING_KEY': open('private.pem', 'r').read(),
        'VERIFYING_KEY': open('public.pem', 'r').read(),
        'ALGORITHM': os.getenv('ALGO')
    }
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://\w+\.example\.com$",
# ]

# CORS_ALLOW_METHODS = (
#     "DELETE",
#     "GET",
#     "OPTIONS",
#     "PATCH",
#     "POST",
#     "PUT",
# )

# CORS_ALLOW_HEADERS = (
#     "accept",
#     "authorization",
#     "content-type",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# )
