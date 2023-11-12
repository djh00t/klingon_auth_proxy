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
	python src/app.py

start:
	@make run
