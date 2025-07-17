# Implement most of server sync functionality

**Version**: v0.1.0

**Date:** 17/07/2025

## Additions

**`/app/models.py`**:

* Added `entry_id` to `EditedEntryWithGroup` as it's the simplest way to keep track of the existing entry.

**`/app/serversync/`**:

* Added abstraction to the generated client as a simpler way to sync with the server.

**`/app/controllers/tabs/passwords.py`**:

* Added a way to optionally retrieve a loaded client.

## Changes

**`/app/controllers/apps.py`**:

* Changed to disable the databases tab while waiting for server sync to load.
* No longer switches to the settings tab.

**`/app/controllers/tabs/databases.py`**:

* Many changes to how it handles the local database and server sync, needs a lot of cleanup.

## Misc

* Will need a lot of cleanup to make sure the sync code doesn't break or become hard to maintain,
  this will also make it easier to implement new features.
