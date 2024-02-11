# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Tech Stack

-   Python : https://www.python.org/
-   PostgreSQL (Database) : https://github.com/postgres/postgres
-   Docker (Container) : https://www.docker.com/

## Framework & Library

-   Flask (HTTP Framework) : https://flask.palletsprojects.com/en/3.0.x/
-   Flask SQLAlchemy (ORM) : https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
-   Flask JWT (Authentication) : https://flask-jwt-extended.readthedocs.io/en/stable/
-   Flask Bcrypt (Hashing) : https://flask-bcrypt.readthedocs.io/en/1.0.1/
-   Pydantic-Settings (Configuration) : https://docs.pydantic.dev/latest/concepts/pydantic_settings/
-   Pydantic (Validation) : https://docs.pydantic.dev/latest/
-   Loguru (Logging) : https://github.com/Delgan/loguru

## Requirements to use the cookiecutter template:

-   Python 3.9+
-   [Cookiecutter python package](http://cookiecutter.readthedocs.org/en/latest/installation.html)
-   [Poetry python package](https://python-poetry.org/)

```bash
$ pip install cookiecutter
$ pip install poetry
```

or

```bash
$ conda install cookiecutter
$ conda install poetry
```

## To start a new project, run:

```bash
cookiecutter https://github.com/JordanMarcelino/cookiecutter-full-stack-flask.git
```

## Installing development requirements

```bash
$ poetry build
```
