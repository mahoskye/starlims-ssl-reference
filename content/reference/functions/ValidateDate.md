---
title: "ValidateDate"
summary: "Checks whether a string can be interpreted as a valid date."
id: ssl.function.validatedate
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ValidateDate

Checks whether a string can be interpreted as a valid date.

`ValidateDate()` accepts a required string and an optional boolean flag.
When `bUseDateFormat` is omitted, [`NIL`](../literals/nil.md), or [`.T.`](../literals/true.md), the function validates the string with the normal date parsing path used by [`CToD`](CToD.md). When `bUseDateFormat` is [`.F.`](../literals/false.md), it switches to strict `yyyyMMdd` validation: the input must be numeric, must contain at least 8 characters, and only the first 8 characters are parsed.

The function returns [`.T.`](../literals/true.md) for valid dates and [`.F.`](../literals/false.md) for invalid date text. It does not silently accept bad argument types: `sDateString` must be non-null, and `bUseDateFormat` must be boolean when supplied.

## When to use

- When you need to validate user-entered date text before converting or saving it.
- When a workflow may receive dates either in the current date format or in strict `yyyyMMdd` form.
- When you want invalid date text to return [`.F.`](../literals/false.md) but still want bad argument types to fail fast.

## Syntax

```ssl
ValidateDate(sDateString, [bUseDateFormat])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sDateString` | [string](../types/string.md) | yes | — | Text to validate as a date. |
| `bUseDateFormat` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Controls the validation mode. Omit it, pass [`NIL`](../literals/nil.md), or pass [`.T.`](../literals/true.md) to use normal date-format parsing. Pass [`.F.`](../literals/false.md) to require strict `yyyyMMdd` validation. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the input is accepted as a valid date, otherwise [`.F.`](../literals/false.md).

In strict `yyyyMMdd` mode, values shorter than 8 characters or containing non-numeric characters return [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDateString` is [`NIL`](../literals/nil.md). | `Argument: sDateString cannot be null.` |
| `sDateString` is not a string. | `Argument: sDateString must be of string type.` |
| `bUseDateFormat` is supplied but is not boolean. | `Argument: bUseDateFormat must be of boolean type.` |

## Best practices

!!! success "Do"
    - Pass [`.F.`](../literals/false.md) explicitly when your input is supposed to be strict `yyyyMMdd` text.
    - Use the default behavior only when the incoming string is meant for normal date-format parsing.
    - Check the boolean result for invalid date text before calling conversion logic.

!!! failure "Don't"
    - Assume the default mode validates `yyyyMMdd` input the way strict import rules usually require.
    - Pass numbers, objects, or other non-string values just because they look date-like.
    - Expect values shorter than 8 characters to pass in strict `yyyyMMdd` mode.

## Examples

### Validate a strict `yyyyMMdd` import value

Pass [`.F.`](../literals/false.md) as the second argument to enable strict `yyyyMMdd` mode. A structurally valid date like `"20240315"` passes while a date like `"20240230"` (February 30) fails.

```ssl
:PROCEDURE ValidateImportDate;
    :DECLARE sImportDate, bValid;

    sImportDate := "20240315";
    bValid := ValidateDate(sImportDate, .F.);

    :IF bValid;
        UsrMes("Import date is valid: " + sImportDate);
        /* Displays a valid import-date status;
    :ELSE;
        UsrMes("Import date is invalid: " + sImportDate);
        /* Displays an invalid import-date status;
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("ValidateImportDate");
```

### Validate input in the current date format

Omit the second argument to validate user-entered text against the runtime's configured date format.

```ssl
:PROCEDURE ValidateEnteredDate;
    :PARAMETERS sEnteredDate;
    :DEFAULT sEnteredDate, "";
    :DECLARE bValid;

    bValid := ValidateDate(sEnteredDate);

    :IF bValid;
        UsrMes("Entered date is valid");
    :ELSE;
        UsrMes("Entered date is not valid for the current date format");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("ValidateEnteredDate", {"04/23/2026"});
```

### Apply mode-specific validation to rows from different sources

Choose the validation mode based on the source field: `SYSTEM` rows use strict `yyyyMMdd` mode; `USER` rows use the current date format. The second SYSTEM row (`"20240230"`) fails because February 30 is not a real date.

```ssl
:PROCEDURE ReviewIncomingDates;
    :DECLARE aRows, nIndex, sSource, sDateText, bUseDateFormat, bValid;
    :DECLARE nValidCount, nInvalidCount, sMessage;

    aRows := {
        {"SYSTEM", "20240419"},
        {"SYSTEM", "20240230"},
        {"USER", DToC(Today())}
    };

    nValidCount := 0;
    nInvalidCount := 0;

    :FOR nIndex := 1 :TO ALen(aRows);
        sSource := aRows[nIndex, 1];
        sDateText := aRows[nIndex, 2];
        bUseDateFormat := .NOT. (sSource == "SYSTEM");

        bValid := ValidateDate(sDateText, bUseDateFormat);

        :IF bValid;
            nValidCount := nValidCount + 1;
        :ELSE;
            nInvalidCount := nInvalidCount + 1;
            sMessage := sSource + " row has an invalid date: " + sDateText;
            UsrMes(sMessage);
            /* Displays an invalid-row message;
        :ENDIF;
    :NEXT;

    sMessage := "Valid rows: " + LimsString(nValidCount)
        + ", invalid rows: " + LimsString(nInvalidCount);
    UsrMes(sMessage);
    /* Displays the validation totals;
:ENDPROC;

/* Usage;
DoProc("ReviewIncomingDates");
```

## Related

- [`StringToDate`](StringToDate.md)
- [`LimsGetDateFormat`](LimsGetDateFormat.md)
- [`DateFromNumbers`](DateFromNumbers.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
