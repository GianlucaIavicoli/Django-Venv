import os


YAPF_STYLE = "{SPLIT_ALL_COMMA_SEPARATED_VALUES: 1, SPACES_BEFORE_COMMENT: 2, SPLIT_ALL_COMMA_SEPARATED_VALUES: 1}"
MODULES_TO_IMPORT = []
MYSQL_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.getenv('DB_NAME', '<MYSQL_NAME>'),
    'USER': os.getenv('MYSQL_USER', '<MYSQL_USER>'),
    'PASSWORD': os.getenv('MYSQL_PASSWORD', '<MYSQL_PASSWORD>'),
    'HOST': os.getenv('MYSQL_HOST', '<MYSQL_HOST>'),
    'PORT': os.getenv('MYSQL_PORT', '<MYSQL_PORT>'),
}
