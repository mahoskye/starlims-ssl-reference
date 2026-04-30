---
title: "DocCancelCheckout"
summary: "Cancels checkout for a Documentum document and returns a boolean result."
id: ssl.function.doccancelcheckout
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCancelCheckout

Cancels checkout for a Documentum document and returns a boolean result.

`DocCancelCheckout` takes one required `sDocumentId` string. If `sDocumentId` is [`NIL`](../literals/nil.md), the function raises an argument-null exception immediately. For non-null input, it resolves the document by id or path and returns [`.T.`](../literals/true.md) when the call completes successfully. That includes the case where the document exists but is already not checked out. If the Documentum operation fails, the function returns [`.F.`](../literals/false.md); you can then inspect the failure with [`DocCommandFailed`](DocCommandFailed.md) and
[`DocGetErrorMessage`](DocGetErrorMessage.md).

## When to use

- When a workflow abandons edits and must release a checked-out document.
- When cleanup logic should cancel checkout instead of checking in changed content.
- When you want a boolean success/failure result and optional Documentum diagnostics.

## Syntax

```ssl
DocCancelCheckout(sDocumentId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDocumentId` | [string](../types/string.md) | yes | — | Document identifier or path to cancel checkout for. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the document is resolved and the call completes successfully, including when the document is already not checked out. [`.F.`](../literals/false.md) when the Documentum operation fails.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDocumentId` is [`NIL`](../literals/nil.md). | `sDocumentId argument cannot be null` |

## Best practices

!!! success "Do"
    - Check the boolean return value before assuming the checkout was cancelled.
    - Use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) after a [`.F.`](../literals/false.md) result when you need diagnostic detail.
    - Use this function when abandoning changes and you want to release the checkout without checking in content.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sDocumentId`. That raises an exception instead of returning [`.F.`](../literals/false.md).
    - Treat [`.T.`](../literals/true.md) as proof that the document had been checked out. A document that is already not checked out also completes successfully.
    - Ignore a [`.F.`](../literals/false.md) result. Check the related Documentum error helpers before continuing.

## Caveats

- Passing an empty string does not raise directly; the underlying Documentum call fails and the function returns [`.F.`](../literals/false.md). In that case, [`DocGetErrorMessage`](DocGetErrorMessage.md) returns a message such as `You must specify document's path or document's id!`.
- A document id or path that cannot be resolved also returns [`.F.`](../literals/false.md), with [`DocGetErrorMessage`](DocGetErrorMessage.md) returning a message such as `Failed: Object does not exist`.
- The function does not tell you whether a [`.T.`](../literals/true.md) result came from cancelling an active checkout or from a document that was already not checked out.
- The function changes checkout state only; it does not check in content or delete the document.

## Examples

### Inspect Documentum diagnostics after a failed cancel-checkout call

Attempts to cancel checkout for a document id passed as a procedure parameter, then builds a diagnostic message using [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) when the call returns [`.F.`](../literals/false.md).

```ssl
:PROCEDURE CancelCheckoutWithDiagnostics;
    :PARAMETERS sDocumentId;
    :DECLARE bCancelled, sMessage;

    bCancelled := DocCancelCheckout(sDocumentId);

    :IF bCancelled;
        UsrMes("Cancel checkout call completed for document: " + sDocumentId);

        :RETURN .T.;
    :ENDIF;

    sMessage := "Cancel checkout failed for document: " + sDocumentId;

    :IF DocCommandFailed();
        sMessage := sMessage + ": " + DocGetErrorMessage();
    :ENDIF;

    ErrorMes(sMessage);

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("CancelCheckoutWithDiagnostics", {"DOC-001"});
```

### Cancel checkout for multiple documents and collect failures

Iterates a list of document ids, cancels checkout for each one, and collects failure messages, with Documentum diagnostics appended when available, before continuing to the next document.

```ssl
:PROCEDURE CancelCheckoutBatch;
    :DECLARE aDocumentIds, aFailedDocs, sDocumentId, sMessage, nIndex;

    aDocumentIds := {"DOC-001", "DOC-002", "DOC-003"};
    aFailedDocs := {};

    :FOR nIndex := 1 :TO ALen(aDocumentIds);
        sDocumentId := aDocumentIds[nIndex];

        :IF .NOT. DocCancelCheckout(sDocumentId);
            sMessage := sDocumentId;

            :IF DocCommandFailed();
                sMessage := sMessage + ": " + DocGetErrorMessage();
            :ENDIF;

            AAdd(aFailedDocs, sMessage);
        :ENDIF;
    :NEXT;

    :IF ALen(aFailedDocs) > 0;
        ErrorMes("Some documents could not be released from checkout");

        :RETURN aFailedDocs;
    :ENDIF;

    UsrMes("All cancel checkout calls completed successfully");

    :RETURN {};
:ENDPROC;

/* Usage;
DoProc("CancelCheckoutBatch");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocCheckoutDocument`](DocCheckoutDocument.md)
- [`DocCheckinDocument`](DocCheckinDocument.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
