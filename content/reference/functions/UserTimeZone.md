---
title: "UserTimeZone"
summary: "Returns the current user's UTC offset in minutes. If a user-specific offset is not available as a numeric value, the function returns the server's UTC offset instead."
id: ssl.function.usertimezone
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# UserTimeZone

Returns the current user's UTC offset in minutes. If a user-specific offset is not available as a numeric value, the function returns the server's UTC offset instead.

Use `UserTimeZone()` when you need a minute-based offset for user-local time display or conversion logic. The function takes no parameters and always returns the effective offset as a [number](../types/number.md).

## When to use

- When you need to convert UTC-based values to the current user's local time.
- When user-visible timestamps should follow the user's timezone when available.
- When a server-offset fallback is acceptable if no user-specific numeric offset is available.

## Syntax

```ssl
UserTimeZone()
```

## Parameters

This function takes no parameters.

## Returns

**[number](../types/number.md)** — The UTC offset in minutes for the current user. If the runtime cannot obtain a numeric user offset, the function returns the same value that [`ServerTimeZone`](ServerTimeZone.md) would return.

## Best practices

!!! success "Do"
    - Treat the return value as **minutes**, not hours.
    - Use [`ServerTimeZone`](ServerTimeZone.md) alongside `UserTimeZone()` when you need to compare user and server offsets explicitly.
    - Label user-visible times clearly when timezone context matters.

!!! failure "Don't"
    - Assume the returned value proves that a user-specific timezone was available; the server offset may have been used as a fallback.
    - Hardcode timezone offsets for user-facing logic when the current session can supply one.
    - Add the return value as if it were hours; convert or format it as minutes.

## Caveats

- A non-numeric user timezone value does not raise a documented exception here; the function falls back to the server offset.
- Equality between `UserTimeZone()` and [`ServerTimeZone`](ServerTimeZone.md) does not by itself prove that a fallback occurred; the user and server may simply share the same offset.

## Examples

### Compare user and server UTC offsets

Fetch both the user and server UTC offsets and log their difference. Both values are in minutes. The actual numbers depend on the current session's timezone configuration. The output below uses UTC-5 as a sample user offset.

```ssl
:PROCEDURE CompareTimeZones;
	:DECLARE nUserOffset, nServerOffset, nDifference;
	:DECLARE sMessage;

	nUserOffset := UserTimeZone();
	nServerOffset := ServerTimeZone();

	nDifference := nUserOffset - nServerOffset;

	sMessage := "User offset: " + LimsString(nUserOffset)
	+ " minutes, server offset: " + LimsString(nServerOffset)
	+ " minutes, difference: " + LimsString(nDifference) + " minutes";

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("CompareTimeZones");
```

`UsrMes` displays:

```text
User offset: -300 minutes, server offset: 0 minutes, difference: -300 minutes
```

### Convert a UTC time-of-day to user local time

Shift a fixed UTC time (14:30) into the user's local time using the minute-based offset. The modulo-and-clamp loop handles offsets that would otherwise push the result below midnight or past the end of the day. The output below assumes a UTC-5 user offset.

```ssl
:PROCEDURE ShowLocalCutoffTime;
	:DECLARE nUtcMinutes, nLocalMinutes, nUserOffset;
	:DECLARE nHours, nMinutes;
	:DECLARE sHours, sMinutes, sMessage;

	/* 14:30 UTC stored as minutes from midnight;
	nUtcMinutes := 14 * 60 + 30;
	nUserOffset := UserTimeZone();
	nLocalMinutes := nUtcMinutes + nUserOffset;

	:WHILE nLocalMinutes < 0;
		nLocalMinutes += 24 * 60;
	:ENDWHILE;

	:WHILE nLocalMinutes >= 24 * 60;
		nLocalMinutes -= 24 * 60;
	:ENDWHILE;

	nHours := Integer(nLocalMinutes / 60);
	nMinutes := nLocalMinutes % 60;

	sHours := LimsString(nHours);
	sMinutes := LimsString(nMinutes);

	:IF nHours < 10;
		sHours := "0" + sHours;
	:ENDIF;

	:IF nMinutes < 10;
		sMinutes := "0" + sMinutes;
	:ENDIF;

	sMessage := "Local cutoff time: " + sHours + ":" + sMinutes;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("ShowLocalCutoffTime");
```

`UsrMes` displays:

```text
Local cutoff time: 09:30
```

## Related

- [`ServerTimeZone`](ServerTimeZone.md)
- [`number`](../types/number.md)
