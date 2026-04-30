---
title: "GetDecimalSep"
summary: "Returns the current decimal separator as a numeric character code."
id: ssl.function.getdecimalsep
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDecimalSep

Returns the current decimal separator as a numeric character code.

`GetDecimalSep` returns the byte value of the current decimal separator's first character. If no decimal separator is configured, it falls back to the byte value for `.`. Use this legacy-style API when you need the separator as a number rather than as a one-character string.

## When to use

- When existing code expects the decimal separator as a numeric character code.
- When you need to convert the separator code back to a character with [`Chr`](Chr.md).
- When you want a safe fallback to `.` if the separator setting is empty.

## Syntax

```ssl
GetDecimalSep()
```

## Parameters

This function takes no parameters.

## Returns

**[number](../types/number.md)** — The byte value of the current decimal separator character. If the configured separator is empty, the function returns the byte value for `.`.

## Best practices

!!! success "Do"
    - Use `GetDecimalSep` when you specifically need a numeric character code.
    - Convert the return value with [`Chr`](Chr.md) before comparing it to string input.
    - Prefer [`GetDecimalSeparator`](GetDecimalSeparator.md) when you need the separator as text.

!!! failure "Don't"
    - Treat the return value as the separator character itself. It is a number, not a string.
    - Hardcode ASCII values such as `46` unless the separator must be fixed by design.
    - Assume a multi-character separator is preserved. This function uses only the first character.

## Examples

### Show the current separator code and character

Retrieve the separator as a numeric code, then convert it to a displayable character.

```ssl
:PROCEDURE ShowDecimalSeparator;
    :DECLARE nSepCode, sSepChar, sMessage;

    nSepCode := GetDecimalSep();
    sSepChar := Chr(nSepCode);

    sMessage := "Decimal separator code: " + LimsString(nSepCode)
		        + " character: " + sSepChar;

    UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("ShowDecimalSeparator");
```

[`UsrMes`](UsrMes.md) displays:

```text
Decimal separator code: 46 character: .
```

### Normalize input using the active separator

Convert a locale-formatted numeric string to a `.`-based form before further processing.

```ssl
:PROCEDURE NormalizeNumericText;
    :PARAMETERS sRawValue;
    :DECLARE nSepCode, sSepChar, sNormalized;

    nSepCode := GetDecimalSep();
    sSepChar := Chr(nSepCode);
    sNormalized := StrTran(sRawValue, sSepChar, ".");

    UsrMes("Normalized value: " + sNormalized);

    :RETURN sNormalized;
:ENDPROC;

/* Usage;
DoProc("NormalizeNumericText", {"3,14"});
```

[`UsrMes`](UsrMes.md) displays:

```text
Normalized value: 3.14
```

### Compare the numeric and string separator APIs

Use [`SetDecimalSeparator`](SetDecimalSeparator.md) to change the current separator, then verify the value through both `GetDecimalSep` and [`GetDecimalSeparator`](GetDecimalSeparator.md).

```ssl
:PROCEDURE VerifyDecimalSeparatorApis;
    :DECLARE sPrevSep, nSepCode, sSepChar, sCurrentSep;

    sPrevSep := SetDecimalSeparator(",");

    nSepCode := GetDecimalSep();
    sSepChar := Chr(nSepCode);
    sCurrentSep := GetDecimalSeparator();

    UsrMes("Code: " + LimsString(nSepCode)
	        + " character: " + sSepChar
	        + " string API: " + sCurrentSep);

    SetDecimalSeparator(sPrevSep);
:ENDPROC;

/* Usage;
DoProc("VerifyDecimalSeparatorApis");
```

[`UsrMes`](UsrMes.md) displays:

```text
Code: 44 character: , string API: ,
```

## Related

- [`GetDecimalSeparator`](GetDecimalSeparator.md)
- [`SetDecimalSeparator`](SetDecimalSeparator.md)
- [`number`](../types/number.md)
