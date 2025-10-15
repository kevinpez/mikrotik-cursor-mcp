# Makefile for MikroTik Cursor MCP
.PHONY: help test test-unit test-integration test-chr test-container test-golden test-all clean setup

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Setup development environment
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -e .
	.venv/bin/pip install pytest pytest-cov pytest-asyncio pytest-mock

test-unit: ## Run unit tests
	.venv/bin/python -m pytest tests/unit/ -v --cov=mcp_mikrotik --cov-report=term-missing

test-integration: ## Run integration tests
	.venv/bin/python -m pytest tests/integration/ -v

test-chr: ## Run CHR integration tests
	.venv/bin/python -m pytest tests/integration/test_chr_integration.py -v

test-container: ## Run container integration tests
	cd routeros-docker && docker-compose up -d
	sleep 30
	.venv/bin/python -m pytest tests/integration/test_container_integration.py -v
	cd routeros-docker && docker-compose down

test-golden: ## Run golden file tests
	.venv/bin/python -m pytest tests/integration/test_golden_files.py -v

test-performance: ## Run performance tests
	.venv/bin/python -m pytest tests/performance/ -v

test-security: ## Run security tests
	.venv/bin/python -m pytest tests/security/ -v

test-all: test-unit test-integration test-container test-golden ## Run all tests

test-coverage: ## Generate coverage report
	.venv/bin/python -m pytest tests/ --cov=mcp_mikrotik --cov-report=html --cov-report=xml
	@echo "Coverage report generated in htmlcov/"

test-watch: ## Run tests in watch mode
	.venv/bin/python -m pytest-watch tests/ -- -v

clean: ## Clean up test artifacts
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf test-results.xml
	cd routeros-docker && docker-compose down -v

lint: ## Run linting
	.venv/bin/flake8 src/mcp_mikrotik/
	.venv/bin/black --check src/mcp_mikrotik/
	.venv/bin/mypy src/mcp_mikrotik/

format: ## Format code
	.venv/bin/black src/mcp_mikrotik/
	.venv/bin/isort src/mcp_mikrotik/

docker-test: ## Run tests in Docker
	docker build -t mikrotik-mcp-test .
	docker run --rm mikrotik-mcp-test make test-all

ci-test: ## Run CI test suite
	.venv/bin/python -m pytest tests/ --cov=mcp_mikrotik --cov-report=xml --junitxml=test-results.xml

benchmark: ## Run performance benchmarks
	.venv/bin/python -m pytest tests/performance/ --benchmark-only --benchmark-save=benchmark_results

update-golden: ## Update golden files with current outputs
	.venv/bin/python scripts/update_golden_files.py

install: ## Install the package
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e .
	pip install pytest pytest-cov pytest-asyncio pytest-mock black flake8 mypy

build: ## Build the package
	python -m build

