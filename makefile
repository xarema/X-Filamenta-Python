fmt-py:
	ruff format .

lint-py:
	ruff check .
	mypy backend/src

test-py:
	pytest -q --disable-warnings --maxfail=1 --cov=backend/src --cov-report=term-missing

# Front targets
fmt-front:
	npm run fmt

lint-front:
	npm run lint

# Convenience aggregates
fmt: fmt-py fmt-front

lint: lint-py lint-front

test: test-py
