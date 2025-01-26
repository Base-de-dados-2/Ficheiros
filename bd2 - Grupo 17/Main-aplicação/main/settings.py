from pathlib import Path
from main.constants import DATABASE_PG, DATABASE_MG
from main.db_creedentials import PASS, PORT
from sshtunnel import SSHTunnelForwarder
import atexit

def create_ssh_tunnel():
    return SSHTunnelForwarder(
        ('193.137.7.56', 22),  # Endereço do servidor SSH e porta
        ssh_username='aluno6',  # Nome de usuário SSH
        ssh_password='di!912877',  # Senha do SSH
        remote_bind_address=('127.0.0.1', 5432),  # Endereço e porta do PostgreSQL no servidor remoto
        local_bind_address=('localhost',),  # Deixe o Python escolher uma porta livre
        set_keepalive=10  # Enviar pacotes keep-alive a cada 10 segundos para manter a conexão ativa
    )
tunnel = create_ssh_tunnel()
tunnel.start()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-uag%v=o0_grx$+0&&a+i@^ag46=18qt@3*i_thrk@k%7o21v%="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

HANDLER404 = 'app.views.custom_404_view'


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main.urls"

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

WSGI_APPLICATION = "main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aluno13',           # Nome da sua base de dados PostgreSQL
        'USER': 'aluno13',           # Nome de usuário do PostgreSQL
        'PASSWORD': 'di!507978',    # Senha do PostgreSQL
        'HOST': '127.0.0.1',        # Endereço local (túnel SSH redireciona para o host remoto)
        'PORT': tunnel.local_bind_port,  # Porta local atribuída pelo túnel SSH
    },
    'DATABASE_MG': {
        'ENGINE': 'djongo',
        'NAME': 'bdII_22894',  
        'HOST' : 'mongodb://localhost:27017/',
        'PORT' : 27017,
        'ENFORCE_SCHEMA': False,  
    },
    #'default': {}
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
