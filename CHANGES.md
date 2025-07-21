# Implement password groups tree model and update client

**Version**: v0.1.0

**Date:** 21/07/2025

## Additions

**`/app/workers.py`**:

* Added simple object names and thread counts for debugging.

**`/app/models/ui.py`**:

* Added `PasswordGroupItem` and `PasswordGroupsTreeModel` to handle password groups instead of using a standard item model.

**`/app/models/models.py`**:

* Added `group_id` to `PasswordEntryBase` because all state models require a `group_id` anyway.
* Added `parent_id` field to `AddPasswordGroup` to ensure current group can't change while processing.

## Changes

**`/app/serversync/ | /app/client`**:

* Updated client to match server's API.

**`/app/models/models.py`**:

* Removed `child_groups` from `GroupParentData`.

**`/app/models/models.py`**:

* Separated `get_root_info()` and `get_children_of_root()`.
* Separated `get_group_info()` and `get_children_of_group()`

**`/app/controllers/tabs/passwords.py`**:

* Many changes related to groups and internal models.

## Misc

* Actual features such as paging and ensuring the server and client don't become out of sync will follow
  as the current goal is to clean up the application and then work from there.
