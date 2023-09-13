import ast
import subprocess
import sys
import os
from time import sleep
from typing import Union
from const import *
import logging
import colorlog


class Logger:
    def __init__(self, logFileName='script.log', logLevel=logging.INFO):
        """
        Initialize the ColoredLogger.

        Args:
            log_file_name (str): The name of the log file. Default is "script.log".
            log_level (int): The logging level. Default is INFO.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logLevel)

        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)s]: %(message)s",
            log_colors={
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
            },
            secondary_log_colors={},
            style='%'
        )

        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(logFileName)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s]: %(message)s"))

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def log_info(self, message):
        """
        Log an informational message.

        Args:
            message (str): The message to log.
        """
        self.logger.info(message)

    def log_warning(self, message):
        """
        Log a warning message.

        Args:
            message (str): The warning message to log.
        """
        self.logger.warning(message)

    def log_error(self, message):
        """
        Log an error message.

        Args:
            message (str): The error message to log.
        """
        self.logger.error(message)


class EditSettings:
    def __init__(self, settingsPath: str, dbType: Union[str, None], projectName: str):
        """
        Class for modifying a Django project's settings.py file.

        This class facilitates the addition of necessary imports, modifications to the database configuration, and fixes for code indentation.

        Args:
            settingsPath (str): Path to settings.py
            dbType (Union[str, None]): The type of database to use. It can be one of the following values: mysql, postgre or None.
            projectName (str): Project name
        """
        self.settingsPath = settingsPath
        self.dbType = dbType
        self.projectName = projectName
        self.logger = Logger()

    def parse_file(self) -> ast.Module:
        with open(self.settingsPath, 'r') as f:
            fileContent = f.read()

        # Parse the settings.py
        return ast.parse(fileContent)

    def unparse_and_save_file(self) -> None:
        unparsedFile = ast.unparse(self.root)
        with open(self.settingsPath, 'w') as f:
            f.write(unparsedFile)
        self.logger.log_info("Settings.py correctly edited.")

    def add_blank_lines(self) -> None:
        """This method will just add blank lines to make the file more readable."""

        with open(self.settingsPath, 'r') as f:
            lines = f.readlines()

            modifiedLines = []

            for line in lines:
                modifiedLines.append(line)
                if line.strip().endswith(']') or line.strip().endswith('}') or line.strip().endswith(')') or line.strip().endswith("'") or line.strip().endswith('True'):
                    modifiedLines.append('\n')

            with open(self.settingsPath, 'w') as f:
                f.writelines(modifiedLines)

    def format_file(self) -> None:
        """Format 'settings.py' with yapf"""

        command = f"yapf -i --style='{YAPF_STYLE}' {self.settingsPath}"
        subprocess.run(command, shell=True, check=True)
        self.logger.log_info("'settings.py' correctly formatted.")

    # In order:

    def _add_imports(self) -> None:

        # Remove the 'from pathlib import Path' which would be useless.
        for node in ast.walk(self.root):
            if isinstance(node, ast.ImportFrom):
                self.root.body.remove(node)

        for module in MODULES_TO_IMPORT:
            importNode = ast.Import(
                names=[ast.alias(name=module, asname=None)])

            self.root.body.insert(1, importNode)

        self.logger.log_info("Added necessary imports.")

    def _add_base_dir(self) -> None:
        for node in ast.walk(self.root):

            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'BASE_DIR':
                baseDirNodeToReplace = node
                baseDirNodeIndex = self.root.body.index(node)

                baseDirNode = ast.parse(LITERAL_BASE_DIR).body[0]

                ast.copy_location(baseDirNode, baseDirNodeToReplace)
                self.root.body.remove(baseDirNodeToReplace)
                self.root.body.insert(baseDirNodeIndex, baseDirNode)

        self.logger.log_info("Added BASE_DIR.")

    def _add_root_dir(self) -> None:
        for node in ast.walk(self.root):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'BASE_DIR':
                baseDirNodeIndex = self.root.body.index(node)

        rootDirNode = ast.parse(LITERAL_ROOT_DIR).body[0]
        self.root.body.insert(baseDirNodeIndex + 1, rootDirNode)
        self.logger.log_info("Added ROOT_DIR.")

    def _add_env(self) -> None:
        for node in ast.walk(self.root):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'SECRET_KEY':
                debugNodeIndex = self.root.body.index(node)

        envNode = ast.parse(LITERAL_ENV).body[0]
        self.root.body.insert(debugNodeIndex, envNode)

        readEnvNode = ast.parse(LITERAL_READ_ENV).body[0]
        self.root.body.insert(debugNodeIndex + 1, readEnvNode)
        self.logger.log_info("Added ENV and read_env.")

    def _add_secret_key(self) -> None:
        def _save_secret_key(secretKey: str) -> None:
            with open('.env', 'a') as env:
                env.write(f"DJANGO_SECRET_KEY='{secretKey}'\n\n")

        for node in ast.walk(self.root):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'SECRET_KEY':
                secretKeyNodeToReplace = node
                secretKeyNodeIndex = self.root.body.index(node)

                secretKeyNode = ast.parse(LITERAL_SECRET_KEY).body[0]
                secretKey = secretKeyNodeToReplace.value.s

                _save_secret_key(secretKey)

                ast.copy_location(secretKeyNode, secretKeyNodeToReplace)
                # self.root.body.remove(secretKeyNodeToReplace)
                # self.root.body.insert(secretKeyNodeIndex, secretKeyNode)

                self.logger.log_info("Added SECRET_KEY.")

    def _add_debug(self) -> None:
        for node in ast.walk(self.root):

            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'DEBUG':
                debugNodeToReplace = node
                debugNodeIndex = self.root.body.index(node)

                debugNode = ast.parse(LITERAL_DEBUG).body[0]

                ast.copy_location(debugNode, debugNodeToReplace)
                self.root.body.remove(debugNodeToReplace)
                self.root.body.insert(debugNodeIndex, debugNode)
                self.logger.log_info("Added DEBUG.")

    def _add_assets_root(self) -> None:
        def add_inside_env() -> None:
            with open('.env', 'a') as env:
                env.write(f"ASSETS_ROOT='{DEFAULT_ASSETS_ROOT}'\n\n")

        for node in ast.walk(self.root):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'DEBUG':
                debugNodeIndex = self.root.body.index(node)

        add_inside_env()
        assetsRootNode = ast.parse(LITERAL_ASSETS_ROOT).body[0]
        self.root.body.insert(debugNodeIndex + 1, assetsRootNode)
        self.logger.log_info("Added ASSETS_ROOT.")

    def _add_allowed_hosts(self) -> None:
        for node in ast.walk(self.root):

            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'ALLOWED_HOSTS':
                allowedHostsNodeToReplace = node
                allowedHostsNodeIndex = self.root.body.index(node)

                allowedHostsNode = ast.parse(LITERAL_ALLOWED_HOSTS).body[0]

                ast.copy_location(allowedHostsNode, allowedHostsNodeToReplace)
                self.root.body.remove(allowedHostsNodeToReplace)
                self.root.body.insert(
                    allowedHostsNodeIndex, allowedHostsNode)
                self.logger.log_info("Added ALLOWED_HOSTS.")

    def _add_csrf_trusted(self) -> None:
        for node in ast.walk(self.root):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'ALLOWED_HOSTS':
                allowedHostsNodeIndex = self.root.body.index(node)

        csrfTrustedNode = ast.parse(LITERAL_CSRF_TRUSTED_ORIGINS).body[0]
        self.root.body.insert(allowedHostsNodeIndex + 1, csrfTrustedNode)
        self.logger.log_info("Added CSRF_TRUSTED_ORIGINS.")

    def _add_installed_apps(self) -> None:
        for node in ast.walk(self.root):

            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'INSTALLED_APPS':
                installedAppsNodeToReplace = node
                installedAppsNodeIndex = self.root.body.index(node)

                installedAppsNode = ast.parse(LITERAL_INSTALLED_APPS).body[0]

                ast.copy_location(installedAppsNode,
                                  installedAppsNodeToReplace)
                self.root.body.remove(installedAppsNodeToReplace)
                self.root.body.insert(
                    installedAppsNodeIndex, installedAppsNode)
                self.logger.log_info("Added INSTALLED_APPS.")

    def _add_middleware(self) -> None:
        for node in ast.walk(self.root):

            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'MIDDLEWARE':
                middlewareNodeToReplace = node
                middlewaresNodeIndex = self.root.body.index(node)

                middlewareNode = ast.parse(LITERAL_MIDDLEWARE).body[0]

                ast.copy_location(middlewareNode,
                                  middlewareNodeToReplace)
                self.root.body.remove(middlewareNodeToReplace)
                self.root.body.insert(
                    middlewaresNodeIndex, middlewareNode)
                self.logger.log_info("Added MIDDLEWARE.")

    def _add_template_dir(self) -> None:
        for node in ast.walk(self.root):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'ROOT_URLCONF':
                rootUrlIndex = self.root.body.index(node)

        templateDirNode = ast.parse(LITERAL_TEMPLATE_DIR).body[0]
        self.root.body.insert(rootUrlIndex + 1, templateDirNode)
        self.logger.log_info("Added TEMPLATE_DIR.")

    def _add_templates(self) -> None:
        for node in ast.walk(self.root):

            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'TEMPLATES':
                templatesNodeToReplace = node
                templatesNodeIndex = self.root.body.index(node)

                templatesNode = ast.parse(LITERAL_TEMPLATES).body[0]

                ast.copy_location(templatesNode,
                                  templatesNodeToReplace)
                self.root.body.remove(templatesNodeToReplace)
                self.root.body.insert(
                    templatesNodeIndex, templatesNode)
                self.logger.log_info("Added TEMPLATES.")

    def _add_database(self) -> None:
        """
        This method modifies the 'DATABASES' dict within the settings.py file to configure database settings
        according to the specified 'dbType'. It supports 'mysql' and 'postgres' database types.
        """

        if self.dbType == "mysql":
            # If it creates the db, and the user with grant
            if setup_mysql(self.projectName, self.logger):
                for node in ast.walk(self.root):
                    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'DATABASES':
                        databasesToReplace = node
                        databasesIndex = self.root.body.index(node)

                databasesNode = ast.parse(LITERAL_MYSQL).body[0]

                ast.copy_location(databasesNode, databasesToReplace)
                self.root.body.remove(databasesToReplace)
                self.root.body.insert(databasesIndex, databasesNode)
                self.logger.log_info("Added DATABASES (MySQL).")
            else:
                self.logger.log_error("Couldn't create the MySQL database.")

        elif self.dbType == "postgre":
            if setup_postgre(self.projectName, self.logger):
                for node in ast.walk(self.root):
                    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'DATABASES':
                        databasesToReplace = node
                        databasesIndex = self.root.body.index(node)

                databasesNode = ast.parse(LITERAL_POSTGRESQL).body[0]

                ast.copy_location(databasesNode, databasesToReplace)
                self.root.body.remove(databasesToReplace)
                self.root.body.insert(databasesIndex, databasesNode)
                self.logger.log_info("Added DATABASES (PostgreSQL).")
            else:
                self.logger.log_error(
                    "Couldn't create the PostgreSQL database.")

    def _add_static_root(self) -> None:
        for node in ast.walk(self.root):

            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'STATIC_URL':
                staticUrlNodeIndex = self.root.body.index(node)

                staticRootNode = ast.parse(LITERAL_STATIC_ROOT).body[0]
                self.root.body.insert(staticUrlNodeIndex, staticRootNode)
                self.logger.log_info("Added STATIC_ROOT.")

    def _add_static_files_dirs(self) -> None:
        for node in ast.walk(self.root):

            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'STATIC_URL':
                staticFilesDirIndex = self.root.body.index(node)

                staticFilesDirNode = ast.parse(
                    LITERAL_STATICFILES_DIRS).body[0]
                self.root.body.insert(
                    staticFilesDirIndex + 1, staticFilesDirNode)
                self.logger.log_info("Added STATICFILES_DIRS.")

    def _add_comments(self):
        """This method will use AST to add comments to the settings.py file."""
        return NotImplementedError

    # Start:
    def edit(self):
        """    
        Edit the settings.py file by performing various modifications and formatting.
        This method performs the following operations:

        1. Parse the settings.py file.
        2. Add necessary imports.
        3. Add the BASE_DIR contant to the settings.py
        4. Add the ROOT_DIR constant to the settings.py
        5. Add the ENV constant to the settings.py
        6. Add the SECRET_KEY constant to the settings.py
        7. Add the DEBUG constant to the settings.py
        8. Add the ASSETS_ROOT constant to the settings.py
        9. Add the ALLOWED_HOSTS constant to the settings.py
        10. Add the CSRF_TRUSTED_ORIGINS constant to the settings.py
        11. Add the INSTALLED_APPS constant to the settings.py
        12. Add the MIDDLEWARE constant to the settings.py
        13. Add the TEMPLATE_DIR constant to the settings.py
        14. Add the TEMPLATES constant to the settings.py
        15. Add the DATABASES constant to the settings.py
        16. Add the STATIC_ROOT constant to the settings.py
        17. Add the STATICFILES_DIRS constant to the settings.py
        18. Save the settings.py file.
        20. Format the settings.py file with yapf.

        Returns:
            None
        """

        # Parse the settings.py
        self.root = self.parse_file()

        # In order:
        self._add_imports()
        self._add_base_dir()
        self._add_root_dir()
        self._add_env()
        self._add_secret_key()
        self._add_debug()
        self._add_assets_root()
        self._add_allowed_hosts()
        self._add_csrf_trusted()
        self._add_installed_apps()
        self._add_middleware()
        self._add_template_dir()
        self._add_templates()
        self._add_database()
        self._add_static_root()
        self._add_static_files_dirs()

        setup_extra_dirs(self.logger)

        # Save file and make other edits after it
        self.unparse_and_save_file()

        self.add_blank_lines()
        self.format_file()


def setup_extra_dirs(logger: Logger) -> None:
    """
    Create necessary directories and files for the project's static, assets and templates.

    This method creates the following directories and files:

    - 'staticfiles': for root static files.
    - 'apps/templates/layouts': for template layout files.
    - 'apps/templates/layouts/base.html': an empty base HTML template file.
    - 'apps/static/assets': directory for the apps static files.
    - 'apps/static/assets/css': directory for CSS files.
    - 'apps/static/assets/js': directory for JavaScript files.
    - 'apps/static/assets/img': directory for image files.

    If any of these directories or files already exist, they will not be recreated.

    Returns:
        None
    """

    # Static root in settings.py
    os.makedirs('staticfiles',  exist_ok=True)

    # Templates dir
    os.makedirs('apps/templates/layouts', exist_ok=True)

    # create a base.html file
    with open('apps/templates/layouts/base.html', 'w') as f:
        f.write("<!DOCTYPE html>\n")

    # Assets dirs
    os.makedirs('apps/static/assets', exist_ok=True)
    os.makedirs('apps/static/assets/css',  exist_ok=True)
    os.makedirs('apps/static/assets/js',  exist_ok=True)
    os.makedirs('apps/static/assets/img',  exist_ok=True)

    logger.log_info("Created necessary directories and files.")


def setup_mysql(projectName: str, logger: Logger) -> bool:
    """
    This function installs MySQL, sets up MySQL, creates a user with privileges, creates a database, and saves the credentials to the '.env' file. 

    Args:
        projectName (str): Project name
        logger (Logger): Logger instance

    Returns:
        bool: True if docker started, user created with grant and saved credentials in the 
    """
    try:
        envVariables = {
            'CONTAINER_NAME': f"{projectName}",
            'DATABASE_TYPE': "mysql",
            'MYSQL_HOST': f"{MYSQL_HOST}",
            'MYSQL_PORT': f"{MYSQL_PORT}",
            'MYSQL_USER': f"{MYSQL_USER}",
            'MYSQL_PASSWORD': f"{MYSQL_PASSWORD}",
            'MYSQL_ROOT_PASSWORD': f"{MYSQL_ROOT_PASSWORD}"
        }

        command = f"./databases.sh"
        subprocess.run(
            command, shell=True, check=True, start_new_session=True, env=envVariables)

        with open('.env', 'a') as env:
            env.write(f"MYSQL_NAME='{projectName}'\n")
            env.write(f"MYSQL_HOST='{MYSQL_HOST}'\n")
            env.write(f"MYSQL_PORT='{MYSQL_PORT}'\n")
            env.write(f"MYSQL_USER='{MYSQL_USER}'\n")
            env.write(f"MYSQL_PASSWORD='{MYSQL_PASSWORD}'\n")
            env.write(f"MYSQL_ROOT_PASSWORD='{MYSQL_ROOT_PASSWORD}'\n\n")
            logger.log_info("Added MySQL credentials to '.env'.")

        return True

    except Exception as e:
        print(f"{e=}")
        return False


def setup_postgre(projectName: str, logger: Logger) -> bool:
    """
    This function installs MySQL, sets up MySQL, creates a user with privileges, creates a database, and saves the credentials to the '.env' file. 

    Args:
        projectName (str): Project name
        logger (Logger): Logger instance

    Returns:
        bool: True if docker started, user created with grant and saved credentials in the 
    """
    try:
        envVariables = {
            'CONTAINER_NAME': f"{projectName}",
            'DATABASE_TYPE': "postgre",
            'POSTGRESQL_HOST': f"{POSTGRESQL_HOST}",
            'POSTGRESQL_PORT': f"{POSTGRESQL_PORT}",
            'POSTGRESQL_USER': f"{POSTGRESQL_USER}",
            'POSTGRESQL_PASSWORD': f"{POSTGRESQL_PASSWORD}",
            'POSTGRESQL_ROOT_PASSWORD': f"{POSTGRESQL_ROOT_PASSWORD}"
        }

        command = f"./databases.sh"
        subprocess.run(
            command, shell=True, check=True, start_new_session=True, env=envVariables)

        with open('.env', 'a') as env:
            env.write(f"POSTGRESQL_NAME='{projectName}'\n")
            env.write(f"POSTGRESQL_HOST='{POSTGRESQL_HOST}'\n")
            env.write(f"POSTGRESQL_PORT='{POSTGRESQL_PORT}'\n")
            env.write(f"POSTGRESQL_USER='{POSTGRESQL_USER}'\n")
            env.write(f"POSTGRESQL_PASSWORD='{POSTGRESQL_PASSWORD}'\n")
            env.write(
                f"POSTGRESQL_ROOT_PASSWORD='{POSTGRESQL_ROOT_PASSWORD}'\n\n")
            logger.log_info("Added PostgreSQL credentials to '.env'.")

        return True

    except Exception as e:
        print(f"{e=}")
        return False


if __name__ == "__main__":
    settingsPath = sys.argv[1] if sys.argv[1] else None
    dbType = sys.argv[2] if sys.argv[2] else None
    projectName = sys.argv[3] if sys.argv[3] else None

    EditSettings(settingsPath=settingsPath, dbType=dbType,
                 projectName=projectName).edit()
