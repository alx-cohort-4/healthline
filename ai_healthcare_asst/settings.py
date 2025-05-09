from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("TOP_KEY")

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

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
    'rest_framework.authtoken',
    'corsheaders',
    'dj_rest_auth',
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
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
       
    ]
}

REST_AUTH = {
    'PASSWORD_RESET_SERIALIZER': 'api.serializer.TenantPasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetConfirmSerializer',
    'PASSWORD_CHANGE_SERIALIZER': 'dj_rest_auth.serializers.PasswordChangeSerializer',
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

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "tenant.TenantUser"

# Email Settings
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")

# For testing email in development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_URL = "/tenant/login/"
LOGOUT_REDIRECT_URL = "/tenant/login/"

# setup-cors branch
CORS_ALLOWED_ORIGINS = [
    "https://healthline-nu.vercel.app",
    "http://127.0.0.1:3000",
]

# Allow credentials if needed (e.g., cookies, session auth)
CORS_ALLOW_CREDENTIALS = True

CORS_URLS_REGEX = r"^/api/.*$"

# Prevent the site from being embedded in frames (mitigates clickjacking)
X_FRAME_OPTIONS = "DENY"

SECURE_SSL_REDIRECT = not DEBUG
# Adds Strict-Transport-Security header (enforces HTTPS in browsers)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Prevents browser from guessing content types
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enables XSS protection in some older browsers
SECURE_BROWSER_XSS_FILTER = True

# Cookie security
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_HTTPONLY = True

SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

