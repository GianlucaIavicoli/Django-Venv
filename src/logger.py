from script import Logger
import sys

if __name__ == '__main__':
    level = sys.argv[1]
    message = sys.argv[2]
    logger = Logger()

    if level == 'info':
        logger.log_info(message)

    elif level == 'warning':
        logger.log_warning(message)

    elif level == 'error':
        logger.log_error(message)
