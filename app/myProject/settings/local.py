from .base import *
import environ

ENV_FILE_PATH = Path(__file__).resolve().parent.parent.parent.parent / '.env'

env = environ.Env()
env.read_env(ENV_FILE_PATH)

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

# Django Debug Toolbarを有効化
INSTALLED_APPS += [
    "debug_toolbar",
]

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env.get_value("DB_PORT", cast=int),
    }
}


MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# INTERNAL_IPS = ["127.0.0.1"]
INTERNAL_IPS = ["172.18.0.1"]

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default="localhost")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# static, mediaは開発環境ではプロジェクト内、本番ではaws S3内に保存する
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# アプリ配下とは別に、共通で使われる静的ファイルの配置設定（STATIC_ROOTとかぶらせるとエラーが出る）
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_dev"),
]
#
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# AWS S3用の設定
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
# AWS_LOCATION = 'static'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# # mediaファイルを"media"ディレクトリで管理するためのカスタムバックエンド
# DEFAULT_FILE_STORAGE = 'myProject.backends.MediaStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'local': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'local',
        },
    },
    'loggers': {
        # 自作したログ出力
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Djangoのエラー・警告・開発WEBサーバのアクセスログ
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # 実行SQL
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}