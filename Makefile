.PHONY: format

format:
	black .
	isort .
	flake8 .
