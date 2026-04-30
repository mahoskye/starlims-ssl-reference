---
title: "DocCommandFailed"
summary: "Checks whether the most recent Documentum command in the current session failed."
id: ssl.function.doccommandfailed
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCommandFailed

Checks whether the most recent Documentum command in the current session failed.

`DocCommandFailed` returns [`.T.`](../literals/true.md) when the current Documentum session context has a recorded exception for the most recent Documentum command, and [`.F.`](../literals/false.md) when no exception is currently recorded. It takes no parameters and is most useful immediately after a Documentum call such as [`DocLoginToDocumentum`](DocLoginToDocumentum.md), [`DocCheckoutDocument`](DocCheckoutDocument.md), or [`DocCancelCheckout`](DocCancelCheckout.md). The function does not provide error details by itself; use [`DocGetErrorMessage`](DocGetErrorMessage.md) when you need the message from the same failure state.

## When to use

- When you need a quick success or failure check immediately after a Documentum call.
- When a Documentum function returns a value but you also want to know whether Documentum recorded an exception.
- When you want to branch to logging or recovery logic before continuing the workflow.

## Syntax

```ssl
DocCommandFailed()
```

## Parameters

This function takes no parameters.

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the most recent Documentum command in the current session context recorded an exception. [`.F.`](../literals/false.md) when no exception is currently recorded.

## Best practices

!!! success "Do"
    - Call `DocCommandFailed` immediately after the specific Documentum command you want to verify.
    - Pair it with [`DocGetErrorMessage`](DocGetErrorMessage.md) when you need the failure message.
    - Initialize the Documentum session first with [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) and close it when finished with [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md).

!!! failure "Don't"
    - Call this before [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md), or after the session has been ended.
    - Wait until later in the workflow to check it. Another Documentum call can clear the earlier failure state.
    - Treat this as an error-details function. It tells you whether a failure was recorded, not why it happened.

## Caveats

- This function requires an active Documentum session context.
- It reports only the most recent recorded Documentum exception for that session context.
- A later Documentum call can replace the earlier failure state, even if you have not inspected it yet.

## Examples

### Check whether a login attempt was recorded as a failure

Calls `DocCommandFailed` immediately after a login attempt to detect a recorded Documentum failure, then displays either an error message or a success message.

```ssl
:PROCEDURE CheckDocumentumLogin;
    :DECLARE sDocBase, sUser, sPassword, bLoggedIn, bFailed;

    sDocBase := "Repository1";
    sUser := "analyst";
    sPassword := "secret";

    DocInitDocumentumInterface();

    :TRY;
        bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);
        bFailed := DocCommandFailed();

        :IF bFailed;
            ErrorMes("Documentum login failed: " + DocGetErrorMessage());
            /* Displays on failure: Documentum login failed;
        :ELSE;
            UsrMes("Documentum login succeeded");
        :ENDIF;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;

    :RETURN bLoggedIn;
:ENDPROC;

/* Usage;
DoProc("CheckDocumentumLogin");
```

### Return early when a document command records a failure

Cancels checkout for a document id passed as a parameter and returns [`.F.`](../literals/false.md) immediately when `DocCommandFailed` reports a recorded failure.

```ssl
:PROCEDURE CancelCheckoutSafely;
    :PARAMETERS sDocumentId;

    DocInitDocumentumInterface();

    :TRY;
        :IF .NOT. DocLoginToDocumentum("Repository1", "analyst", "secret");
            ErrorMes("Login failed: " + DocGetErrorMessage());
            /* Displays on failure: Login failed;

            :RETURN .F.;
        :ENDIF;

        DocCancelCheckout(sDocumentId);

        :IF DocCommandFailed();
            ErrorMes(
                "Cancel checkout failed for " + sDocumentId + ": "
                + DocGetErrorMessage()
            );
            /* Displays on failure: Cancel checkout failed;

            :RETURN .F.;
        :ENDIF;

        :RETURN .T.;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CancelCheckoutSafely", {"DOC-001"});
```

### Capture failures for each document in a batch loop

Iterates a list of document IDs, attempts checkout for each one, captures any recorded failure message before the next call can overwrite it, and reports whether any failures occurred.

```ssl
:PROCEDURE CollectDocumentumFailures;
    :DECLARE aDocumentIds, aFailures, sDocumentId, sMessage, nIndex;

    aDocumentIds := {"DOC-001", "DOC-002", "DOC-003"};
    aFailures := {};

    DocInitDocumentumInterface();

    :TRY;
        :IF .NOT. DocLoginToDocumentum("Repository1", "analyst", "secret");
            ErrorMes("Login failed: " + DocGetErrorMessage());
            /* Displays on failure: Login failed;

            :RETURN {};
        :ENDIF;

        :FOR nIndex := 1 :TO ALen(aDocumentIds);
            sDocumentId := aDocumentIds[nIndex];

            DocCheckoutDocument(sDocumentId);

            :IF DocCommandFailed();
                sMessage := sDocumentId + ": " + DocGetErrorMessage();
                AAdd(aFailures, sMessage);
            :ENDIF;
        :NEXT;

        :IF ALen(aFailures) > 0;
            ErrorMes("One or more Documentum commands failed");
        :ELSE;
            UsrMes(
                "All Documentum commands completed without recorded failures"
            );
        :ENDIF;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;

    :RETURN aFailures;
:ENDPROC;

/* Usage;
DoProc("CollectDocumentumFailures");
```

## Related

- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`boolean`](../types/boolean.md)
