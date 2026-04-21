.PHONY: install ingest run test

install:
	pip install -r requirements.txt

ingest:
	python scripts/ingest_docs.py

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q
