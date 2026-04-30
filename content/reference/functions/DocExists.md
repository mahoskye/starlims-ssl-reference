---
title: "DocExists"
summary: "Checks whether a Documentum document exists for a given object ID."
id: ssl.function.docexists
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocExists

Checks whether a Documentum document exists for a given object ID.

`DocExists(sObjId)` returns [`.T.`](../literals/true.md) when the specified document exists and [`.F.`](../literals/false.md) when the check returns no success value. Passing [`NIL`](../literals/nil.md) for `sObjId` raises an argument error before the Documentum call is attempted.

The function uses the current Documentum session context. Initialize that context with [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) before calling `DocExists`.

If the Documentum lookup fails, `DocExists` still returns [`.F.`](../literals/false.md). When you need to distinguish "not found" from "Documentum command failed," check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after the call.

## When to use

- When you need to confirm that a document exists before deleting, exporting, or updating it.
- When your workflow needs to branch between "continue with the document" and "handle missing document".
- When you want a lightweight existence check without retrieving document metadata.
- When you already have an active Documentum interface context for the current workflow.

## Syntax

```ssl
DocExists(sObjId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sObjId` | [string](../types/string.md) | yes | — | Object ID of the document to check. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the document exists. [`.F.`](../literals/false.md) when the document does not exist or when the Documentum command does not complete successfully.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sObjId` is [`NIL`](../literals/nil.md). | `sObjId argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sObjId` is populated before calling the function.
    - Initialize the Documentum interface with [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) before using `DocExists`.
    - Check [`DocCommandFailed`](DocCommandFailed.md) right after a [`.F.`](../literals/false.md) result when you need to separate a missing document from a Documentum failure.
    - Use `DocExists` as a precondition check before operations such as [`DocDelete`](DocDelete.md) or [`DocExportDocument`](DocExportDocument.md).

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sObjId`; that raises an error instead of returning [`.F.`](../literals/false.md).
    - Call `DocExists` before the Documentum interface has been initialized for the current session.
    - Assume every [`.F.`](../literals/false.md) result means the document is missing.
    - Use this function when you need document metadata or content; it only answers the existence check.

## Caveats

- Only [`NIL`](../literals/nil.md) is rejected before the Documentum call. Blank strings are passed through to the Documentum lookup.

## Examples

### Check existence before deleting a document

Guards a delete operation by first calling `DocExists`, skipping the delete and reporting the outcome when the document is absent, and confirming deletion when it succeeds.

```ssl
:PROCEDURE DeleteIfDocumentExists;
    :DECLARE sObjId, bExists, bDeleted;

    sObjId := "0900000180001234";

    DocInitDocumentumInterface();

    :TRY;
        bExists := DocExists(sObjId);

        :IF .NOT. bExists;
            UsrMes("Document was not found: " + sObjId);
            :RETURN .F.;
        :ENDIF;

        bDeleted := DocDelete(sObjId);

        :IF .NOT. bDeleted;
            UsrMes("Delete request did not succeed for: " + sObjId);
            :RETURN .F.;
        :ENDIF;

        UsrMes("Document deleted: " + sObjId);

        :RETURN .T.;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("DeleteIfDocumentExists");
```

### Distinguish not found from Documentum failure

Checks [`DocCommandFailed`](DocCommandFailed.md) after a [`.F.`](../literals/false.md) result to tell apart a genuine missing document from a Documentum command failure, displaying a different message for each case.

```ssl
:PROCEDURE CheckDocumentStatus;
    :PARAMETERS sObjId;
    :DECLARE bExists, sErrMsg;

    DocInitDocumentumInterface();

    :TRY;
        bExists := DocExists(sObjId);

        :IF bExists;
            UsrMes("Document is available: " + sObjId);
            :RETURN .T.;
        :ENDIF;

        :IF DocCommandFailed();
            sErrMsg := DocGetErrorMessage();
            ErrorMes("Documentum check failed: " + sErrMsg);
            :RETURN .F.;
        :ENDIF;

        UsrMes("Document was not found: " + sObjId);

        :RETURN .F.;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CheckDocumentStatus", {"0900000180001234"});
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocDelete`](DocDelete.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocExportDocument`](DocExportDocument.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