publish: ## Publish to PyPI
	python -m twine upload dist/*

version: ## Show version information
	@python -c "import mcp_mikrotik; print(f'Version: {mcp_mikrotik.__version__}')"

docs: ## Generate documentation
	.venv/bin/sphinx-build -b html docs/ docs/_build/html

serve-docs: ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000

check-deps: ## Check for outdated dependencies
	.venv/bin/pip list --outdated

update-deps: ## Update dependencies
	.venv/bin/pip install --upgrade -r requirements.txt

security-scan: ## Run security scan
	.venv/bin/bandit -r src/mcp_mikrotik/

type-check: ## Run type checking
	.venv/bin/mypy src/mcp_mikrotik/

test-integration-full: ## Run full integration test suite
	@echo "Starting full integration test suite..."
	@echo "1. Setting up test environment..."
	make setup
	@echo "2. Running unit tests..."
	make test-unit
	@echo "3. Running integration tests..."
	make test-integration
	@echo "4. Running container tests..."
	make test-container
	@echo "5. Running golden file tests..."
	make test-golden
	@echo "6. Running performance tests..."
	make test-performance
	@echo "7. Running security tests..."
	make test-security
	@echo "8. Generating coverage report..."
	make test-coverage
	@echo "All tests completed successfully!"

test-quick: ## Run quick test suite (unit + basic integration)
	.venv/bin/python -m pytest tests/unit/ tests/integration/test_basic.py -v

test-smoke: ## Run smoke tests (basic connectivity)
	.venv/bin/python -m pytest tests/integration/test_smoke.py -v

test-regression: ## Run regression tests
	.venv/bin/python -m pytest tests/regression/ -v

test-api: ## Run API tests
	.venv/bin/python -m pytest tests/api/ -v

test-multi-site: ## Run multi-site manager tests
	.venv/bin/python -m pytest multi-site-manager/tests/ -v

validate-config: ## Validate configuration files
	.venv/bin/python -c "import yaml; yaml.safe_load(open('mcp-config.json.example'))"
	.venv/bin/python -c "import yaml; yaml.safe_load(open('multi-site-manager/sites.yaml.example'))"

check-format: ## Check code formatting
	.venv/bin/black --check src/mcp_mikrotik/
	.venv/bin/isort --check-only src/mcp_mikrotik/

fix-format: ## Fix code formatting
	.venv/bin/black src/mcp_mikrotik/
	.venv/bin/isort src/mcp_mikrotik/

pre-commit: ## Run pre-commit checks
	make check-format
	make lint
	make type-check
	make test-quick

pre-push: ## Run pre-push checks
	make pre-commit
	make test-integration
	make security-scan

release-check: ## Run release checks
	make pre-push
	make test-all
	make docs
	make build

# Development helpers
dev-setup: ## Setup development environment with all tools
	make setup
	make install-dev
	@echo "Development environment ready!"

dev-test: ## Run tests in development mode
	MIKROTIK_LOG_LEVEL=DEBUG .venv/bin/python -m pytest tests/ -v -s

dev-watch: ## Watch for changes and run tests
	.venv/bin/pytest-watch tests/ -- -v

dev-debug: ## Run with debug logging
	MIKROTIK_LOG_LEVEL=DEBUG .venv/bin/python -m pytest tests/ -v -s --log-cli-level=DEBUG

# Docker helpers
docker-build: ## Build Docker image
	docker build -t mikrotik-cursor-mcp .

docker-run: ## Run Docker container
	docker run -it --rm mikrotik-cursor-mcp

docker-test: ## Run tests in Docker
	docker run --rm mikrotik-cursor-mcp make test-all

# Multi-site manager helpers
multi-site-test: ## Test multi-site manager
	cd multi-site-manager && python -m pytest tests/ -v

multi-site-setup: ## Setup multi-site manager
	cd multi-site-manager && pip install -r requirements.txt

multi-site-example: ## Run multi-site manager example
	cd multi-site-manager && python site_manager.py status

# Documentation helpers
docs-build: ## Build documentation
	.venv/bin/sphinx-build -b html docs/ docs/_build/html

docs-serve: ## Serve documentation
	cd docs/_build/html && python -m http.server 8000

docs-clean: ## Clean documentation
	rm -rf docs/_build/

# Cleanup helpers
clean-all: ## Clean everything
	make clean
	make docs-clean
	rm -rf .venv/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	cd routeros-docker && docker-compose down -v --remove-orphans

# Status helpers
status: ## Show project status
	@echo "MikroTik Cursor MCP Status:"
	@echo "=========================="
	@echo "Python version: $$(python --version)"
	@echo "Virtual env: $$(if [ -d .venv ]; then echo 'Active'; else echo 'Not found'; fi)"
	@echo "Dependencies: $$(if [ -f .venv/pyvenv.cfg ]; then echo 'Installed'; else echo 'Not installed'; fi)"
	@echo "Tests: $$(if [ -d tests ]; then echo 'Available'; else echo 'Not found'; fi)"
	@echo "Docker: $$(if command -v docker >/dev/null 2>&1; then echo 'Available'; else echo 'Not found'; fi)"

# Help for specific categories
help-test: ## Show test-related help
	@echo "Test-related targets:"
	@echo "  test-unit        - Run unit tests"
	@echo "  test-integration - Run integration tests"
	@echo "  test-container   - Run container tests"
	@echo "  test-chr         - Run CHR tests"
	@echo "  test-golden      - Run golden file tests"
	@echo "  test-performance - Run performance tests"
	@echo "  test-security    - Run security tests"
	@echo "  test-all         - Run all tests"
	@echo "  test-coverage    - Generate coverage report"

help-dev: ## Show development-related help
	@echo "Development-related targets:"
	@echo "  setup            - Setup development environment"
	@echo "  dev-setup        - Setup with all development tools"
	@echo "  dev-test         - Run tests in development mode"
	@echo "  dev-watch        - Watch for changes and run tests"
	@echo "  dev-debug        - Run with debug logging"
	@echo "  format           - Format code"
	@echo "  lint             - Run linting"
	@echo "  type-check       - Run type checking"

help-docker: ## Show Docker-related help
	@echo "Docker-related targets:"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-run       - Run Docker container"
	@echo "  docker-test      - Run tests in Docker"
	@echo "  test-container   - Run container integration tests"

help-docs: ## Show documentation-related help
	@echo "Documentation-related targets:"
	@echo "  docs-build       - Build documentation"
	@echo "  docs-serve       - Serve documentation locally"
	@echo "  docs-clean       - Clean documentation"

# Default target
.DEFAULT_GOAL := help
