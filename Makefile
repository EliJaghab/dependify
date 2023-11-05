.PHONY: format

format:
	black . --exclude venv
	isort . --skip venv
	flake8 . --exclude venv
