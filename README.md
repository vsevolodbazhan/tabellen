# Tabellen

[![CodeFactor](https://www.codefactor.io/repository/github/vsevolodbazhan/tabellen/badge)](https://www.codefactor.io/repository/github/vsevolodbazhan/tabellen)
[![Requirements Status](https://requires.io/github/vsevolodbazhan/tabellen/requirements.svg?branch=master)](https://requires.io/github/vsevolodbazhan/tabellen/requirements/?branch=master)

A microservice for sending messages to clients from Google Sheets.

## Installation

Install dependencies using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install -r requirements.txt
```

or [Poetry](https://python-poetry.org):

```bash
poetry install
```

Poetry will install dev-dependencies as well. So use that if you are planning to contribute.

## Usage

Run the server:

```bash
make run_server
```

and run the Celery worker in the separate process:

```bash
make run_celery
```

You might want to activate shell first with:

```bash
poetry shell
```

## Docs

Docs can be found in `docs` folder.

To generate the new docs use:

```
make docs
```

## Tests

Run tests using `pytest`:

```bash
make test
```

## License

[GNU GPLv3](https://github.com/vsevolodbazhan/tabellen/blob/master/LICENSE)
