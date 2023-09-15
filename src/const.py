import string
import secrets


def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(12))
    return password


YAPF_STYLE = "{SPLIT_ALL_COMMA_SEPARATED_VALUES: 1, SPACES_BEFORE_COMMENT: 2, SPLIT_ALL_COMMA_SEPARATED_VALUES: 1}"

MODULES_TO_IMPORT = ['environ', 'os']
DEFAULT_ASSETS_ROOT = '/static/assets'

# Default MySQL:

MYSQL_ROOT_PASSWORD = generate_password()
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3336
MYSQL_USER = 'test'
MYSQL_PASSWORD = generate_password()

# Default PostgreSQL:

POSTGRESQL_ROOT_PASSWORD = generate_password()
POSTGRESQL_HOST = '127.0.0.1'
POSTGRESQL_PORT = 5434
POSTGRESQL_USER = 'test'
POSTGRESQL_PASSWORD = generate_password()

# settings.py const
LITERAL_BASE_DIR = "BASE_DIR = os.path.dirname(os.path.dirname(__file__))"
LITERAL_READ_ENV = "environ.Env.read_env(os.path.join(BASE_DIR, '.env'))"
LITERAL_ENV = "env = environ.Env(DEBUG=(bool, True))"
LITERAL_DEBUG = "DEBUG = env('DEBUG')"
LITERAL_ROOT_DIR = "ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))"
LITERAL_SECRET_KEY = "SECRET_KEY = env('SECRET_KEY')"
LITERAL_MYSQL = "DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': os.getenv('MYSQL_NAME'), 'USER': os.getenv('MYSQL_USER'), 'PASSWORD': os.getenv('MYSQL_PASSWORD'), 'HOST': os.getenv('MYSQL_HOST', 'localhost'), 'PORT': os.getenv('MYSQL_PORT')} }"
LITERAL_POSTGRESQL = "DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': os.getenv('POSTGRESQL_NAME'), 'USER': os.getenv('POSTGRESQL_USER'), 'PASSWORD': os.getenv('POSTGRESQL_PASSWORD'), 'HOST': os.getenv('POSTGRESQL_HOST', 'localhost'), 'PORT': os.getenv('POSTGRESQL_PORT')} }"
LITERAL_ASSETS_ROOT = "ASSETS_ROOT = os.getenv('ASSETS_ROOT')"
LITERAL_ALLOWED_HOSTS = "ALLOWED_HOSTS = ['localhost', '127.0.0.1', env('SERVER', default='127.0.0.1')]"
LITERAL_CSRF_TRUSTED_ORIGINS = "CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1')]"

LITERAL_INSTALLED_APPS = "INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages','django.contrib.staticfiles','apps.home' ]"
LITERAL_INSTALLED_APPS_HTMX = "INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages','django.contrib.staticfiles','django_htmx','apps.home' ]"

LITERAL_MIDDLEWARE = "MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django_htmx.middleware.HtmxMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']"
LITERAL_TEMPLATE_DIR = "TEMPLATE_DIR = os.path.join(ROOT_DIR, 'apps/templates')"
LITERAL_TEMPLATES = "TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [TEMPLATE_DIR], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]"
LITERAL_STATIC_ROOT = "STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')"
LITERAL_STATICFILES_DIRS = "STATICFILES_DIRS = (os.path.join(ROOT_DIR, 'apps/static'))"

# SMTP literals:
EMAIL_BACKEND = "EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'"
EMAIL_HOST = "EMAIL_HOST = os.getenv('EMAIL_HOST')"
EMAIL_USE_TLS = "EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')"
EMAIL_PORT = "EMAIL_PORT = os.getenv('EMAIL_PORT')"
EMAIL_USE_SSL = "EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')"
EMAIL_HOST_USER = "EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')"
EMAIL_HOST_PASSWORD = "EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')"


# Comments for each settings:

SETTINGS_COMMENTS = [("BASE_DIR", "# Build paths inside the project like this: os.path.join(BASE_DIR, ...)"),
                     ("SECRET_KEY", "# SECURITY WARNING: keep the secret key used in production secret!"),
                     ("env", "# Take environment variables from .env file"),
                     ("ASSETS_ROOT", "# Assets Management"),
                     ("ALLOWED_HOSTS", "# The ALLOWED_HOSTS setting specifies a list of host/domain names that this Django application can serve. Requests with hostnames not included in this list will be denied access as a security measure to prevent HTTP Host header attacks."),
                     ("CSRF_TRUSTED_ORIGINS", "# The CSRF_TRUSTED_ORIGINS setting allows you to specify a list of trusted origins (domains) for Cross-Site Request Forgery (CSRF) protection. Requests originating from these domains will not be subject to CSRF checks. This is useful when you need to allow AJAX requests from specific origins."),
                     ("MIDDLEWARE", "# The MIDDLEWARE setting defines the order and behavior of middleware components that process each request and response in your Django application."),
                     ("TEMPLATE_DIR",
                      "# Store the path to your custom templates directory."),
                     ("TEMPLATES", "# Configures the template engine for your Django project."),
                     ("STATICFILES_DIRS",
                      "# Extra places for collectstatic to find static files."),
                     ("EMAIL_BACKEND", "# Email backend setting specifies the backend to use for sending email."),
                     ("EMAIL_HOST", "# The hostname of your email server."),
                     ("EMAIL_USE_TLS",
                      "# Set this to False if your email server doesn't use TLS."),
                     ("EMAIL_PORT", "# The port to use for the SMTP server."),
                     ("EMAIL_USE_SSL", "# Set this to True if your email server uses SSL."),
                     ("EMAIL_HOST_USER",
                      "# The email address you want to use as the sender."),
                     ("EMAIL_HOST_PASSWORD", "# The password for the email address used as the sender.")]
