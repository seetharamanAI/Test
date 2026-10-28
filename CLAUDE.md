# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup (first time)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# Run the dev server (reads FLASK_APP from .flaskenv)
flask run

# Run the full test suite
pytest

# Run a single test
pytest tests/test_routes.py::test_index
```

There is no linter/formatter configured yet.

## Architecture

This is a minimal Flask app built with the application-factory pattern:

- `app/__init__.py` — `create_app()` factory. Builds the `Flask` instance, loads config, and registers blueprints. New blueprints must be imported and registered here.
- `app/config.py` — config classes (`Config`, `DevelopmentConfig`, `TestingConfig`). `create_app()` takes a config class as an argument; tests pass `TestingConfig` (see `tests/conftest.py`).
- `app/routes.py` — the `main_bp` blueprint holding view functions. As routes grow, split them into additional blueprints registered in `create_app()` rather than growing this file indefinitely.
- `app/templates/` — Jinja2 templates, rendered via `render_template`.
- `wsgi.py` — entry point that calls `create_app()`; used by `flask run` and WSGI servers.

Tests (`tests/`) use pytest with fixtures in `conftest.py`: the `app` fixture creates an app via the factory with `TestingConfig`, and `client` gives a Flask test client built from it. `pyproject.toml` sets `pythonpath = ["."]` so `app` is importable from the test suite without installing the package.
