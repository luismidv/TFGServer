"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d%*3v$s916u#p_*+i-j-%n%!u6dut^qsqqzo#k*1hp)=*53t&!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['tfgserver.onrender.com',
                 "0.0.0.0", os.getenv("RENDER_EXTERNAL_HOSTNAME", "")]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'room',
    'room_api',
    'rest_framework',
    'corsheaders',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://tfgserver.onrender.com"
]

CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_HTTPONLY = False  # Make sure it's accessible by JavaScript
CSRF_COOKIE_SAMESITE = 'None'  # Needed for cross-origin requests
CSRF_COOKIE_SECURE = True  #

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://tfgserver.onrender.com',

]

CORS_ALLOW_CREDENTIALS = True


ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
    #     'BACKEND': 'django.template.backends.django.DjangoTemplates',
    #     'DIRS': [r"C:\Users\luism\OneDrive\Escritorio\TFG LPM\Frontend"],
    #     'APP_DIRS': True,
    #     'OPTIONS': {
    #         'context_processors': [
    #             'django.template.context_processors.debug',
    #             'django.template.context_processors.request', 
    #             'django.contrib.auth.context_processors.auth',
    #             'django.contrib.messages.context_processors.messages',
    #         ],
    #     },
    # },

    "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Keep empty since you don’t use templates
        "APP_DIRS": True,  # Required for Django Admin
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = 'core.wsgi.application'
DEBUG_PROPAGATE_EXCEPTIONS = True


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # PostgreSQL backend
        "NAME": "roomatch",               # Name of your database
        "USER": "luismidv",               # PostgreSQL username
        "PASSWORD": "J7QO7lVyhKk9vFZMyGSc5XYJgCT2r1hY",       # PostgreSQL password
        "HOST": "postgresql://luismidv:J7QO7lVyhKk9vFZMyGSc5XYJgCT2r1hY@dpg-cucvp4an91rc73em2v40-a/roomatch",                        # Use "localhost" or your database server's IP
        "PORT": "5432",                             # Default PostgreSQL port
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
