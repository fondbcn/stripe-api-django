from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'auth.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k$%f*@8g-huo)u*s+ii-!_(33d!jpr1!pa@1=b@4z%2ufg4v=@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

PAYPAL_CLIENT_ID = 'Aa4hM-oy9bu5YX8qkqUkZS-RIGIE6If4iHVgtEXZAoOg2Ld9euZCnmmeFzfAVuLF7xuZUeGn85sKpGGB'
PAYPAL_SECRET_KEY = 'EHzxCxdmnWgKuVsEiDvVT6koL-sVKV7RYulxunnnDMuumB60pEqVAVtPyp4biHIzV6pmGPc2cavVGIpr'

STRIPE_TEST_PUBLIC_KEY ='pk_test_51OOFpIJODblskrVixPPy0G5xSBHpc5LDX6ovbnBBFnvbjnvyWcYwxW1u1nKNdU9fx6XvQO4emQkCRHvsSBGc7BQC001hHsichc'
STRIPE_TEST_SECRET_KEY = 'sk_test_51OOFpIJODblskrVisz58sAsDpZCFPxxtlCTsCBxBPBveGQOfNwpuiNbOmJmcR06SL3CYOIbArZ5MDqJpOnjmM9uK00ZfSS7mod'
STRIPE_WEBHOOK_SECRET ='whsec_MH6A5qLZaDPPxS1KXBZBHV93xzd3m1q2'
STRIPE_LIVE_MODE = False  # Change to True in production

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pay',
    'guest_user',
]

AUTHENTICATION_BACKENDS = [
   "pay.auth.EmailBackend",
   "django.contrib.auth.backends.ModelBackend",
   "guest_user.backends.GuestBackend",
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

ROOT_URLCONF = 'djgo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djgo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

STATIC_URL = 'pay/static/'

SESSION_COOKIE_AGE = 3600*24

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'