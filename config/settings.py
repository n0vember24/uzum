from datetime import timedelta
from os.path import join
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-14^q0a(*lu3%tgcsamg02(dhy&(f-^e*gshwe4exz9!la059t4'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
	'jazzmin',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'uzum',
	'accounts',
	'rest_framework',
	'rest_framework_simplejwt',
	'drf_yasg',
	'mptt',
	'django_filters',
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

ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = 'accounts.User'

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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'uzum',
		'USER': 'postgres',
		'PASSWORD': 'db_pass',
		'HOST': 'localhost',
		'PORT': '5432'
	}
}

AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
		'LOCATION': 'localhost:11211',
	}
}

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.BasicAuthentication',
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	)
}

SIMPLE_JWT = {
	'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
	'ROTATE_REFRESH_TOKENS': True,
	'BLACKLIST_AFTER_ROTATION': True
}

SWAGGER_SETTINGS = {
	'SECURITY_DEFINITIONS': {
		'Basic': {
			'type': 'basic'
		},
		'Bearer': {
			'type': 'apiKey',
			'name': 'Token Authorization',
			'in': 'header'
		}
	}
}

JAZZMIN_SETTINGS = {
	'icons': {
		'auth': 'fas fa-users-cog',
		'accounts.User': 'fas fa-user',
		'auth.Group': 'fas fa-users',
		'admin.LogEntry': 'fas fa-file',
		'uzum.Cart': 'fas fa-shopping-cart',
		'uzum.Category': 'fas fa-list',
		'uzum.Favourite': 'fas fa-star',
		'uzum.Order': 'fas fa-clipboard-list',
		'uzum.Product': 'fas fa-shopping-basket',
		'uzum.ProductImage': 'fas fa-images',
		'uzum.Report': 'fas fa-history',
		'uzum.Vendor': 'fas fa-store',
		'uzum.BranchPoint': 'fas fa-map-marker-alt',
	},
}

TWILIO_ACCOUNT_SID = 'ACc5d9252dd2872a666f2f4f13d5461160'
TWILIO_AUTH_TOKEN = '845ab57f85851195a3336e156d7165ef'
TWILIO_PHONE_NUMBER = '+17076406640'
TWILIO_SERVICES = 'MGccfb6a600186c24e41b29392b4da2da1'
