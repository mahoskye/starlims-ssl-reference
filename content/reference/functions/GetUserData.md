---
title: "GetUserData"
summary: "Returns the current session user name as a string."
id: ssl.function.getuserdata
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetUserData

Returns the current session user name as a string.

`GetUserData()` returns the user name currently stored in the session context for the running execution. It takes no parameters and performs no validation or authentication check. Use it when you need the current user name for messages, auditing, or to preserve and restore session context around a later [`SetUserData`](SetUserData.md) call.

## When to use

- When you need the current session user name for messages, audit text, or workflow decisions.
- When you need to save the current user before a temporary context switch with [`SetUserData`](SetUserData.md).
- When your code must check who is running the script before allowing or blocking an action.

## Syntax

```ssl
GetUserData();
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The current session user name.

## Best practices

!!! success "Do"
    - Use `GetUserData()` when you need the current session user for logging, audit text, or workflow decisions.
    - Save the current user with `GetUserData()` before temporarily changing the session context with [`SetUserData`](SetUserData.md).
    - Check for an empty result before treating the value as a usable user name.

!!! failure "Don't"
    - Use `GetUserData()` as proof that a user has been authenticated for a sensitive action.
    - Assume the returned value is non-empty without checking it.
    - Hard-code logic that depends on a previous user value after another part of the session may have changed it with [`SetUserData`](SetUserData.md).

## Caveats

- `GetUserData()` returns the current session value only; it does not look up other users.
- If the current session user changes, later calls return the updated value.

## Examples

### Show the current user in a message

Read the current session user name and include it in a user-facing message.

```ssl
:PROCEDURE ShowCurrentUser;
    :DECLARE sUserName;

    sUserName := GetUserData();

    UsrMes("Current user: " + sUserName);
:ENDPROC;

/* Usage;
DoProc("ShowCurrentUser");
```

[`UsrMes`](UsrMes.md) displays:

```text
Current user: jsmith
```

### Require a current user before continuing

Check that a current user is available before running logic that depends on it.

```ssl
:PROCEDURE ValidateCurrentUser;
    :DECLARE sUserName;

    sUserName := GetUserData();

    :IF Empty(sUserName);
        ErrorMes("This action requires a current user context.");
        :RETURN .F.;
    :ENDIF;

    UsrMes("Running as user: " + sUserName);

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateCurrentUser");
```

### Save and restore user context

Preserve the original user name before a temporary context switch, then restore it in [`:FINALLY`](../keywords/FINALLY.md).

```ssl
:PROCEDURE RunAsServiceUser;
    :PARAMETERS sServiceUser;
    :DECLARE sOriginalUser;

    sOriginalUser := GetUserData();

    :TRY;
        SetUserData(sServiceUser);
        UsrMes("Temporary user context: " + GetUserData());
    :FINALLY;
        SetUserData(sOriginalUser);
        UsrMes("Restored user context: " + GetUserData());
    :ENDTRY;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("RunAsServiceUser", {"svc_account"});
```

## Related

- [`ChkPassword`](ChkPassword.md)
- [`SetUserData`](SetUserData.md)
- [`string`](../types/string.md)
