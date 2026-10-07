---
title: "SetUserData"
summary: "Sets the current user name for the active execution context."
id: ssl.function.setuserdata
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# SetUserData

Sets the current user name for the active execution context.

`SetUserData` accepts one argument, `sUserName`, and updates the value returned by [`GetUserData`](GetUserData.md). The function requires a non-empty string. If you pass [`NIL`](../literals/nil.md), an empty string, or a value that is not a string, it raises an argument error.

`SetUserData` only validates the input and updates the current execution context. It does not perform authentication, confirm that the user exists, or return a result value.

## When to use

- When you need later code in the same execution context to run under a
  different current user name.
- When you need to temporarily change the current user and then restore the
  previous value.
- When you want [`GetUserData()`](GetUserData.md) to report a specific user name for the rest of the current flow.

## Syntax

```ssl
SetUserData(sUserName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sUserName` | [string](../types/string.md) | yes | — | Non-empty user name to store in the current execution context. |

## Returns

**NIL** — `SetUserData` updates context state and does not return a value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sUserName` is [`NIL`](../literals/nil.md), not a string, or empty. | `Argument: userName must be a non-empty string.` |

## Best practices

!!! success "Do"
    - Save the current user with [`GetUserData`](GetUserData.md) before changing it when you need to restore it later.
    - Pass a known non-empty string value.
    - Keep the scope of the user change as small as practical.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), an empty string, or a non-string value.
    - Assume this function authenticates the user or verifies that the user exists.
    - Change the current user without restoring the previous value when later code depends on the original context.
    - Log with [`UsrMes`](UsrMes.md) while the user name is switched and expect the message in your own user log. It goes to the log of the user name you set.

## Caveats

- The change affects the current execution context immediately.
- While the session user name is changed, messages written with [`UsrMes`](UsrMes.md) go to the user log of the name you set, not to your own log (verified in Designer). Capture anything you need to report, restore the original user name, then log.

## Examples

### Set the current user name

Use `SetUserData`, confirm the change with [`GetUserData`](GetUserData.md), and restore the original user name before logging the result.

```ssl
:PROCEDURE ShowCurrentUser;
    :DECLARE sOriginalUser, sCurrentUser;

    sOriginalUser := GetUserData();

    SetUserData("jsmith");
    sCurrentUser := GetUserData();

    SetUserData(sOriginalUser);

    UsrMes("Current user: " + sCurrentUser);
:ENDPROC;

/* Usage;
DoProc("ShowCurrentUser");
```

[`UsrMes`](UsrMes.md) logs:

```text
Current user: jsmith
```

### Change the user temporarily and restore the original

Store the original value before switching, restore it after the work is done, and log once it is restored.

```ssl
:PROCEDURE RunAsReviewer;
    :DECLARE sOriginalUser, sReviewUser, sRanAs;

    sOriginalUser := GetUserData();
    sReviewUser := "REVIEWER";

    :TRY;
        SetUserData(sReviewUser);
        sRanAs := GetUserData();
    :FINALLY;
        SetUserData(sOriginalUser);
    :ENDTRY;

    /* Logged after restoring the user name, so the messages reach your own log;
    UsrMes("Ran as: " + sRanAs);
    UsrMes("Review work completed");
:ENDPROC;

/* Usage;
DoProc("RunAsReviewer");
```

### Validate a candidate value before switching

Check the input first so the function is called only with a non-empty string.

```ssl
:PROCEDURE ApplyRequestedUser;
    :PARAMETERS sRequestedUser;
    :DECLARE sOriginalUser, sActiveUser;

    :IF Empty(sRequestedUser);
        UsrMes("A user name is required");
        :RETURN;
    :ENDIF;

    sOriginalUser := GetUserData();

    :TRY;
        SetUserData(sRequestedUser);
        sActiveUser := GetUserData();
    :FINALLY;
        SetUserData(sOriginalUser);
    :ENDTRY;

    UsrMes("Active user: " + sActiveUser);
:ENDPROC;

/* Usage;
DoProc("ApplyRequestedUser", {"jsmith"});
```

## Related

- [`GetUserData`](GetUserData.md)
- [`string`](../types/string.md)
