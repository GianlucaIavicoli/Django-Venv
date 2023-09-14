# Django Setup

This repository contains a set of Python and Bash scripts designed to simplify the process of setting up a development environment for Django projects. Whether you are a seasoned Django developer or just starting out, these scripts aim to streamline common tasks and make it easier to get your Django project up and running quickly.

<!-- TABLE OF CONTENTS -->

## Table of Contents

<ol>
  <li>
    <a href="#django-setup">About The Project</a>
    <ul>
      <li><a href="#features">Features</a></li>
      <li><a href="#built-with">Built With</a></li>
    </ul>
  </li>
  <li>
    <a href="#getting-started">Getting Started</a>
    <ul>
      <li><a href="#prerequisites">Prerequisites</a></li>
      <li><a href="#installation">Installation</a></li>
      <li><a href="#usage">Usage</a></li>
      <li><a href="#command-line-options">Command-Line Options</a></li>
      <li><a href="#usage-example">Usage Example</a></li>
    </ul>
  </li>
  <li><a href="#upcoming-features">Upcoming Features</a></li>
  <li><a href="#code-of-conduct">Code of Conduct</a></li>
  <li><a href="#contributing">Contributing</a></li>
  <li><a href="#license">License</a></li>
  <li><a href="#acknowledgments">Acknowledgments</a></li>
</ol>



## Features
Djando-Setup provides the following features:

1. **Virtual Environment Setup**: Automatically creates a virtual environment and installs project dependencies.

2. **Django Project Initialization**: Automates the creation of a Django project, along with additional directories and files such as static files, apps directory, and a base.html template.

3. **Django Settings Configuration**: Edits the `settings.py` file to include various settings, including database configuration (MySQL, PostgreSQL) with docker, htmx setup, SMTP configuration, and other common settings.

4. **Database Setup**: Users have the option to either utilize their own server or have the script generate a Docker container for the specified database. When opting for MySQL or other compatible databases, the script will endeavor to create a Docker container with your chosen database, establish a user profile with the requisite permissions, set up a database, and store the credentials securely in an .env file.

## Built With

![LINUX](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
<!--![ApacheCassandra](https://img.shields.io/badge/cassandra-%231287B1.svg?style=for-the-badge&logo=apache-cassandra&logoColor=white)-->
<p align="right">(<a href="#django-setup">back to top</a>)</p>


## Getting Started 

### Prerequisites

Before you begin, please ensure that you have the following dependencies installed on your system:

- **Linux Operating System**: Djando-Setup is designed to work on Linux-based systems.

- **Docker**: Djando-Setup relies on Docker for certain functionality. Make sure you have Docker installed on your machine. You can find installation instructions for Docker on the [Docker website](https://docs.docker.com/get-docker/).

Once you have these dependencies in place, you can proceed with the installation and usage of Djando-Setup.
<p align="right">(<a href="#django-setup">back to top</a>)</p>


### Installation
To get started, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/GianlucaIavicoli/Django-Setup.git
   ```

2. Enter the project directory:

   ```bash
   cd Django-Setup
   ```

3. Make the script executable by running the following command in the project directory:

   ```bash
   chmod +x script.sh databases.sh
   ```

### Usage
Run the script to set up your Django project:

   ```bash
   ./script.sh <project_name>
   ```

### Command-Line Options
```bash
./script.sh <project_name> [OPTIONS]

Options:
    -h, --help                       Display this help message
    -d, --database <database_type>   Specify the database type (required)
                                     Choose between 'mysql' or 'postgre'
    --smtp                           Configure SMTP settings in settings.py
    --htmx                           Configure HTMX settings in settings.py
```
<p align="right">(<a href="#django-setup">back to top</a>)</p>

### Usage Example
   ```bash
   ./script.sh <project_name> -d mysql --htmx --smtp
   ```
  This will generate [settings.py](./example.settings.py), an '.env' file with all the credentials, a locally running MySQL Docker container if the database is not specified, as well as all the static directories and application directories for the Django project.

<p align="right">(<a href="#django-setup">back to top</a>)</p>

## Upcoming Features

1. **Cassandra Support with Docker**: Integrate support for Cassandra databases with Docker.
2. **Scylla Support with Docker**: Extend our Docker support to include Scylla, a highly available NoSQL database compatible with Apache Cassandra. 
<p align="right">(<a href="#django-setup">back to top</a>)</p>

## Code of Conduct

Please review our [Code of Conduct](./CODE_OF_CONDUCT.md) before contributing to Django-Setup.
<p align="right">(<a href="#django-setup">back to top</a>)</p>

## Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for more information.
<p align="right">(<a href="#django-setup">back to top</a>)</p>

## License
Distributed under the Apache-2.0 license. See LICENSE for more information.
<p align="right">(<a href="#django-setup">back to top</a>)</p>

## Acknowledgments

* [Yapf Python formatter](https://github.com/google/yapf)
* [ast-comments](https://github.com/t3rn0/ast-comments)

<p align="right">(<a href="#django-setup">back to top</a>)</p>
