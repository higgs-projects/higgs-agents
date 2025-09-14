# Higgs Agents Backend API

## Usage
1. Create environment.

   Higgs Agents API service uses [UV](https://docs.astral.sh/uv/) to manage dependencies.
   First, you need to add the uv package manager, if you don't have it already.

   ```bash
   pip install uv
   # Or on macOS
   brew install uv
   ```

1. Install dependencies

   ```bash
   uv sync --dev
   ```

1. Run migrate

   Before the first launch, migrate the database to the latest version.

   ```bash
   uv run alembic  -c ./migrations/alembic.ini upgrade head
   ```

1. Start backend

   ```bash
   uv run fastapi dev app.py --host 0.0.0.0 --port 7777
   ```

1. Start Dify [web](../web) service.

1. Setup your application by visiting `http://localhost:3000`.

1. If you need to handle and debug the async tasks (e.g. dataset importing and documents indexing), please start the worker service.