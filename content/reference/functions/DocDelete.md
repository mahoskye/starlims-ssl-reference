---
title: "DocDelete"
summary: "Deletes a Documentum document by object ID."
id: ssl.function.docdelete
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocDelete

Deletes a Documentum document by object ID.

`DocDelete` takes a required `sObjId` and an optional `bAllVersions` flag. When you omit `bAllVersions`, the SSL wrapper defaults it to [`.T.`](../literals/true.md) before calling the backend delete operation. The function returns [`.T.`](../literals/true.md) when the delete succeeds and [`.F.`](../literals/false.md) when the backend call does not succeed.

Passing [`NIL`](../literals/nil.md) for `sObjId` raises an immediate SSL argument error. Other delete failures are returned as [`.F.`](../literals/false.md) and leave details in the current Documentum error state, which you can inspect with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## When to use

- When you need to delete a document and you already have its object ID.
- When you need to choose between the default all-versions delete and a single-version delete request.
- When your workflow needs a boolean result and can inspect the Documentum error state after a failure.

## Syntax

```ssl
DocDelete(sObjId, [bAllVersions])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sObjId` | [string](../types/string.md) | yes | — | Document object ID to delete. |
| `bAllVersions` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | When [`.T.`](../literals/true.md), the backend delete request uses the all-versions form. When [`.F.`](../literals/false.md), it uses the single-version form. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the delete operation succeeds. [`.F.`](../literals/false.md) when the backend delete call fails or does not return success.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sObjId` is [`NIL`](../literals/nil.md). | `sObjId argument cannot be null` |

## Best practices

!!! success "Do"
    - Check the boolean result immediately after the call.
    - Pass `bAllVersions` explicitly when your workflow depends on deleting one version versus all versions.
    - Read [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) right after a [`.F.`](../literals/false.md) result when you need the failure details.
    - Validate that `sObjId` is populated before calling the function.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sObjId`; that raises an immediate SSL argument error.
    - Assume a failed delete raises an exception in normal flow; backend failures come back as [`.F.`](../literals/false.md).
    - Use the default call form when you only want the single-version delete request.
    - Delay reading [`DocGetErrorMessage`](DocGetErrorMessage.md), because a later Documentum call can replace the stored error state.

## Caveats

- Only [`NIL`](../literals/nil.md) is checked by the SSL wrapper. Blank strings are passed through to the backend delete call.

## Examples

### Delete all versions using the default behavior

Deletes all versions of a document using the default `bAllVersions` behavior and displays either a success message or the Documentum error when the call returns [`.F.`](../literals/false.md).

```ssl
:PROCEDURE DeleteArchivedDocument;
    :PARAMETERS sObjId;
    :DEFAULT sObjId, "0900000180001234";
    :DECLARE bDeleted;

    bDeleted := DocDelete(sObjId);

    :IF .NOT. bDeleted;
        ErrorMes("Document delete failed: " + DocGetErrorMessage());
        :RETURN .F.;
    :ENDIF;

    UsrMes("Document deleted: " + sObjId);

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("DeleteArchivedDocument", {"0900000180001234"});
```

### Delete only the current version by passing [`.F.`](../literals/false.md) for `bAllVersions`

Passes [`.F.`](../literals/false.md) for `bAllVersions` to request a single-version delete, then distinguishes between a Documentum command failure and a [`.F.`](../literals/false.md) result with no recorded error.

```ssl
:PROCEDURE DeleteCurrentVersionOnly;
    :PARAMETERS sObjId;
    :DEFAULT sObjId, "0900000180005678";
    :DECLARE bDeleted, sErrMsg;

    bDeleted := DocDelete(sObjId, .F.);

    :IF bDeleted;
        UsrMes("Delete request completed for one version: " + sObjId);
        :RETURN .T.;
    :ENDIF;

    sErrMsg := DocGetErrorMessage();

    :IF DocCommandFailed();
        ErrorMes("Single-version delete failed: " + sErrMsg);
    :ELSE;
        UsrMes("Single-version delete request returned .F. with no stored backend message");
    :ENDIF;

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("DeleteCurrentVersionOnly", {"0900000180005678"});
```

### Delete multiple documents and collect per-document failure details

Iterates a list of document object IDs, attempts each delete, and collects a failure object for every document that was not deleted successfully, then reports the overall outcome.

```ssl
:PROCEDURE DeleteDocumentsBatch;
    :DECLARE aObjIds, aFailures, oFailure, sObjId, sErrMsg, nIndex;

    aObjIds := {
        "0900000180002001",
        "0900000180002002",
        "0900000180002003"
    };
    aFailures := {};

    :FOR nIndex := 1 :TO ALen(aObjIds);
        sObjId := aObjIds[nIndex];

        :IF DocDelete(sObjId);
            :LOOP;
        :ENDIF;

        sErrMsg := DocGetErrorMessage();
        oFailure := CreateUdObject();
        oFailure:objId := sObjId;
        oFailure:commandFailed := DocCommandFailed();
        oFailure:errorMessage := sErrMsg;
        AAdd(aFailures, oFailure);
    :NEXT;

    :IF ALen(aFailures) > 0;
        ErrorMes("One or more document deletes failed");
    :ELSE;
        UsrMes("All requested documents were deleted");
    :ENDIF;

    :RETURN aFailures;
:ENDPROC;

/* Usage;
DoProc("DeleteDocumentsBatch");
```

## Related

- [`DocExists`](DocExists.md)
- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocDeleteCabinet`](DocDeleteCabinet.md)
- [`DocDeleteFolder`](DocDeleteFolder.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocImportDocument`](DocImportDocument.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
