"""
Django settings for myProject project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib.messages import constants as messages  # 追加
from django.contrib.messages import constants as message_constants  # 追加

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# django-environを用いて.envから変数を読み込めるようにする
ENV_FILE_PATH = Path(__file__).resolve().parent.parent.parent.parent / '.env'
env = environ.Env()
env.read_env(ENV_FILE_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get("SECRET_KEY")
# SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env.get_value("DEBUG", cast=int, default=0)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myAccount.apps.MyAccountConfig',
    'board.apps.BoardConfig',
    'storages',
    # Bootstrap
    'bootstrap4',
    # 画像処理関連
    'django_cleanup.apps.CleanupConfig',
    'sorl.thumbnail',
    # 以下、allauth用
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # googleで認証
]

# Bootstrap4 jqueryを使用するため追加
BOOTSTRAP4 = {
    'include_jquery': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'myAccount.context_processors.common',  # 追加
            ],
            # Bootstrap4を使用するために追加
            'builtins': [
                'bootstrap4.templatetags.bootstrap4',
            ],
        },
    },
]

WSGI_APPLICATION = 'myProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     # 'default': {
#     #     'ENGINE': 'django.db.backends.sqlite3',
#     #     'NAME': BASE_DIR / 'db.sqlite3',
#     # }
#     "default": {
#         "ENGINE": env("DB_ENGINE"),
#         "NAME": env("DB_NAME"),
#         "USER": env("DB_USER"),
#         "PASSWORD": env("DB_PASSWORD"),
#         "HOST": env("DB_HOST"),
#         "PORT": env.get_value("DB_PORT", cast=int),
#     }
# }

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# for allauth
SITE_ID = 1

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 追加 メッセージタグの設定
MESSAGE_TAGS = {
    messages.ERROR: 'alert alert-danger alert-dismissible fade show',
    messages.WARNING: 'alert alert-warning alert-dismissible fade show',
    messages.SUCCESS: 'alert alert-success alert-dismissible fade show',
    messages.INFO: 'alert alert-info alert-dismissible fade show'
}

AUTH_USER_MODEL = 'myAccount.MyUser'

# ログインURLやリダイレクト先の設定
LOGIN_REDIRECT_URL = 'home'  # ログイン後のリダイレクト先
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'  # ログアウト後のリダイレクト先
LOGIN_URL = 'account_login'  # 'loginrequired'などの遷移先
# LOGOUT_REDIRECT_URL = 'account_login'
# ACCOUNT_SIGNUP_REDIRECT_URL = 'myAccount:home'  # メール認証なしでサインアップした場合の登録後のリダイレクト先

# ログイン・サインアップ時の設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # メールアドレスでログイン
ACCOUNT_EMAIL_REQUIRED = True  # メールアドレスでログインする場合は必要
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # MyUserモデルからusernameを除外
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # メールアドレスを認証するか(none=しない, mandatory=必須)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # 確認メールの有効期限（日）
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # メアド確認後、自動ログインして'LOGIN_REDIRECT_URL'に遷移(登録、確認を同じブラウザで行わないと機能しない)
ACCOUNT_LOGOUT_ON_GET = True  # GETでそのままログアウト
# ACCOUNT_LOGIN_ON_PASSWORD_RESET = True  # パスワードリセット後、自動ログイン


# その他の設定
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''  # メールの件名のプレフィックス
ACCOUNT_MAX_EMAIL_ADDRESSES = 2  # 登録できるメールアドレスの上限。1だと変更できない。
ACCOUNT_USERNAME_BLACKLIST = []  # usernameとして使えない文字

# 認証メールの設定。開発中はコンソールに擬似的に送信される。
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'pictoforio@gmail.com'
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

GUEST_USER_EMAIL = 'guestguest@mail.com'