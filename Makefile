.PHONY: check

format:
	black .
	isort .
	flake8 .
