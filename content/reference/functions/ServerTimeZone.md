---
title: "ServerTimeZone"
summary: "Returns the current server's UTC offset in minutes as a number."
id: ssl.function.servertimezone
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ServerTimeZone

Returns the current server's UTC offset in minutes as a number.

`ServerTimeZone()` returns the current difference, in minutes, between the server's local time and UTC. The value is read when the function is called, so it reflects the server's active timezone offset at that moment, including daylight saving adjustments when applicable. Use it when server-local timing is the right reference point. If you need the current user's offset instead, use [`UserTimeZone()`](UserTimeZone.md).

## When to use

- When you need the server's current UTC offset for logging or scheduling.
- When converting between UTC-based values and server-local time.
- When comparing server-local behavior with user-local behavior.
- When checking whether a deployment is running with the expected server offset.

## Syntax

```ssl
ServerTimeZone()
```

## Parameters

This function takes no parameters.

## Returns

**[number](../types/number.md)** — The server's current UTC offset in minutes. Positive values mean the server is ahead of UTC, and negative values mean it is behind UTC.

## Best practices

!!! success "Do"
    - Use `ServerTimeZone()` when logic must follow the server's local timezone rather than the current user's timezone.
    - Capture the value once per logical operation if multiple calculations must use the same offset.
    - Pair it with [`UserTimeZone()`](UserTimeZone.md) when you need to explain or handle server-versus-user time differences.

!!! failure "Don't"
    - Assume the server offset matches the current user's local timezone.
    - Treat the offset as a full timestamp or a complete timezone identity.
    - Assume the value stays constant across long periods or daylight saving transitions.

## Caveats

- The value is based on the server's current local time, so it can change when the server timezone or daylight saving offset changes.
- The result is a minute offset, not a timezone name.
- The offset can include non-hour increments such as 30-minute differences.

## Examples

### Display the current server UTC offset

Read the server's current UTC offset and display it. The value reflects any active daylight saving adjustment at the moment of the call.

```ssl
:PROCEDURE ShowServerOffset;
    :DECLARE nServerOffset, sMessage;

    nServerOffset := ServerTimeZone();

    sMessage := "Server UTC offset: " + LimsString(nServerOffset)
        + " minute(s)";
    UsrMes(sMessage);

    :RETURN nServerOffset;
:ENDPROC;

/* Usage;
DoProc("ShowServerOffset");
```

[`UsrMes`](UsrMes.md) displays:

```text
Server UTC offset: <±N> minute(s)
```

### Compare server and user timezone offsets

Read both offsets in one procedure and report whether the server and the current user share the same active UTC offset.

```ssl
:PROCEDURE CompareServerAndUserOffset;
    :DECLARE nServerOffset, nUserOffset, sMessage;

    nServerOffset := ServerTimeZone();
    nUserOffset := UserTimeZone();

    sMessage := "Server offset: " + LimsString(nServerOffset)
        + ", user offset: " + LimsString(nUserOffset);
    UsrMes(sMessage);
    /* Displays current offsets;

    :IF nServerOffset != nUserOffset;
        UsrMes("Server-local and user-local times may differ");
    :ELSE;
        UsrMes("Server and user are using the same current offset");
    :ENDIF;

    :RETURN nServerOffset;
:ENDPROC;

/* Usage;
DoProc("CompareServerAndUserOffset");
```

## Related

- [`UserTimeZone`](UserTimeZone.md)
- [`number`](../types/number.md)
