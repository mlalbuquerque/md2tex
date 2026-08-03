.PHONY: install dev test lint example clean

install:
	python3 -m pip install .

dev:
	python3 -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

example:
	netra-md2tex examples/relatorio.md --output build/relatorio.tex --force

clean:
	rm -rf build dist .pytest_cache .ruff_cache .coverage htmlcov src/*.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
