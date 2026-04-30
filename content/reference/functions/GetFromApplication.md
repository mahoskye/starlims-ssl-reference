---
title: "GetFromApplication"
summary: "Returns a comma-separated string of connected usernames when called with the special key \"STARLIMSUSERS\" in a CUSTOM session context."
id: ssl.function.getfromapplication
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetFromApplication

Returns a comma-separated string of connected usernames when called with the special key `"STARLIMSUSERS"` in a `CUSTOM` session context.

`GetFromApplication` does not provide general application-variable lookup in the SSL implementation documented here. It recognizes one key only: `"STARLIMSUSERS"`. When that key is used and the current `Session:Mode` is `"CUSTOM"`, the function returns the connected usernames joined into a single comma-separated string.

For any other key, and for [`NIL`](../literals/nil.md) or empty input, the function returns [`NIL`](../literals/nil.md).
If the key is `"STARLIMSUSERS"` but the current session mode is not `"CUSTOM"`, the function returns an empty string. The function also expects the public `Session` variable to be available in the current execution context.

## When to use

- When you need the list of currently connected users as one comma-separated
  string.
- When building administrative or audit logic that only runs in `CUSTOM`
  session mode.
- When you need a quick application-wide user snapshot rather than a session-specific value.

## Syntax

```ssl
GetFromApplication(sKey)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sKey` | [string](../types/string.md) | yes | — | Lookup key. `"STARLIMSUSERS"` is the only documented key that returns a value. |

## Returns

**[string](../types/string.md)** — Comma-separated username list, empty string, or [`NIL`](../literals/nil.md) depending on the key and session context.

- [`NIL`](../literals/nil.md) when `sKey` is [`NIL`](../literals/nil.md), empty, or any value other than `"STARLIMSUSERS"`.
- Empty string when `sKey` is `"STARLIMSUSERS"` but `Session:Mode` is not `"CUSTOM"`.
- Comma-separated username list when `sKey` is `"STARLIMSUSERS"` and `Session:Mode` is `"CUSTOM"`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The public `Session` variable is not available in the current execution context. | `Variable [Session] is undefined!` |

## Best practices

!!! success "Do"
    - Pass `"STARLIMSUSERS"` when you want the connected-user list.
    - Treat both [`NIL`](../literals/nil.md) and empty string as non-usable results unless your code explicitly distinguishes them.
    - Use [`:TRY`](../keywords/TRY.md) and [`:CATCH`](../keywords/CATCH.md) if the code may run outside a context where the public `Session` variable exists.

!!! failure "Don't"
    - Assume arbitrary application keys are supported. This SSL function documents one special key only.
    - Assume a successful call always returns usernames. Non-`CUSTOM` sessions return an empty string.
    - Use [`ErrorMes`](ErrorMes.md) for routine absence handling. Reserve it for cases where missing context is genuinely a hard failure.

## Caveats

- Key matching is case-insensitive for `"STARLIMSUSERS"`.

## Examples

### Display the connected users list

Retrieves the connected users string and displays it when the current session mode supports the lookup.

```ssl
:PROCEDURE ShowConnectedUsers;
    :DECLARE sUsers;

    sUsers := GetFromApplication("STARLIMSUSERS");

    :IF Empty(sUsers);
        UsrMes("No connected users were returned.");
    :ELSE;
        UsrMes("Connected users: " + sUsers);
        /* Displays: connected users with the current list;
    :ENDIF;

    :RETURN sUsers;
:ENDPROC;

/*
Usage
;
DoProc("ShowConnectedUsers");
```

### Validate the key before calling

Guards the call so the function is only invoked with its one supported key, returning [`NIL`](../literals/nil.md) immediately for any other input.

```ssl
:PROCEDURE LookupConnectedUsers;
    :PARAMETERS sKey;
    :DECLARE sUsers, sMessage;

    sMessage := "";

    :IF .NOT. (Upper(sKey) == "STARLIMSUSERS");
        sMessage := "GetFromApplication only supports STARLIMSUSERS.";
        UsrMes(sMessage);
        :RETURN NIL;
    :ENDIF;

    sUsers := GetFromApplication(sKey);

    :IF Empty(sUsers);
        sMessage := "No users returned. Check whether Session:Mode is CUSTOM.";
    :ELSE;
        sMessage := "Connected users: " + sUsers;
    :ENDIF;

    UsrMes(sMessage); /* Displays: status for the lookup result;

    :RETURN sUsers;
:ENDPROC;

/*
Usage
;
DoProc("LookupConnectedUsers", {"STARLIMSUSERS"});
```

### Handle missing Session context safely

Wraps the lookup in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) so a missing `Session` variable or other runtime error is caught and reported rather than propagated.

```ssl
:PROCEDURE AuditConnectedUsers;
    :DECLARE sUsers, sReport, oErr;

    sReport := "";

    :TRY;
        sUsers := GetFromApplication("STARLIMSUSERS");

        :IF Empty(sUsers);
            sReport := "Audit skipped because no connected users were returned.";
            UsrMes(sReport);
            :RETURN sReport;
        :ENDIF;

        sReport := "Connected users at " + DToC(Today()) + " " + LimsTime();
        sReport := sReport + Chr(13) + Chr(10) + sUsers;

        UsrMes(sReport); /* Displays: connected users with a timestamp;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes(
            "Connected-user audit failed: " + oErr:Description
        ); /* Displays on failure: connected-user audit failed;
        :RETURN "";
    :ENDTRY;

    :RETURN sReport;
:ENDPROC;

/*
Usage
;
DoProc("AuditConnectedUsers");
```

## Related

- [`GetFromSession`](GetFromSession.md)
- [`ClearSession`](ClearSession.md)
- [`string`](../types/string.md)
