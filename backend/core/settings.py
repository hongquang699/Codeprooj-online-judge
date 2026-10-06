import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def _load_project_env(path: Path) -> None:
    """Load simple KEY=value entries without overriding process environment."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)

_load_project_env(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError('SECRET_KEY must be set in the environment or project .env file')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0,codeprooj.com,www.codeprooj.com').split(',') if h.strip()]
if 'codeprooj.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend(['codeprooj.com', 'www.codeprooj.com'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'backend.judge.apps.JudgeAppConfig',
    'backend.api.apps.ApiConfig',
    'backend.community.apps.CommunityConfig',
    'backend.ranking.apps.RankingConfig',
    'backend.users.apps.UsersConfig',
    'backend.organizations.apps.OrganizationsConfig',
    'backend.contest_admin.apps.ContestAdminConfig',
    'backend.auth.apps.AuthConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'security.middleware.FullSecurityMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'backend', 'templates')],
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

CSRF_TRUSTED_ORIGINS = [
    'https://codeprooj.com',
    'http://codeprooj.com',
    'https://www.codeprooj.com',
    'http://www.codeprooj.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:8888',
    'http://127.0.0.1:8888',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

WSGI_APPLICATION = 'backend.core.wsgi.application'
ASGI_APPLICATION = 'backend.core.asgi.application'

DB_ENGINE = os.getenv('DB_ENGINE', '').lower()
DB_HOST = os.getenv('DB_HOST', '')

if DB_ENGINE in ('mysql', 'mariadb'):
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'coding_platform'),
            'USER': os.getenv('DB_USER', 'coding_app'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': DB_HOST or 'localhost',
            'PORT': os.getenv('DB_PORT', '3306'),
            'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', '60')),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION'",
            }
        }
    }
elif DB_ENGINE in ('postgresql', 'postgres', 'pgsql') or DB_HOST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'coding_platform'),
            'USER': os.getenv('DB_USER', 'judge_admin'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': DB_HOST or 'localhost',
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'database' / 'vnoi_db.sqlite3',
        }
    }

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
]

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'frontend')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'storage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Cryptographic Password & Token Hashing (SHA-512 & SHA-256) ────────────────
PASSWORD_HASHERS = [
    'backend.auth.security.crypto_hash.PBKDF2SHA512PasswordHasher',  # PBKDF2 with HMAC-SHA512 (Primary default)
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',              # PBKDF2 with HMAC-SHA256 (Compatibility)
    'backend.auth.security.crypto_hash.SHA512PasswordHasher',        # Salted SHA-512
    'backend.auth.security.crypto_hash.SHA256PasswordHasher',        # Salted SHA-256
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# ── CORS Settings (Strict Origin Whitelist when credentials allowed) ─────────
CORS_ALLOW_CREDENTIALS = True
if not DEBUG and os.getenv('CORS_ALLOW_ALL') != 'True':
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        'https://codeprooj.com',
        'http://codeprooj.com',
        'https://www.codeprooj.com',
        'http://www.codeprooj.com',
        'http://localhost:8888',
        'http://127.0.0.1:8888',
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]
    env_cors = os.getenv('CORS_ALLOWED_ORIGINS')
    if env_cors:
        CORS_ALLOWED_ORIGINS.extend([o.strip() for o in env_cors.split(',') if o.strip()])
else:
    CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL', 'False').lower() == 'true'

csrf_origins = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://codeprooj.com,http://codeprooj.com,https://www.codeprooj.com,http://www.codeprooj.com,http://localhost:8888,http://127.0.0.1:8888,http://localhost:8000,http://127.0.0.1:8000')
CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins.split(',') if o.strip()]

# ── Security & Cookie Hardening (XSS, CSRF, Clickjacking) ─────────────────────
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Production HTTPS & HSTS Settings (Activated when DEBUG is False)
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'
    CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True') == 'True'
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False


REST_FRAMEWORK_RENDERERS = ['rest_framework.renderers.JSONRenderer']
if DEBUG:
    REST_FRAMEWORK_RENDERERS.append('rest_framework.renderers.BrowsableAPIRenderer')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': REST_FRAMEWORK_RENDERERS
}

# DMOJ / VNOI Specific configs
DMOJ_PROBLEM_DATA_ROOT = os.getenv('DMOJ_PROBLEM_DATA_ROOT', str(BASE_DIR / 'problem-data' / 'problems'))
DMOJ_CONTEST_DATA_ROOT = os.getenv('DMOJ_CONTEST_DATA_ROOT', str(BASE_DIR / 'contest-data' / 'contests'))

# ── Judge System Integration ──────────────────────────────────────────────────
# External judge-system REST API (port 9999)
JUDGE_SERVER_URL  = os.getenv('JUDGE_SERVER_URL', 'http://127.0.0.1:9999')
JUDGE_AUTH_TOKEN  = os.getenv('JUDGE_AUTH_TOKEN', '')
JUDGE_POLL_TIMEOUT   = int(os.getenv('JUDGE_POLL_TIMEOUT', '30'))   # max seconds to wait
JUDGE_POLL_INTERVAL  = float(os.getenv('JUDGE_POLL_INTERVAL', '0.5'))  # seconds between polls
