.PHONY: help install install-dev test test-coverage lint format clean build docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install        Install production dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo "  test          Run all tests"
	@echo "  test-coverage Run tests with coverage report"
	@echo "  lint          Run all linting tools"
	@echo "  format        Format code with black and isort"
	@echo "  clean         Clean build artifacts"
	@echo "  build         Build package"
	@echo "  docker-build  Build Docker image"
	@echo "  docker-run    Run Docker container"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

# Testing
test:
	pytest tests/ -v

test-coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

# Code quality
lint:
	black --check src/ tests/
	isort --check-only src/ tests/
	pylint src/
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

# Security
security:
	bandit -r src/
	safety check

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	python -m build

# Docker
docker-build:
	docker build -t wyscout-scraper:latest .

docker-run:
	docker-compose up --build

# Development
dev-setup: install-dev
	@echo "Development environment ready!"
	@echo "Run 'make test' to verify installation"

# Release
release: lint test build
	@echo "Ready for release!"
	@echo "Run 'twine upload dist/*' to publish to PyPI"