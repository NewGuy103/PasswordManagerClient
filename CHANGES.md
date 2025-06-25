# Add support for multiple databases with one open at a time

**Version**: v0.1.0

**Date:** 25/06/2025

## Additions

**`/app/config.py`**:

* Added `recent_databases` to config model.

**`/app/controllers/tabs/databases.py`**:

* Added support for multiple databases but one opened at a time.

**`/app/controllers/tabs/passwords.py`**:

* Added statusbar information whenever an action is performed.

## Changes

**`/app/main.py`**:

* No longer loads the main database file, instead offloaded to the `databases.py` controller.

**`/app/controllers/apps.py`**:

* Changed to automatically disable the passwords tab until a database is selected.

**`/app/localdb/database.py`**:

* Changed `setup()` to take in an SQLite Path object to create the engine.
* Removed top-level `database` variable.

## Misc

* Will add editing/renaming and more after this, then the app settings and such can be worked on.
