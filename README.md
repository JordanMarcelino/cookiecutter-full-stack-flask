# Cookiecutter Full Stack Flask

_Full stack flask template with lot of features provided._

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

## How to get email application password?
- Open your google account settings
- Search for application password
- Enter the application name and you will received the secret key

## To start a new project, run:

```bash
cookiecutter https://github.com/JordanMarcelino/cookiecutter-full-stack-flask.git
```

[![asciicast](https://asciinema.org/a/cWDQIp7Gh7j0gWEKA2mCjapJ2.svg)](https://asciinema.org/a/cWDQIp7Gh7j0gWEKA2mCjapJ2)

### The resulting directory structure

---

The directory structure of your new project looks like this:

```
├── LICENSE
├── .env               <- Environment variables for the application
├── pyproject.toml     <- Poetry dependencies
├── .gitignore         <- .gitignore file for ignoring specific files
├── README.md          <- The top-level README for developers using this project.
├── deploy             <- Docker configuration for building the docker container
│
├── flaskr             <- A default Sphinx project; see sphinx-doc.org for details
│   ├── __init__.py    <- Makes flaskr a Python module
│   ├── extensions.py  <- Flask extensions
│   ├── api            <- Scripts to create REST API
│   ├── core           <- Scripts to create application utilities
│   ├── entity         <- Scripts to create database schemas
│   ├── forms          <- Scripts to create flask forms
│   ├── repository     <- Scripts to create repository layer to communicate with database
│   ├── schemas        <- Scripts to create http request & response schemas
│   ├── static         <- Static files
│   ├── templates      <- HTML file to render
│   ├── views          <- Scripts to create view layer
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── instance           <- Temporary sqlite database for testing application
│
├── tests              <- Folder that contains unit testing for the application
```

## Installing development requirements

```bash
poetry install
```

## Running the tests

```bash
pytest -v
```

## Credit

-   https://github.com/drivendata/cookiecutter-data-science
-   https://github.com/ashutoshkrris/Flask-User-Authentication-With-Email-Verification
