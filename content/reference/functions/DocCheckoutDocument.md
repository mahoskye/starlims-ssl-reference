---
title: "DocCheckoutDocument"
summary: "Checks out an existing Documentum document and returns the local checkout file path."
id: ssl.function.doccheckoutdocument
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCheckoutDocument

Checks out an existing Documentum document and returns the local checkout file path.

`DocCheckoutDocument` takes one required `sDocumentId` argument. If `sDocumentId` is [`NIL`](../literals/nil.md), the function raises an argument-null exception immediately. Otherwise, it attempts the checkout through the current Documentum session and returns the local file path produced by the checkout operation.

When the underlying Documentum command fails, this function returns an empty string. Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after the call to confirm whether the checkout succeeded and to capture the failure message.

## When to use

- When a workflow needs to check out a managed document before editing or replacing it.
- When you need the local checkout file path returned by the Documentum layer.
- When you want to branch on Documentum success or failure without relying on an SSL exception for command errors.

## Syntax

```ssl
DocCheckoutDocument(sDocumentId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDocumentId` | [string](../types/string.md) | yes | — | Document identifier or path to check out. |

## Returns

**[string](../types/string.md)** — The local file path returned by the checkout operation. If the underlying Documentum command fails, this function returns an empty string.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDocumentId` is [`NIL`](../literals/nil.md). | `sDocumentId argument cannot be null` |

## Best practices

!!! success "Do"
    - Initialize and log in to Documentum before calling this function.
    - Validate `sDocumentId` before the call when it may be missing.
    - Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after the call when the result matters.
    - Treat the returned string as a local checkout path that your next step can use for editing or later check-in.

!!! failure "Don't"
    - Assume checkout failures will surface as SSL exceptions. Documentum command failures are reported through the return value and the related error helpers.
    - Treat an empty return value as a successful checkout.
    - Continue with edit or check-in logic until you have confirmed the checkout succeeded.

## Caveats

- This function expects an active Documentum session, typically established with [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) and [`DocLoginToDocumentum`](DocLoginToDocumentum.md).
- Empty or whitespace `sDocumentId` does not raise directly; the command fails with `You must specify document's path or document's id!`. A missing document reports `Failed: Object does not exist`, and an already-checked-out document reports `Failed: Object is already checked out`.
- [`DocCommandFailed`](DocCommandFailed.md) reflects the most recent Documentum command, so check it before running another Documentum function.

## Examples

### Check out one document and keep the returned local file path

Logs in to Documentum, checks out a single document by ID, and displays either the local checkout file path or the command failure message.

```ssl
:PROCEDURE CheckoutDocumentBasic;
    :DECLARE sDocBase, sUser, sPassword;
    :DECLARE sDocumentId, sCheckoutPath;
    :DECLARE bLoggedIn;

    sDocBase := "QualityRepository";
    sUser := "doc_user";
    sPassword := "secret";
    sDocumentId := "DOC-2024-001";

    DocInitDocumentumInterface();

    :TRY;
        bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

        :IF .NOT. bLoggedIn;
            ErrorMes("Documentum login failed: " + DocGetErrorMessage()); /* Displays login failure details;

            :RETURN "";
        :ENDIF;

        sCheckoutPath := DocCheckoutDocument(sDocumentId);

        :IF DocCommandFailed();
            ErrorMes("Checkout failed: " + DocGetErrorMessage()); /* Displays checkout failure details;

            :RETURN "";
        :ENDIF;

        UsrMes("Checkout file path: " + sCheckoutPath); /* Displays the local checkout path;

        :RETURN sCheckoutPath;

    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage example;
DoProc("CheckoutDocumentBasic");
```

### Validate input and return a structured checkout result

Guards against an empty document ID before calling checkout and returns a structured result object containing the success flag, checkout path, and any error message.

```ssl
:PROCEDURE CheckoutDocumentWithStatus;
    :PARAMETERS sDocumentId;
    :DECLARE oResult, sCheckoutPath;

    oResult := CreateUdObject();
    oResult:success := .F.;
    oResult:checkoutPath := "";
    oResult:errorMessage := "";

    :IF Empty(sDocumentId);
        oResult:errorMessage := "Document ID is required before checkout.";

        :RETURN oResult;
    :ENDIF;

    sCheckoutPath := DocCheckoutDocument(sDocumentId);

    :IF DocCommandFailed();
        oResult:errorMessage := DocGetErrorMessage();

        :RETURN oResult;
    :ENDIF;

    oResult:success := .T.;
    oResult:checkoutPath := sCheckoutPath;

    :RETURN oResult;
:ENDPROC;

/* Usage example;
DoProc("CheckoutDocumentWithStatus", {"DOC-2024-001"});
```

### Check out multiple documents and track per-document failures

Checks out a list of document IDs, collects a failure object for each one that does not succeed, and reports the total count of failed checkouts.

```ssl
:PROCEDURE CheckoutDocumentsBatch;
    :DECLARE sDocBase, sUser, sPassword;
    :DECLARE aDocumentIds, aCheckoutPaths, aFailures;
    :DECLARE sDocumentId, sCheckoutPath;
    :DECLARE oBatchResult, oFailure;
    :DECLARE nIndex, bLoggedIn;

    sDocBase := "QualityRepository";
    sUser := "doc_user";
    sPassword := "secret";
    aDocumentIds := {"DOC-2024-001", "DOC-2024-002", "DOC-2024-003"};
    aCheckoutPaths := {};
    aFailures := {};

    oBatchResult := CreateUdObject();
    oBatchResult:checkoutPaths := aCheckoutPaths;
    oBatchResult:failures := aFailures;

    DocInitDocumentumInterface();

    :TRY;
        bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

        :IF .NOT. bLoggedIn;
            ErrorMes("Documentum login failed: " + DocGetErrorMessage());
            /* Displays login failure details;

            :RETURN oBatchResult;
        :ENDIF;

        :FOR nIndex := 1 :TO ALen(aDocumentIds);
            sDocumentId := aDocumentIds[nIndex];
            sCheckoutPath := DocCheckoutDocument(sDocumentId);

            :IF DocCommandFailed();
                oFailure := CreateUdObject();
                oFailure:documentId := sDocumentId;
                oFailure:errorMessage := DocGetErrorMessage();
                AAdd(aFailures, oFailure);
            :ELSE;
                AAdd(aCheckoutPaths, sCheckoutPath);
            :ENDIF;
        :NEXT;

        :IF ALen(aFailures) > 0;
            UsrMes(
                "One or more document checkouts failed. Count: "
                + LimsString(ALen(aFailures))
            ); /* Displays the checkout failure count;
        :ENDIF;

        oBatchResult:checkoutPaths := aCheckoutPaths;
        oBatchResult:failures := aFailures;

        :RETURN oBatchResult;

    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage example;
DoProc("CheckoutDocumentsBatch");
```

## Related

- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`string`](../types/string.md)
- [`object`](../types/object.md)
