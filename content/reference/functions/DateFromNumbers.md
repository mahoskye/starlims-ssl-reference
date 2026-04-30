---
title: "DateFromNumbers"
summary: "Creates a date value from individual numeric components."
id: ssl.function.datefromnumbers
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DateFromNumbers

Creates a date value from individual numeric components.

`DateFromNumbers` builds a date from separate year, month, day, hour, minute, second, and millisecond values.

All arguments are optional. Omitted arguments and arguments passed as [`NIL`](../literals/nil.md) use the same defaults: `1` for year, month, and day, and `0` for hour, minute, second, and millisecond.

When a numeric argument is supplied, it must be an integer. The optional `bMakeInvariant` argument may be [`NIL`](../literals/nil.md) or boolean. By default the function returns a local date. When `bMakeInvariant` is [`.T.`](../literals/true.md), it returns an invariant date.

## When to use

- When you already have date parts as numbers instead of a formatted string.
- When you need to build a date from partial numeric input and rely on the function's defaults for omitted parts.
- When you need to include time components in the constructed date.
- When you need an invariant date instead of a local one.

## Syntax

```ssl
DateFromNumbers(
    [nYear],
    [nMonth],
    [nDay],
    [nHour],
    [nMinute],
    [nSecond],
    [nMillisecond],
    [bMakeInvariant]
)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nYear` | [number](../types/number.md) | no | `1` | Year component. When supplied, it must be an integer. |
| `nMonth` | [number](../types/number.md) | no | `1` | Month component. When supplied, it must be an integer. |
| `nDay` | [number](../types/number.md) | no | `1` | Day component. When supplied, it must be an integer. |
| `nHour` | [number](../types/number.md) | no | `0` | Hour component. When supplied, it must be an integer. |
| `nMinute` | [number](../types/number.md) | no | `0` | Minute component. When supplied, it must be an integer. |
| `nSecond` | [number](../types/number.md) | no | `0` | Second component. When supplied, it must be an integer. |
| `nMillisecond` | [number](../types/number.md) | no | `0` | Millisecond component. When supplied, it must be an integer. |
| `bMakeInvariant` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Optional flag that controls the returned date kind. Use [`.T.`](../literals/true.md) to return an invariant date. [`NIL`](../literals/nil.md) and [`.F.`](../literals/false.md) return a local date. |

## Returns

**[date](../types/date.md)** — A date built from the supplied components. When all arguments are omitted, returns a local date with year 1, month 1, day 1, and time `00:00:00.000`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| A numeric component is supplied but is not an integer. `<name>` is one of: `year`, `month`, `day`, `hour`, `minute`, `second`, `millisecond`. | `Argument: <name> must be an integer.` |
| `bMakeInvariant` is not [`NIL`](../literals/nil.md) and not a boolean. | `Argument 'makeInvariant' can be NIL or boolean.` |

## Best practices

!!! success "Do"
    - Validate imported numeric parts before calling the function.
    - Stop at the last component you actually need instead of passing unnecessary trailing arguments.
    - Use `bMakeInvariant` only when your workflow needs an invariant date.
    - Use [`DateFromString`](DateFromString.md) or [`StringToDate`](StringToDate.md) when the source value starts as text.

!!! failure "Don't"
    - Pass fractional numbers such as `2024.5` or `10.25` for date parts.
    - Assume invalid combinations such as February 30 will be corrected automatically.
    - Pass strings for numeric parts just because they look numeric.
    - Set `bMakeInvariant` to non-boolean values.

## Caveats

- The function does not coerce fractional numbers to integers.
- Invalid date combinations such as an out-of-range month or a non-existent calendar day raise a date construction error.

## Examples

### Build a date from year, month, and day values

Constructs a date from three separate numeric variables and displays the result. The time components default to `00:00:00.000`.

```ssl
:PROCEDURE BuildSampleDate;
	:DECLARE nYear, nMonth, nDay, dSampleDate;

	nYear := 2024;
	nMonth := 11;
	nDay := 15;

	dSampleDate := DateFromNumbers(nYear, nMonth, nDay);

	UsrMes("Sample date constructed: " + LimsString(dSampleDate));

	:RETURN dSampleDate;
:ENDPROC;

/* Usage;
DoProc("BuildSampleDate");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sample date constructed: 11/15/2024
```

### Build a full timestamp from numeric date and time parts

Passes all seven numeric components including milliseconds to construct a full timestamp. [`LimsString`](LimsString.md) on a date value uses the `MM/dd/yyyy` format and does not include the time portion.

```ssl
:PROCEDURE BuildRunTimestamp;
	:DECLARE dRunAt;

	dRunAt := DateFromNumbers(2026, 4, 18, 14, 30, 45, 125);

	UsrMes("Run timestamp: " + LimsString(dRunAt));

	:RETURN dRunAt;
:ENDPROC;

/* Usage;
DoProc("BuildRunTimestamp");
```

[`UsrMes`](UsrMes.md) displays:

```text
Run timestamp: 04/18/2026
```

### Create an invariant date and verify it

Passes [`.T.`](../literals/true.md) for `bMakeInvariant` and skips the time components with positional commas, then uses [`IsInvariantDate`](IsInvariantDate.md) to confirm the returned date kind.

```ssl
:PROCEDURE BuildInvariantReviewDate;
	:DECLARE nYear, nMonth, nDay, dReviewDate, bInvariant, sMessage;

	nYear := 2026;
	nMonth := 4;
	nDay := 18;

	dReviewDate := DateFromNumbers(nYear, nMonth, nDay,,,,, .T.);
	bInvariant := IsInvariantDate(dReviewDate);

	:IF bInvariant;
		sMessage := "Review date created as invariant";
	:ELSE;
		sMessage := "Review date is local";
	:ENDIF;

	UsrMes(sMessage);

	:RETURN dReviewDate;
:ENDPROC;

/* Usage;
DoProc("BuildInvariantReviewDate");
```

[`UsrMes`](UsrMes.md) displays:

```text
Review date created as invariant
```

## Related

- [`CToD`](CToD.md)
- [`DToC`](DToC.md)
- [`DToS`](DToS.md)
- [`DateFromString`](DateFromString.md)
- [`DateToString`](DateToString.md)
- [`IsInvariantDate`](IsInvariantDate.md)
- [`MakeDateInvariant`](MakeDateInvariant.md)
- [`StringToDate`](StringToDate.md)
- [`ValidateDate`](ValidateDate.md)
- [`date`](../types/date.md)
- [`number`](../types/number.md)
- [`boolean`](../types/boolean.md)
