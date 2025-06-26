# Add initial support for sync information and implement entry editing

**Version**: v0.1.0

**Date:** 26/06/2025

## Additions

**`/pyside6_ui/edit_sync_info_dialog.ui | /app/ui/edit_sync_info_dialog.py`**

**`/app/controllers/tabs/settings.py`**:

* Added support for sync information, functionality not yet implemented.

**`/app/controllers/tabs/passwords.py`**:

* Added `PasswordEntryTableModel.update_entry()`.
* Added a messagebox to `PasswordsTabController.worker_exc_received()` for better UX.
* Added right-click action to edit entries.

**`/app/models.py`**:

* Added models for sync information and state.

**`/app/localdb/dbtables.py`**:

* Added `SyncConfig` singleton to handle sync information.

**`/app/localdb/database.py`**:

* Added `SyncConfigMethods`.
* Added `PasswordEntryMethods.update_entry_data()` to handle editing entries.

## Changes

**`/app/client/`**:

* Updated generated OpenAPI client to match the server.

**`/app/config.py`**:

* Removed `logins` field and `AvailableLogins` model because login info is moved to the specific database.

**`/app/models.py`**:

* Changed `PasswordEntryBase` to use an `AnyUrl | None` instead of a `str`.
* Changed `AddPasswordEntry` to `EditedPasswordEntryInfo` to unify adding and editing an entry.

**`/app/controllers/login_page.py`**:

* Removed login page logic because the client can now set up sync optionally.

**`/app/controllers/tabs/databases.py`**:

* Changed to load the database and run `setup()` and emit a `MainDatabase` instance.

**`/app/controllers/tabs/passwords.py`**:

* Changed to receive a loaded database instance instead of loading the database directly.
* Changed so that the entry info dialog is now created once and uses signals to add/edit data.

**`/app/localdb/database.py`**:

* Changed `PasswordEntryMethods.create_entry()` to take in an `EditedPasswordEntryInfo` model instead
  of the fields individually to simplify the code.

**`/app/localdb/dbtables.py`**:

* Changed `PasswordEntry.url` to be `str | None` and nullable.

## Misc

* Currently working on a way to add actual sync functionality and figuring out how that would add new routes
  to the server app.
* Will cleanup the app slowly after the core is complete.
