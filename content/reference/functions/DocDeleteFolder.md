---
title: "DocDeleteFolder"
summary: "Deletes a Documentum folder and optionally allows the delete only when the folder is empty."
id: ssl.function.docdeletefolder
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocDeleteFolder

Deletes a Documentum folder and optionally allows the delete only when the folder is empty.

`DocDeleteFolder` takes a required `sFolderId` and an optional `bDeepDelete` flag. When you omit `bDeepDelete`, the function uses [`.T.`](../literals/true.md). It returns [`.T.`](../literals/true.md) when the folder delete succeeds and [`.F.`](../literals/false.md) when the Documentum delete operation fails.

Passing [`NIL`](../literals/nil.md) for `sFolderId` raises an immediate SSL argument error. Other delete failures, including blank input, an unresolved folder, or a non-empty folder when `bDeepDelete` is [`.F.`](../literals/false.md), return [`.F.`](../literals/false.md) and leave details in the current Documentum error state, which you can inspect with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## When to use

- When you need to delete a folder and all of its contents in one operation.
- When you need to prevent recursive deletion by requiring the target folder to be empty.
- When your workflow needs a boolean success result and can inspect the current
  Documentum error state after a failed delete.

## Syntax

```ssl
DocDeleteFolder(sFolderId, [bDeepDelete])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sFolderId` | [string](../types/string.md) | yes | — | Folder reference to delete. |
| `bDeepDelete` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | When [`.T.`](../literals/true.md), the delete call proceeds recursively. When [`.F.`](../literals/false.md), the call fails if the folder has children. If omitted, the function uses [`.T.`](../literals/true.md). |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the folder delete succeeds. [`.F.`](../literals/false.md) when the Documentum delete operation fails.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFolderId` is [`NIL`](../literals/nil.md). | `sFolderId argument cannot be null` |

## Best practices

!!! success "Do"
    - Check the boolean result immediately after the call.
    - Use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) right after a [`.F.`](../literals/false.md) result so you capture the failure from this delete attempt.
    - Pass `bDeepDelete` explicitly when your workflow must guarantee either recursive delete or empty-folder-only delete behavior.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sFolderId`; that raises an immediate SSL argument error.
    - Assume [`.F.`](../literals/false.md) means only one kind of failure. Blank input, an invalid folder, and a non-empty folder can all fail this call.
    - Delay reading [`DocGetErrorMessage`](DocGetErrorMessage.md). A later Documentum call can replace the stored error state.

## Caveats

- A blank or whitespace-only `sFolderId` does not raise the SSL [`NIL`](../literals/nil.md) argument exception. The Documentum operation fails instead and records `Please specify folder id or folder path!`.
- If the supplied folder cannot be resolved, the current Documentum error state records `Failed: Folder does not exist`.
- If `bDeepDelete` is [`.F.`](../literals/false.md) and the folder has children, the current Documentum error state records `Failed: Folder is not empty`.
- This function works against the current Documentum session state, so use it within an initialized Documentum workflow.

## Examples

### Delete one folder using the default recursive behavior

Deletes a folder using the default deep-delete mode, captures any Documentum error message when the call returns [`.F.`](../literals/false.md), and displays the result.

```ssl
:PROCEDURE DeleteArchiveFolder;
    :PARAMETERS sFolderId;
    :DEFAULT sFolderId, "ARCHIVE-FOLDER-001";
    :DECLARE bDeleted, sErrMsg;

    bDeleted := DocDeleteFolder(sFolderId);

    :IF .NOT. bDeleted;
        :IF DocCommandFailed();
            sErrMsg := DocGetErrorMessage();
            ErrorMes("Folder delete failed: " + sErrMsg);
            /* Displays folder delete failure details;
        :ELSE;
            ErrorMes("Folder delete failed");
        :ENDIF;

        :RETURN .F.;
    :ENDIF;

    UsrMes("Folder deleted: " + sFolderId);
    /* Displays deleted folder ID;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("DeleteArchiveFolder", {"ARCHIVE-FOLDER-001"});
```

### Require the folder to be empty before deleting

Passes [`.F.`](../literals/false.md) for `bDeepDelete` to reject non-empty folders, then distinguishes between a non-empty-folder failure (skipped with a message) and any other delete failure (reported as an error).

```ssl
:PROCEDURE DeleteEmptyFolderOnly;
    :PARAMETERS sFolderId;
    :DECLARE bDeleted, sErrMsg;

    bDeleted := DocDeleteFolder(sFolderId, .F.);

    :IF bDeleted;
        UsrMes("Empty folder deleted: " + sFolderId);
        /* Displays deleted folder ID;
        :RETURN .T.;
    :ENDIF;

    :IF DocCommandFailed();
        sErrMsg := DocGetErrorMessage();
    :ELSE;
        sErrMsg := "Folder delete failed";
    :ENDIF;

    :IF sErrMsg == "Failed: Folder is not empty";
        UsrMes("Skipped non-empty folder: " + sFolderId);
        /* Displays skipped folder ID when not empty;
        :RETURN .F.;
    :ENDIF;

    ErrorMes("Folder delete failed: " + sErrMsg);
    /* Displays folder delete failure details;

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("DeleteEmptyFolderOnly", {"ARCHIVE-FOLDER-001"});
```

### Delete multiple folders and collect per-folder failure details

Iterates a list of folder IDs, attempts each delete, and collects a failure object for every folder that was not deleted successfully, then reports the overall outcome.

```ssl
:PROCEDURE DeleteFoldersBatch;
    :DECLARE aFolderIds, aFailures, oFailure, sFolderId, sErrMsg, nIndex;

    aFolderIds := {
        "ARCHIVE-2024-01",
        "ARCHIVE-2024-02",
        "ARCHIVE-2024-03"
    };
    aFailures := {};

    :FOR nIndex := 1 :TO ALen(aFolderIds);
        sFolderId := aFolderIds[nIndex];

        :IF DocDeleteFolder(sFolderId);
            :LOOP;
        :ENDIF;

        :IF DocCommandFailed();
            sErrMsg := DocGetErrorMessage();
        :ELSE;
            sErrMsg := "Folder delete failed";
        :ENDIF;

        oFailure := CreateUdObject();
        oFailure:folderId := sFolderId;
        oFailure:errorMessage := sErrMsg;
        AAdd(aFailures, oFailure);
    :NEXT;

    :IF ALen(aFailures) > 0;
        ErrorMes("One or more folder deletes failed");
    :ELSE;
        UsrMes("All folders were deleted successfully");
    :ENDIF;

    :RETURN aFailures;
:ENDPROC;

/* Usage;
DoProc("DeleteFoldersBatch");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
