
YAPF_STYLE = "{SPLIT_ALL_COMMA_SEPARATED_VALUES: 1, SPACES_BEFORE_COMMENT: 2, SPLIT_ALL_COMMA_SEPARATED_VALUES: 1}"

MODULES_TO_IMPORT = ['environ', 'os']


# settings.py const

READ_ENV_LITERAL = "environ.Env.read_env(os.path.join(BASE_DIR, '.env'))"
ENV_LITERAL = "env = environ.Env(DEBUG=(bool, True))"
DEBUG_LITERAL = "DEBUG = env('DEBUG')"
ROOT_DIR_LITERAL = "ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))"
SECRE_KEY_LITERAL = "SECRET_KEY = env('SECRET_KEY')"
MYSQL_CONFIG = "DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': os.getenv('DB_NAME'), 'USER': os.getenv('MYSQL_USER'), 'PASSWORD': os.getenv('MYSQL_PASSWORD'), 'HOST': os.getenv('MYSQL_HOST', 'localhost'), 'PORT': os.getenv('MYSQL_PORT', 3306)} }"
