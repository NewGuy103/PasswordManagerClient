# Clean up passwords tab code

**Version**: v0.1.0

**Date:** 19/07/2025

## Additions

**`/app/models/`**:

* Added folder to store PySide6 models and state models.

**`/app/serversync/client.py`**:

* Added option to set client to be enabled/disabled when initializing.

**`/app/controllers/entry_data.py`**:

* Added as the helper to manage data within the passwords tab.

**`/app/controllers/tabs/passwords.py`**:

* Added a way to optionally retrieve a loaded client.

## Changes

**`/app/models.py`**:

* Moved file to `/app/models/` directory.

**`/app/controllers/sync_client.py`**:

* No longer emits `loadWithoutSync`, instead only emits `clientLoaded` that has `self.enabled` set.

**`/app/controllers/apps.py`**:

* Changed to disable the databases tab while waiting for server sync to load.
* No longer switches to the settings tab.

**`/app/controllers/tabs/databases.py`**:

* Moved list model to `/app/models/ui.py`.

**`/app/controllers/tabs/setting.py`**:

* Unlocking the database settings tab now happens when client is loaded to let everything load first.
* Now locks the edit sync info button while waiting for a request to complete.

**`/app/controllers/tabs/passwords.py`**:

* Moved table model to `/app/models/ui.py`.
* Cleaned up main controller, setup now happens only after both database and client have been loaded.
* Entries and groups controllers now require the database and client instances on initialization instead of taking the objects from the parent.
* Entries controller no longer depends on a `QModelIndex` and instead the UUID/model.

## Misc

* Cleanup of database and server sync code is halfway done, next is to clean up the groups and use
  a real tree model instead of relying on a standard item model.
