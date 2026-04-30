---
title: "DocCompleteWorkitem"
summary: "Completes a Documentum workflow work item and returns whether the operation succeeded."
id: ssl.function.doccompleteworkitem
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCompleteWorkitem

Completes a Documentum workflow work item and returns whether the operation succeeded.

`DocCompleteWorkitem` requires a work item identifier and accepts optional
sign-off values. If `sWorkitemId` is [`NIL`](../literals/nil.md), the function raises an argument-null exception instead of returning a boolean. For non-[`NIL`](../literals/nil.md) input, it attempts to complete the target work item and returns [`.T.`](../literals/true.md) on success or [`.F.`](../literals/false.md) on failure. Each call clears the current Documentum error state before running; if the completion attempt fails, the failure is available through [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## When to use

- When you need to complete a specific Documentum workflow work item.
- When the completion step may require sign-off credentials and a reason.
- When your script needs a boolean result and immediate access to the Documentum failure state for the same call.

## Syntax

```ssl
DocCompleteWorkitem(sWorkitemId, [sSignOffUser], [sSignOffPass], [sSignOffReason])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkitemId` | [string](../types/string.md) | yes | — | Identifier of the work item to complete. Passing [`NIL`](../literals/nil.md) raises an exception. |
| `sSignOffUser` | [string](../types/string.md) | no | omitted | User name for the optional sign-off step. A sign-off is attempted only when this value is not [`NIL`](../literals/nil.md) and not blank after trimming. |
| `sSignOffPass` | [string](../types/string.md) | no | omitted | Password passed to the sign-off operation when `sSignOffUser` triggers sign-off. |
| `sSignOffReason` | [string](../types/string.md) | no | omitted | Reason passed to the sign-off operation when `sSignOffUser` triggers sign-off. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the work item is completed successfully, or [`.F.`](../literals/false.md) when the underlying completion attempt fails.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sWorkitemId` is [`NIL`](../literals/nil.md). | `sWorkitemId argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sWorkitemId` is not [`NIL`](../literals/nil.md) before calling the function.
    - Check the boolean result before assuming the workflow step was completed.
    - Call [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after a failed completion when you need diagnostic detail.
    - Provide `sSignOffUser`, `sSignOffPass`, and `sSignOffReason` together when your workflow requires sign-off before completion.
    - Use the function within an initialized and logged-in Documentum session.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sWorkitemId`. That raises an exception instead of returning [`.F.`](../literals/false.md).
    - Assume `sSignOffPass` or `sSignOffReason` alone will trigger sign-off. The sign-off step only runs when `sSignOffUser` is present and not blank.
    - Ignore a [`.F.`](../literals/false.md) result. A failed call can record the reason for the failure on the current Documentum session.
    - Wait until after another Documentum call to inspect the failure state. A later call can replace the earlier error information.

## Caveats

- The function returns only a boolean result. Use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) when you need failure details.

## Examples

### Complete a single work item after logging in

Logs in to Documentum, completes one work item by ID, and displays whether the operation succeeded.

```ssl
:PROCEDURE CompleteBasicWorkitem;
    :DECLARE sDocBase, sUser, sPassword, sWorkitemId, bLoggedIn, bCompleted;

    sDocBase := "Repository1";
    sUser := "analyst";
    sPassword := "secret";
    sWorkitemId := "WI-2024-00142";

    DocInitDocumentumInterface();

    bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

    :IF .NOT. bLoggedIn;
        UsrMes("Documentum login failed: " + DocGetErrorMessage());
        DocEndDocumentumInterface();
        :RETURN .F.;
    :ENDIF;

    bCompleted := DocCompleteWorkitem(sWorkitemId);

    :IF bCompleted;
        UsrMes("Work item " + sWorkitemId + " completed successfully");
    :ELSE;
        UsrMes("Could not complete work item " + sWorkitemId);
    :ENDIF;

    DocEndDocumentumInterface();

    :RETURN bCompleted;
:ENDPROC;

/* Usage;
DoProc("CompleteBasicWorkitem");
```

### Complete a work item with sign-off and inspect the failure message on error

Completes a work item with all four sign-off arguments, then reads the Documentum error message to build a specific failure description when the operation returns [`.F.`](../literals/false.md).

```ssl
:PROCEDURE CompleteRegulatedWorkitem;
    :DECLARE sWorkitemId, sSignOffUser, sSignOffPass, sSignOffReason;
    :DECLARE bCompleted, sErrMsg;

    sWorkitemId := "WI-2024-00142";
    sSignOffUser := "jsmith";
    sSignOffPass := "P@ssw0rd!";
    sSignOffReason := "Approved for release";

    bCompleted := DocCompleteWorkitem(
        sWorkitemId,
        sSignOffUser,
        sSignOffPass,
        sSignOffReason
    );

    :IF bCompleted;
        UsrMes("Work item " + sWorkitemId + " completed with sign-off");
        :RETURN .T.;
    :ENDIF;

    sErrMsg := DocGetErrorMessage();

    :IF DocCommandFailed() .AND. .NOT. Empty(sErrMsg);
        UsrMes("Completion failed: " + sErrMsg);
    :ELSE;
        UsrMes("Completion failed for work item " + sWorkitemId);
    :ENDIF;

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("CompleteRegulatedWorkitem");
```

### Complete a batch of work items and stop on the first failure

Accepts a work item ID array and sign-off values as parameters, validates each ID is non-blank, and halts the batch immediately on the first failed completion with a specific or generic error message.

```ssl
:PROCEDURE CompleteWorkitemBatch;
    :PARAMETERS aWorkitemIds, sSignOffUser, sSignOffPass, sSignOffReason;
    :DECLARE nIndex, sWorkitemId, bCompleted, sErrMsg;

    :FOR nIndex := 1 :TO ALen(aWorkitemIds);
        sWorkitemId := aWorkitemIds[nIndex];

        :IF Empty(sWorkitemId);
            UsrMes("Work item IDs must not be blank");
            :RETURN .F.;
        :ENDIF;

        bCompleted := DocCompleteWorkitem(
            sWorkitemId,
            sSignOffUser,
            sSignOffPass,
            sSignOffReason
        );

        :IF .NOT. bCompleted;
            sErrMsg := DocGetErrorMessage();

            :IF DocCommandFailed() .AND. .NOT. Empty(sErrMsg);
                UsrMes("Failed to complete " + sWorkitemId + ": " + sErrMsg);
            :ELSE;
                UsrMes("Failed to complete " + sWorkitemId);
            :ENDIF;

            :RETURN .F.;
        :ENDIF;
    :NEXT;

    UsrMes("All work items completed successfully");

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc(
    "CompleteWorkitemBatch",
    {{"WI-2024-00142"}, "jsmith", "P@ssw0rd!", "Approved for release"}
);
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
