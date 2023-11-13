# This is a simple Makefile for Python projects

.PHONY: clean test

clean:
	@echo "Cleaning up __pycache__ directories and .pyc files..."
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type f -name "*.pyc" -delete

test:
	@echo "Running tests..."
	python -m unittest discover -s tests

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

run:
	@echo "Running the application..."
	@export APP_PORT=$${APP_PORT:-9111}; \
	if ! echo $$APP_PORT | egrep -q '^[0-9]+$$'; then \
		export APP_PORT=9111; \
	fi; \
	echo "Using port $$APP_PORT"; \
	uvicorn src.main:app --reload --host 0.0.0.0 --port $$APP_PORT --log-level debug

start:
	@make run
