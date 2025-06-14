# Change model for entries to be a table instead of a list

**Version**: v0.1.0

**Date:** 14/06/2025

## Additions

**`/app/controllers/tabs/passwords.py`**:

* Added `PasswordEntriesTableModel` as the abstract table model for the view.

**`/CHANGES.md`**:

* Added changelog file.

## Changes

**`/app/controllers/tabs/passwords.py`**:

* Refactored some `make_worker_thread` calls to use a callback method of the
  controller instead of a function inside a function.

## Misc

* Working on the client application to see what it needs and what can be improved, before making
  some functionality to sync with the server app.
