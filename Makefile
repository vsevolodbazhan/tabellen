PROJECT_NAME = tabellen
DOCS_DIR = docs

test:
	@pytest --cov=.

docs:
	@pdoc --html $(PROJECT_NAME) -o ./$(DOCS_DIR)

run_server:
	@gunicorn app:connexion_app

run_celery:
	@celery -A $(PROJECT_NAME).tasks worker

.PHONY: test run_server run_celery
