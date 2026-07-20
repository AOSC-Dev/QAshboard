#! /usr/bin/env bash

set -euo pipefail

cd "$(dirname -- "${BASH_SOURCE[0]}")/../frontend"
uv run --directory=../backend python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > openapi.json
pnpm generate-client
rm openapi.json
