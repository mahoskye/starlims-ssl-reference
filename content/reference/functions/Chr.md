---
title: "Chr"
summary: "Converts a numeric character code to a single-character string."
id: ssl.function.chr
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Chr

Converts a numeric character code to a single-character string.

`Chr` takes one optional numeric value and returns the corresponding single character. If `nAsciiCode` is omitted or [`NIL`](../literals/nil.md), the function uses `0`. Fractional values are rounded to the nearest whole number using away-from-zero rounding before conversion. Rounded values outside `0` through `65535` raise an error. Use [`Asc`](Asc.md) for the reverse operation.

## When to use

- When you need a specific character but only have its numeric code.
- When you need control characters such as line feed, tab, or separators.
- When building strings that include delimiters or protocol markers.

## Syntax

```ssl
Chr([nAsciiCode])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nAsciiCode` | [number](../types/number.md) | no | `0` | Numeric character code to convert. If omitted or [`NIL`](../literals/nil.md), `Chr` uses `0`. Fractional values are rounded to the nearest whole number using away-from-zero rounding before conversion. |

## Returns

**[string](../types/string.md)** — The single-character string for the rounded character code.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The rounded value is outside the supported character-code range `0` through `65535`. | Raises an error. |

## Best practices

!!! success "Do"
    - Validate computed values before calling `Chr` when the input may fall outside the valid character range.
    - Use [`Asc`](Asc.md) when you need the numeric code for an existing character.
    - Use named variables for control characters so their purpose stays clear in surrounding code.

!!! failure "Don't"
    - Assume `Chr` silently clamps or wraps invalid values. Invalid codes raise an error.
    - Pass fractional values when exact character selection matters. `Chr` rounds before converting.
    - Use unexplained numeric literals repeatedly when a named variable would make the character's purpose clearer.

## Caveats

- `Chr()` and `Chr(NIL)` both behave like `Chr(0)`.
- Some valid character codes produce non-printable characters, so the result may not display visibly even though the function succeeded.

## Examples

### Insert a line feed between two lines

Stores `Chr(10)` in a variable and uses it to place a line feed between two lines of text before displaying the result.

```ssl
:PROCEDURE InsertNewlineCharacter;
    :DECLARE sLine1, sLine2, sOutput, sNewline;

    sLine1 := "This is the first line.";
    sLine2 := "This is the second line.";

    sNewline := Chr(10);

    sOutput := sLine1 + sNewline + sLine2;

    UsrMes(sOutput);
:ENDPROC;

/* Usage;
DoProc("InsertNewlineCharacter");
```

[`UsrMes`](UsrMes.md) displays:

```text
This is the first line.
This is the second line.
```

### Build a tab-delimited string from an array

Assigns `Chr(9)` to a named variable once and reuses it as the tab delimiter while joining five numbers into one string.

```ssl
:PROCEDURE BuildTabDelimitedList;
    :DECLARE aNumbers, sResult, nIndex, sTab;

    aNumbers := {12, 34, 56, 78, 90};
    sTab := Chr(9);

    sResult := LimsString(aNumbers[1]);

    :FOR nIndex := 2 :TO ALen(aNumbers);
        sResult := sResult + sTab + LimsString(aNumbers[nIndex]);
    :NEXT;

    UsrMes(sResult);
:ENDPROC;

/* Usage;
DoProc("BuildTabDelimitedList");
```

[`UsrMes`](UsrMes.md) displays:

```text
12	34	56	78	90
```

### Build a message with protocol control separators

Combines unit separator (`Chr(31)`) and record separator (`Chr(30)`) control characters to build a structured protocol payload. Non-printable characters are shown symbolically in the output.

```ssl
:PROCEDURE EmbedProtocolControlCodes;
    :DECLARE sUnitSeparator, sRecordSeparator, sData, sField1, sField2;
    :DECLARE sField3, sPayload;

    sUnitSeparator := Chr(31);
    sRecordSeparator := Chr(30);

    sField1 := "Sample123";
    sField2 := "Pending";
    sField3 := "2024-04-11";

    sData := sField1 + sUnitSeparator
	         + sField2 + sUnitSeparator
	         + sField3 + sRecordSeparator;

    sPayload := "TXSEND" + sUnitSeparator + sData;

    UsrMes("Payload with protocol control codes: " + sPayload);
:ENDPROC;

/* Usage;
DoProc("EmbedProtocolControlCodes");
```

[`UsrMes`](UsrMes.md) displays (with `<US>` = `Chr(31)` and `<RS>` = `Chr(30)`):

```text
Payload with protocol control codes: TXSEND<US>Sample123<US>Pending<US>2024-04-11<RS>
```

## Related

- [`Asc`](Asc.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
