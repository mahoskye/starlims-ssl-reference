---
title: "DocGetFolders"
summary: "Retrieves the immediate child folders of a Documentum folder as a sorted two-dimensional array."
id: ssl.function.docgetfolders
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetFolders

Retrieves the immediate child folders of a Documentum folder as a sorted two-dimensional array.

`DocGetFolders` queries the supplied repository path for items of type `dm_folder` and returns one row per child folder. Each row is a 5-element array containing the folder ID, name, type, content type, and status in fixed positions. Results are sorted by folder name before they are returned.

If `sParentPath` is [`NIL`](../literals/nil.md), the function raises an exception. Other Documentum lookup failures are captured by the Documentum interface and surface as an empty array, which you can distinguish from a genuine no-results case by checking [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## When to use

- When you need to list the direct child folders under a known Documentum path.
- When you need folder metadata such as ID, type, content type, or status for display or follow-up processing.
- When you need to validate that expected subfolders exist before continuing a document-management workflow.

## Syntax

```ssl
DocGetFolders(sParentPath)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sParentPath` | [string](../types/string.md) | yes | — | Repository folder path to query for immediate child folders. Passing [`NIL`](../literals/nil.md) raises an exception. |

## Returns

**[array](../types/array.md)** — A two-dimensional array. Each row is a 5-element array of strings.

| Position | Value |
|----------|-------|
| `row[1]` | Folder ID |
| `row[2]` | Folder name |
| `row[3]` | Folder type |
| `row[4]` | Content type |
| `row[5]` | Status |

Status is returned as one of these string values:

- `checkedin`
- `checkedout`
- `locked`

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sParentPath` is [`NIL`](../literals/nil.md). | `sParentPath argument cannot be null` |

## Best practices

!!! success "Do"
    - Check `ALen(aFolders)` before iterating, because both an empty folder and a failed Documentum lookup can produce an empty array.
    - Access row values by their documented 1-based positions such as `aFolders[nIndex, 2]` for the folder name.
    - Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) when an empty result may indicate a failed lookup rather than a folder with no child folders.

!!! failure "Don't"
    - Treat each result row as an object with named properties. Each row is an array.
    - Assume every empty result means the folder has no children. A failed Documentum call also returns an empty array.
    - Pass [`NIL`](../literals/nil.md) when you mean to query a real folder path. That raises an exception instead of returning a result.

## Caveats

- The function returns only immediate child folders. It does not recurse into nested folders.
- Blank strings for `sParentPath` are not rejected. They are passed through to the Documentum query and will likely produce an empty array.

## Examples

### List child folder names

Queries a folder for immediate children and prints each folder name, exiting early when the result is empty.

```ssl
:PROCEDURE ListChildFolders;
    :DECLARE sParentPath, aFolders, nCount, nIndex;

    sParentPath := "/Engineering/Specifications";
    aFolders := DocGetFolders(sParentPath);
    nCount := ALen(aFolders);

    :IF nCount == 0;
        UsrMes("No child folders found in " + sParentPath);
        /* Displays when empty: No child folders found;

        :RETURN aFolders;
    :ENDIF;

    :FOR nIndex := 1 :TO nCount;
        UsrMes(aFolders[nIndex, 2]);
        /* Displays per folder: folder name;
    :NEXT;

    :RETURN aFolders;
:ENDPROC;

/* Usage;
DoProc("ListChildFolders");
```

### Validate required subfolders and detect lookup failures

Checks that three required child folders exist under a path, distinguishing a failed Documentum lookup (empty result with [`DocCommandFailed`](DocCommandFailed.md) set) from a folder that is genuinely missing from the results.

```ssl
:PROCEDURE ValidateRequiredFolders;
    :DECLARE sParentPath, aFolders, aRequiredFolders, aMissingFolders;
    :DECLARE sRequiredName, sError, nIndex;

    sParentPath := "/Clinical/StudyReports";
    aRequiredFolders := {"Archive", "Incoming", "Processed"};
    aMissingFolders := {};

    aFolders := DocGetFolders(sParentPath);

    :IF ALen(aFolders) == 0 .AND. DocCommandFailed();
        sError := DocGetErrorMessage();
        ErrorMes("Unable to retrieve child folders: " + sError);

        :RETURN .F.;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aRequiredFolders);
        sRequiredName := aRequiredFolders[nIndex];

        :IF AScan(aFolders, {|aRow| Upper(aRow[2]) == Upper(sRequiredName)}) == 0;
            AAdd(aMissingFolders, sRequiredName);
        :ENDIF;
    :NEXT;

    :IF ALen(aMissingFolders) > 0;
        UsrMes(
            "Missing required folders under " + sParentPath + ": "
            + BuildString(aMissingFolders)
        );
        /* Displays when folders are missing: Missing required folders;

        :RETURN .F.;
    :ENDIF;

    UsrMes("All required child folders are present under " + sParentPath);
    /* Displays when all present: All required child folders are present;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateRequiredFolders");
```

In the failure path, `ErrorMes` displays:

```text
Unable to retrieve child folders: <repository error>
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocGetCabinets`](DocGetCabinets.md)
- [`DocGetDocuments`](DocGetDocuments.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
