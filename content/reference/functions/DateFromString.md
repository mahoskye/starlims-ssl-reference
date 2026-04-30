---
title: "DateFromString"
summary: "Parses a string into a date value with optional format and culture controls."
id: ssl.function.datefromstring
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DateFromString

Parses a string into a date value with optional format and culture controls.

`DateFromString` accepts a required source string plus optional format, culture, and date-handling controls. When `vFormat` is omitted, the function uses the selected culture's normal date parsing rules. When `vFormat` is a string or an array of strings, the input must match one of those formats exactly.

By default, parsing uses invariant culture. Pass `bUseLocalCulture` as [`.T.`](../literals/true.md) to parse with the current local culture instead. By default, the returned value is marked as a local date. Pass `bMakeInvariant` as [`.T.`](../literals/true.md) to return the parsed value as an unspecified date.

## When to use

- When incoming text may use one of several known date formats.
- When you need to parse using invariant culture by default, or explicitly opt into the current local culture.
- When a workflow needs to control whether the resulting date is local or unspecified.
- When strict format matching is preferred over relying on the current SSL date format alone.

## Syntax

```ssl
DateFromString(sDateAsString, [vFormat], [bUseLocalCulture], [bMakeInvariant])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDateAsString` | [string](../types/string.md) | yes | — | Source text to parse. |
| `vFormat` | [string](../types/string.md), [array](../types/array.md), or NIL | no | [`NIL`](../literals/nil.md) | Exact format to use, or an array of exact formats to try. When omitted, the function uses standard parsing for the selected culture. |
| `bUseLocalCulture` | [boolean](../types/boolean.md) or NIL | no | [`NIL`](../literals/nil.md) | When [`.T.`](../literals/true.md), parse with the current local culture. When [`NIL`](../literals/nil.md) or [`.F.`](../literals/false.md), parse with invariant culture. |
| `bMakeInvariant` | [boolean](../types/boolean.md) or NIL | no | [`NIL`](../literals/nil.md) | When [`.T.`](../literals/true.md), return an unspecified date. When [`NIL`](../literals/nil.md) or [`.F.`](../literals/false.md), return a local date. |

## Returns

**[date](../types/date.md)** — The parsed date value, marked as local when `bMakeInvariant` is [`NIL`](../literals/nil.md) or [`.F.`](../literals/false.md), or as an unspecified date when `bMakeInvariant` is [`.T.`](../literals/true.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDateAsString` is [`NIL`](../literals/nil.md). | A null argument exception. The exact runtime message is platform-dependent. |
| `vFormat` is not [`NIL`](../literals/nil.md), a string, or an array. | `Argument 'vFormat' can be NIL, string or array.` |
| `bUseLocalCulture` is not [`NIL`](../literals/nil.md) and not a boolean. | `Argument 'bUseLocalCulture' can be NIL or boolean.` |
| `bMakeInvariant` is not [`NIL`](../literals/nil.md) and not a boolean. | `Argument 'bMakeInvariant' can be NIL or boolean.` |
| The text cannot be parsed by the selected culture and format. | A format exception. |

## Best practices

!!! success "Do"
    - Pass an explicit format when the incoming text is expected to follow a known pattern.
    - Pass an array of formats when imported data can legitimately arrive in more than one exact shape.
    - Use `useLocalCulture` only when the input is intentionally tied to the current local culture.
    - Handle parse failures with [`:TRY`](../keywords/TRY.md) and [`:CATCH`](../keywords/CATCH.md) when invalid input is possible.

!!! failure "Don't"
    - Assume omitted `vFormat` means local-culture parsing. The default is invariant culture unless `bUseLocalCulture` is [`.T.`](../literals/true.md).
    - Use `DateFromString` when you want a quiet parse failure. This function raises an error when parsing fails.
    - Treat `bMakeInvariant` as time-zone conversion. It changes how the parsed date is marked, not the clock value.
    - Pass unsupported argument types and rely on implicit conversion. The function validates `vFormat`, `bUseLocalCulture`, and `bMakeInvariant`.

## Caveats

- `sDateAsString` is expected to be a string value.
- Use [`StringToDate`](StringToDate.md) when you want exact-format parsing that returns an empty date instead of raising an error.
- Use [`CToD`](CToD.md) when the input follows the current SSL date format.

## Examples

### Parse a date with one explicit format

Parses an ISO-style date string by supplying the exact format, then displays the result using the current SSL date format.

```ssl
:PROCEDURE ParseIsoDate;
    :DECLARE sDateInput, dParsedDate;

    sDateInput := "2026-04-11";

    dParsedDate := DateFromString(sDateInput, "yyyy-MM-dd");

    UsrMes("Parsed date: " + DToC(dParsedDate));
:ENDPROC;

/* Usage;
DoProc("ParseIsoDate");
```

[`UsrMes`](UsrMes.md) displays (assuming MM/DD/YYYY date format):

```text
Parsed date: 04/11/2026
```

### Accept several exact import formats

Parses an imported date field that may arrive in one of several approved formats, using an array of format strings and catching failures with [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md).

```ssl
:PROCEDURE ParseImportedDate;
	:DECLARE aFormats, dParsedDate, oErr, sDateInput;

	sDateInput := "25.04.2024";
	aFormats := {"yyyy-MM-dd", "MM/dd/yyyy", "dd.MM.yyyy", "yyyyMMdd"};

	:TRY;
		dParsedDate := DateFromString(sDateInput, aFormats);
		UsrMes("Imported date: " + DToC(dParsedDate));

	:CATCH;
		oErr := GetLastSSLError();
		UsrMes("Could not parse imported date: " + oErr:Description);
		/* Displays on failure: Could not parse imported date;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ParseImportedDate");
```

### Parse local-culture input and keep the result unspecified

Passes [`.T.`](../literals/true.md) for both `bUseLocalCulture` and `bMakeInvariant` to parse a user-entered date string with the current local culture while marking the result as an unspecified date.

```ssl
:PROCEDURE ParseLocalDateForStorage;
	:DECLARE dParsedDate, oErr, sDateInput;

	sDateInput := "11/04/2026";

	:TRY;
		dParsedDate := DateFromString(sDateInput,, .T., .T.);
		UsrMes("Accepted date: " + DToC(dParsedDate));

	:CATCH;
		oErr := GetLastSSLError();
		UsrMes("Date input is invalid: " + oErr:Description);
		/* Displays on failure: Date input is invalid;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ParseLocalDateForStorage");
```

## Related

- [`CToD`](CToD.md)
- [`DToC`](DToC.md)
- [`DToS`](DToS.md)
- [`DateFromNumbers`](DateFromNumbers.md)
- [`DateToString`](DateToString.md)
- [`IsInvariantDate`](IsInvariantDate.md)
- [`MakeDateInvariant`](MakeDateInvariant.md)
- [`StringToDate`](StringToDate.md)
- [`date`](../types/date.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
