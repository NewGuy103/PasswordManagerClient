# Add a way to display the entry info below the entry table

**Version**: v0.1.0

**Date:** 16/06/2025

## Additions

**`/app/controllers/tabs/passwords.py`**:

* Added `PasswordEntriesTableModel` as the abstract table model for the view.

**`/CHANGES.md`**:

* Added changelog file.

**`/app/models.py`**:

* Added `notes` field to `PasswordEntryBase`.
* Added `created_at` field for `PasswordEntryData`.

**`/app/localdb/dbtables.py`**:

* Added `notes` and `created_at` field.

**`/app/controllers/tabs/passwords.py`**:

* Added `entryChanged` signal to `PasswordEntriesController`.
* Added `PasswordEntryInfoController` to handle showing information about the current entry.

## Changes

**`/app/main.py`**:

* Now properly closes the app if the initial loading fails by using `QTimer.singleShot`.

**`/app/models.py`**:

* Changed `entry_name` field to `title` in `PasswordEntryBase`.
* Uncommented `group_id` in `PasswordEntryData`.

**`/app/localdb/dbtables.py`**:

* Removed `entry_` prefix for `username`, `password` and `url`.
* Changed `entry_name` field to `title`.

**`/app/localdb/database.py`**:

* Removed placeholder types `AsyncSession` and `GroupPublicGet`.
* Changed many variable names to match the models and database tables.

**`/app/controllers/tabs/passwords.py`**:

* Changed `PasswordEntriesTableModel` column headers to include "Created at" and "Title".
* `AddPasswordEntryDialog` now disables the accept button when the URL is invalid.
* `AddPasswordGroupDialog` also disables the accept button when there is no group name set.

## Misc

* Will add editing/renaming and more after this, then the app settings and such can be worked on.
