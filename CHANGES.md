# Clean up and separate sync functionality

**Version**: v0.1.0

**Date:** 07/07/2025

## Additions

**`/pyproject.toml`**:

* Added `datamodel-code-generator[http]` as a dev dependency to generate the sync client Pydantic models.

**`/scripts/generate-client.sh`**:

* Added `datamodel-codegen` as a step in generating the client.

**`/app/serversync/`**:

* Added abstraction to the generated client as a simpler way to sync with the server.

**`/app/controllers/tabs/passwords.py`**:

* Added a way to optionally retrieve a loaded client.

## Changes

**`/app/localdb/synced_db.py`**:

* Removed `SyncedDatabase` implementation to separate the sync and the database.

**`/app/controllers/apps.py`**:

* Changed to handle disabling/enabling and switching to tabs directly instead of letting the controllers do it.

**`/app/controllers/tabs/databases.py`**:

* Removed code to initialize the sync client and moved it to `sync_client.py`.

## Misc

* Separating the network code from the database code will make it easier to track unsynced changes
  and syncing with the server by allowing the controller to know what is happening.
* Actually implementing the sync code will take a while so this is only one step.
