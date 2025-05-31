#!/usr/bin/env bash

set -e
set -x

uv run openapi-python-client generate \
--url http://localhost:8000/openapi.json \
--meta none \
--output-path app/client \
--overwrite \
--config openapi-python-client.yaml
