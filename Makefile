PY ?= python3

.PHONY: help install test validate today status report doctor clean

help:
	@echo "make install   - editable install + dev-deps"
	@echo "make test      - unit tests (unittest)"
	@echo "make validate  - inhoud van alle assessments valideren"
	@echo "make today     - vandaag se studieblok"
	@echo "make status    - voortgangsoverzicht"
	@echo "make report    - bewijsrapport genereren"
	@echo "make doctor    - omgevingscheck"

install:
	$(PY) -m pip install -e ".[dev]"

test:
	PYTHONPATH=src $(PY) -m unittest discover -s tests -v

validate:
	PYTHONPATH=src $(PY) -m aae validate

today:
	PYTHONPATH=src $(PY) -m aae today

status:
	PYTHONPATH=src $(PY) -m aae status

report:
	PYTHONPATH=src $(PY) -m aae report --write docs/PROGRESS.md

doctor:
	PYTHONPATH=src $(PY) -m aae doctor
