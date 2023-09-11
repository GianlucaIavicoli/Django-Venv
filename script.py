import ast
import subprocess
import sys
from typing import Union
from const import *


class EditSettings:
    def __init__(self, settingsPath: str, dbType: Union[str, None]):
        """
        Class for modifying a Django project's settings.py file.

        This class facilitates the addition of necessary imports, modifications to the database configuration, and fixes for code indentation.

        Args:
            settingsPath (str): Path to settings.py
            dbType (Union[str, None]): The type of database to use. It can be one of the following values: mysql, postgres or None.
        """

        self.settingsPath = settingsPath
        self.dbType = dbType

    def parse_file(self) -> ast.Module:
        with open(self.settingsPath, 'r') as f:
            fileContent = f.read()

        # Parse the settings.py
        return ast.parse(fileContent)

    def unparse_and_save_file(self) -> None:
        unparsedFile = ast.unparse(self.root)
        with open(self.settingsPath, 'w') as f:
            f.write(unparsedFile)

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

    def edit_database(self) -> None:
        """
        This method modifies the 'DATABASES' dict within the settings.py file to configure database settings
        according to the specified 'dbType'. It supports 'mysql' and 'postgres' database types.
        """

        if self.dbType == "mysql":
            for node in ast.walk(self.root):
                if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'DATABASES':
                    databaseDictToReplace = node
                    databaseDictIndex = self.root.body.index(node)

            getEnvName = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='os', ctx=ast.Load()),
                    attr='getenv',
                    ctx=ast.Load()
                ),
                args=[ast.Str('DB_NAME')],
                keywords=[]
            )
            getEnvUser = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='os', ctx=ast.Load()),
                    attr='getenv',
                    ctx=ast.Load()
                ),
                args=[ast.Str('MYSQL_USER')],
                keywords=[]
            )
            getEnvPass = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='os', ctx=ast.Load()),
                    attr='getenv',
                    ctx=ast.Load()
                ),
                args=[ast.Str('MYSQL_PASSWORD')],
                keywords=[]
            )
            getEnvHost = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='os', ctx=ast.Load()),
                    attr='getenv',
                    ctx=ast.Load()
                ),
                args=[ast.Str('MYSQL_HOST')],
                keywords=[]
            )
            getEnvPort = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='os', ctx=ast.Load()),
                    attr='getenv',
                    ctx=ast.Load()
                ),
                args=[ast.Str('MYSQL_PORT')],
                keywords=[]
            )

            # Define the entire DATABASES dictionary with os.getenv calls
            DATABASE_NODE = ast.Assign(
                targets=[ast.Name(id='DATABASES', ctx=ast.Store())],
                value=ast.Dict(
                    keys=[ast.Str('default')],
                    values=[
                        ast.Dict(
                            keys=[ast.Str('ENGINE'), ast.Str('NAME'), ast.Str('USER'), ast.Str(
                                'PASSWORD'), ast.Str('HOST'), ast.Str('PORT')],
                            values=[
                                ast.Str('django.db.backends.mysql'),
                                getEnvName,
                                getEnvUser,
                                getEnvPass,
                                getEnvHost,
                                getEnvPort
                            ]
                        )
                    ]
                )
            )

            print(ast.dump(DATABASE_NODE, indent=4))
            ast.copy_location(DATABASE_NODE, databaseDictToReplace)
            self.root.body.remove(databaseDictToReplace)
            self.root.body.insert(databaseDictIndex, DATABASE_NODE)

        elif self.dbType == "postgres":
            return NotImplementedError

    def add_imports(self) -> None:
        for index, module in enumerate(MODULES_TO_IMPORT):
            importNode = ast.Import(
                names=[ast.alias(name=module, asname=None)])
            self.lastLineAdd = index + 2

            self.root.body.insert(index + 2, importNode)

    def add_env(self) -> None:
        envNode = ast.Assign(
            targets=[ast.Name(id='env', ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id='environ', ctx=ast.Load()),
                                   attr='Env', ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(
                        arg='DEBUG',
                        value=ast.Tuple(
                            elts=[ast.Constant(value=bool, kind=None),
                                  ast.Constant(value=True, kind=None)],
                            ctx=ast.Load()
                        )
                    ),
                ],
            ),
        )

        print(ast.dump(envNode, indent=4))

        ast.copy_location(envNode, self.root)
        self.root.body.insert(1, envNode)

    def edit_settings(self):
        """    
        Edit the settings.py file by performing various modifications and formatting.
        This method performs the following operations:

        1. Parses the settings.py file into an Abstract Syntax Tree (AST).
        2. Edits the database configuration if a specific database type (dbType) is provided.
        3. Adds necessary imports to the settings.py file.
        4. Saves the modified AST back to the settings.py file.
        5. Adds blank lines between sections for improved readability.
        6. Formats the settings.py file for consistent code style using a code formatter.
        """

        # Parse the settings.py
        self.root = self.parse_file()

        # Various edits
        if dbType:
            self.edit_database()

        self.add_imports()
        # self.add_env()

        # Save file and make other edits after it
        self.unparse_and_save_file()

        self.add_blank_lines()
        self.format_file()


if __name__ == "__main__":
    try:
        settingsPath = sys.argv[1] if sys.argv[1] else None
        dbType = sys.argv[2] if sys.argv[2] else None
    except:
        dbType = None

    EditSettings(settingsPath=settingsPath, dbType=dbType).edit_settings()
