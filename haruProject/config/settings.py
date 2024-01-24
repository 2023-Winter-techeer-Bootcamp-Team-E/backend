"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import environ
import boto3

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
'''
2. 각 호출자가 기본 매개변수를 전달할 필요가 없도록 환경 변수의 체계 기반 조회를 제공합니다.
라고 번역하니 나와있는데, 무슨말인지 생각해보니 환경변수를 불러올 수 있는 상태로 세팅한다고
이해했다. 

'''
env = environ.Env(DEBUG=(bool, True))

'''
3. 환경변수를 읽어올 준비는 마쳤고, 어떤 파일에서 불러올건지 정해줘야 하기 때문에
나는 '.env'에서 가져올거라고 설정해줬다.
'''
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
'''
4. SECEREY_KEY와 DEBUG에 넣은 값들을 불러올 수 있게 설정
'''
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# AUTH_USER_MODEL = 'member.Member'

# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'corsheaders',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'diary',
    'rest_framework',
    'member',
    'guest',
    'harucalendar',
    'drf_yasg',
    'storages',
    'static',
    'whitenoise',
    'django_prometheus',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',

]

# CORS 설정 - whitelist 에 추가된 주소 접근 허용
CORS_ORIGIN_WHITELIST = [
    "https://127.0.0.1:3000",  # for dev remove
    "http://127.0.0.1:8000",
    # for dev remove
    "http://frontend:3000",
    "http://backend:8000",
    "http://localhost:*"
]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "host.docker.internal"]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1",
    "https://www.haruconnection.store"
]
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = None
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

CORS_ORIGIN_ALLOW_ALL = True

# SESSION_COOKIE_DOMAIN = "founderslooking.com"

# SESSION_COOKIE_SECURE = False

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

ASGI_APPLICATION = 'config.asgi.application'
# CHHANNEL_LAYERS = {
#
WSGI_APPLICATION = 'config.wsgi.application'
#
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'haru',
#         'USER': 'root',
#         'PASSWORD': '12345678',
#         'HOST': 'db',
#         'PORT': '3306',
#     }
# }

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

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DALLE_API_KEY = env('DALLE_API_KEY')

# AWS S3 설정
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_URL_PROTOCOL = 'https:'

# Django-storages 설정
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_USE_SSL = True

# Static files (CSS, JavaScript, images)
# STATIC_URL = f"{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/static/"
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media files (uploads)
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = f"{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/media/"
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

# celery와 관련된 환경설정
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_ENABLE_UTC = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 디폴트 : True, 장고의 디폴트 로그 설정을 대체. / False : 장고의 디폴트 로그 설정의 전부 또는 일부를 다시 정의
    'formatters': {  # message 출력 포맷 형식
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs') + "/log",  # message가 저장될 파일명(파일명 변경 가능)
            'formatter': 'verbose'
        },
        'member_file': {
            'level': 'INFO',
            'class': "logging.FileHandler",
            'filename': os.path.join(BASE_DIR, 'logs') + "/member_log"
        },
        'calendar_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs') + "/calendar_log"

        },
        'diary_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs') + "/diary_log"

        },
        'static_file':{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs') + "/static_log"

        },

    },
    'loggers': {
        'django': {
            'handlers': ['file'],  # 'file' : handler의 이름
            'propagate': True,
            'level': 'DEBUG',  # DEBUG 및 그 이상의 메시지를 file 핸들러에게 보내줍니다.
        },
        'member': {  # Project에서 생성한 app의 이름
            'handlers': ['member_file'],  # 다른 app을 생성 후 해당 app에서도
            'propagate': True,
            'level': 'INFO',  # 사용하고자 할 경우 해당 app 이름으로
        },
        'harucalendar': {  # Project에서 생성한 app의 이름
            'handlers': ['calendar_file'],  # 다른 app을 생성 후 해당 app에서도
            'propagate': True,
            'level': 'INFO',  # 사용하고자 할 경우 해당 app 이름으로
        },
        'diary': {  # Project에서 생성한 app의 이름
            'handlers': ['diary_file'],  # 다른 app을 생성 후 해당 app에서도
            'propagate': True,
            'level': 'INFO',  # 사용하고자 할 경우 해당 app 이름으로
        },
        'static': {  # Project에서 생성한 app의 이름
            'handlers': ['static_file'],  # 다른 app을 생성 후 해당 app에서도
            'propagate': True,
            'level': 'INFO',  # 사용하고자 할 경우 해당 app 이름으로
        },
        # 좌측 코드를 추가 작성해서 사용
    }
}

