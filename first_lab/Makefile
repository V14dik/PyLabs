.PHONY: all venv

# Set the main shell for executing tasks.
SHELL := /bin/bash

SOURCES := $(shell find . -name '*.py' -not -path '*./.venv/*' -not -path '*./.git/*' -print)

all: lint

venv: .venv/bin/activate
.venv/bin/activate: requirements.txt
	@python3 -m venv ./.venv

	# Install the required python packages inside a new virtual environment.
	@.venv/bin/python -m pip install -r requirements.txt

	@touch .venv/bin/activate

black: venv
	@.venv/bin/black --target-version=py38 --line-length=100 -- $(SOURCES)

lint: venv
	# Stage #1.
	-.venv/bin/pylint -- $(SOURCES)

	# Stage #2.
	-.venv/bin/flake8 -- $(SOURCES)
