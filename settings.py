# coding: utf-8

import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'q8@+pm33!e*!5zisvxx_k+^-p1byx0aaypj&^6_gwwefm*90x&'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guardian',
    'web',
    'h5',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'investment.urls'

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

WSGI_APPLICATION = 'investment.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'investment',
        'USER': 'root',
        'PASSWORD': 'yijia',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}


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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=60),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    'web.auth_web.mobile.MobileBackend',
)


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

BACK_PAGE_COUNT = 15

# 后台提醒
FILED_CHECK_MSG = '<b class="error_msg">字段不能为空</b>'

# 过滤不可添加的父级栏目
COLUMN_NOT_LIST = [
    # {'id': 1, 'name': '内容服务'},
]
# 是否可以创建父栏目
COLUMN_IS_ADD = True
COLUMN_IS_EDIT = True

# redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_TIMEOUT = 7*24*60*60

# 加密前缀
DB_PREFIX = 'investment_'

# 云通讯
SMS_ACCOUNT_SID = '8aaf0708570871f8015721cd332f0e24'
SMS_ACCOUNT_TOKEN = '4445bda8680142899dc91c43df4a7d99'
SMS_SUB_ACCOUNT_SID = 'a1eb8b67976611e69b876c92bf2c142d'
SMS_SUB_ACCOUNT_TOKEN = 'c2c7a073d888513461a4f7439f110951'
SMS_APP_ID = '8aaf070857dc0e780157e14b3a1c04b2'
SMS_TEMPLATE_CODE_ID = 125618

# 微信
WECHAT_APP_ID = 'wx6a6aa8335b5059c4'
WECHAT_APP_SECRET = 'c3dcd3cf0738066226fe4b495d500485'

# ping++
API_KEY = 'sk_live_DKyPiDvnn1qTeDyzPK98W1e5'
APP_ID = 'app_SOGGKKPaLafDq1aH'


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'upload')

MEDIA_URL = '/media/'
MEDIA_ROOT = UPLOAD_DIR

DOMAIN = 'http://119.23.210.215:81'

# setting_local
ROOT = os.path.abspath(os.path.dirname(__file__))
if os.path.exists(os.path.join(ROOT, 'settings_local.py')):
    execfile(os.path.join(ROOT, 'settings_local.py'))
