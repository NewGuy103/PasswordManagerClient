#!/usr/bin/env bash

set -e
set -x

uv run openapi-python-client generate \
--url http://localhost:8000/openapi.json \
--meta none \
--output-path app/client \
--overwrite \
--config openapi-python-client.yaml

uv run datamodel-codegen \
--url http://localhost:8000/openapi.json \
--output-model-type pydantic_v2.BaseModel \
--use-annotated \
--output app/serversync/models.py \
--use-union-operator \
--use-standard-collections \
--output-datetime-class AwareDatetime \
--use-non-positive-negative-number-constrained-types

uv run ruff check app/client --fix
uv run ruff format app/client

uv run ruff check app/serversync --fix
uv run ruff format app/serversync
