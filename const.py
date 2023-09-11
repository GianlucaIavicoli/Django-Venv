
YAPF_STYLE = "{SPLIT_ALL_COMMA_SEPARATED_VALUES: 1, SPACES_BEFORE_COMMENT: 2, SPLIT_ALL_COMMA_SEPARATED_VALUES: 1}"

MODULES_TO_IMPORT = ['environ', 'os']
DEFAULT_ASSETS_ROOT = '/static/assets'

# settings.py const

LITERAL_READ_ENV = "environ.Env.read_env(os.path.join(BASE_DIR, '.env'))"
LITERAL_ENV = "env = environ.Env(DEBUG=(bool, True))"
LITERAL_DEBUG = "DEBUG = env('DEBUG')"
LITERAL_ROOT_DIR = "ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))"
LITERAL_SECRET_KEY = "SECRET_KEY = env('SECRET_KEY')"
LITERAL_MYSQL = "DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': os.getenv('DB_NAME'), 'USER': os.getenv('MYSQL_USER'), 'PASSWORD': os.getenv('MYSQL_PASSWORD'), 'HOST': os.getenv('MYSQL_HOST', 'localhost'), 'PORT': os.getenv('MYSQL_PORT', 3306)} }"
LITERAL_ASSETS_ROOT = "ASSETS_ROOT = os.getenv('ASSETS_ROOT')"
LITERAL_ALLOWED_HOSTS = "ALLOWED_HOSTS = ['localhost', '127.0.0.1', env('SERVER', default='127.0.0.1')]"
LITERAL_CSRF_TRUSTED_ORIGINS = "CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1')]"

LITERAL_INSTALLED_APPS = "INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages','django.contrib.staticfiles','django_htmx','apps.home' ]"
