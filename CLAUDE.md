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
- `app/quiz.py` — the `quiz_bp` blueprint (mounted at `/quiz`) implementing the cricket trivia quiz. Progress is tracked server-side in the Flask `session` (`quiz_index`, `quiz_score`); `/quiz/` resets it and redirects into `/quiz/question`, which renders the current question on GET and grades the submitted choice on POST before advancing, redirecting to `/quiz/result` once all questions are answered.
- `app/quiz_data.py` — the `QUESTIONS` list (question/choices/answer index) consumed by `app/quiz.py`. Add trivia here rather than hardcoding it in the blueprint.
- `app/templates/` — Jinja2 templates, rendered via `render_template`. `base.html` is the shared layout; page templates extend it with `{% block content %}`. Quiz-specific templates live under `app/templates/quiz/`.
- `wsgi.py` — entry point that calls `create_app()`; used by `flask run` and WSGI servers.

Tests (`tests/`) use pytest with fixtures in `conftest.py`: the `app` fixture creates an app via the factory with `TestingConfig`, and `client` gives a Flask test client built from it. `pyproject.toml` sets `pythonpath = ["."]` so `app` is importable from the test suite without installing the package. `tests/test_quiz.py` drives the quiz through its session-based flow using `client.session_transaction()` to assert on session state directly.
