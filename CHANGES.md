# Add functionality for syncing database with the server

**Version**: v0.1.0

**Date:** 02/08/2025

## Additions

**`/app/controllers/tabs/settings.py`**:

* Added a way to toggle sync without re-testing authorization.

**`/app/controllers/tabs/databases.py`**:

* Added a check to see if sync is enabled or not, then sets up the database.
* Added `databaseWithSyncLoaded` to differentiate from local and synced database.

**`/app/models.py`**:

* Added `EditedEntryWithGroup` to allow passing a `group_id` when editing an entry.

**`/app/localdb/synced_db.py`**:

* Added as a wrapper to `MainDatabase` to enable syncing with the server.

**`/app/localdb/database.py`**:

* Added `group_id` parameter to `PasswordGroupMethods.create_group()` to stay in sync with the server.
* Added `entry_id` and `group_id` parameter to `PasswordEntryMethods.create_entry()` to stay in sync with the server.
* Added `SyncConfigMethods.toggle_sync_enabled()` to toggle when sync is enabled or not.

## Changes

**`/app/client/`**:

* Updated generated OpenAPI client to match the server.

**`/app/controllers/tabs/passwords.py`**:

* `PasswordEntryInfoDialog` now returns a group ID when finishing an edit operation.

## Misc

* Most of the app now works when using the synced database, the next step is to find a way to ensure
  the local copy of the client always stays synced with the server.
