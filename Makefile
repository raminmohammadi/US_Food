PYTHON := python3
UV := uv
ENV_DIR := .venv

.PHONY: install clean run lint

# Create virtual environment and install dependencies
install:
	$(UV) venv $(ENV_DIR)
	$(UV) pip install -r requirements.txt --python $(ENV_DIR)/bin/python

# Remove virtual environment and all caches
clean:
	rm -rf $(ENV_DIR)
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '.ipynb_checkpoints' -type d -exec rm -r {} +


run:
	$(ENV_DIR)/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Lint code using Ruff
lint:
	$(ENV_DIR)/bin/pip install ruff
	$(ENV_DIR)/bin/ruff check .


# Remove virtual environment and all caches
clean:
	rm -rf $(ENV_DIR)
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '.ipynb_checkpoints' -type d -exec rm -r {} +
