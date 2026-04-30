---
title: "SetUserData"
summary: "Sets the current user name for the active execution context."
id: ssl.function.setuserdata
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
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
SetUserData(sUserName);
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
| `sUserName` is [`NIL`](../literals/nil.md), not a string, or empty. | `Argument: sUserName must be a non-empty string.` |

## Best practices

!!! success "Do"
    - Save the current user with [`GetUserData`](GetUserData.md) before changing it when you need to restore it later.
    - Pass a known non-empty string value.
    - Keep the scope of the user change as small as practical.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), an empty string, or a non-string value.
    - Assume this function authenticates the user or verifies that the user exists.
    - Change the current user without restoring the previous value when later code depends on the original context.

## Caveats

- The change affects the current execution context immediately.

## Examples

### Set the current user name

Use `SetUserData` and then confirm the change with [`GetUserData`](GetUserData.md).

```ssl
:PROCEDURE ShowCurrentUser;
    :DECLARE sUserName, sCurrentUser;

    sUserName := "jsmith";
    SetUserData(sUserName);

    sCurrentUser := GetUserData();
    UsrMes("Current user: " + sCurrentUser);
:ENDPROC;

/* Usage;
DoProc("ShowCurrentUser");
```

[`UsrMes`](UsrMes.md) displays:

```text
Current user: jsmith
```

### Change the user temporarily and restore the original

Store the original value before switching, then restore it after the work is done.

```ssl
:PROCEDURE RunAsReviewer;
    :DECLARE sOriginalUser, sReviewUser;

    sOriginalUser := GetUserData();
    sReviewUser := "REVIEWER";

    :TRY;
        SetUserData(sReviewUser);
        UsrMes("Running as: " + GetUserData());
        UsrMes("Review work completed");
    :FINALLY;
        SetUserData(sOriginalUser);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("RunAsReviewer");
```

### Validate a candidate value before switching

Check the input first so the function is called only with a non-empty string.

```ssl
:PROCEDURE ApplyRequestedUser;
    :PARAMETERS sRequestedUser;
    :DECLARE sOriginalUser;

    :IF Empty(sRequestedUser);
        UsrMes("A user name is required");
        :RETURN;
    :ENDIF;

    sOriginalUser := GetUserData();

    :TRY;
        SetUserData(sRequestedUser);
        UsrMes("Active user: " + GetUserData());
    :FINALLY;
        SetUserData(sOriginalUser);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ApplyRequestedUser", {"jsmith"});
```

## Related

- [`GetUserData`](GetUserData.md)
- [`string`](../types/string.md)
