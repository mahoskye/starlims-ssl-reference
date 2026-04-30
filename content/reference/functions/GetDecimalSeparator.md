---
title: "GetDecimalSeparator"
summary: "Returns the current decimal separator as a string."
id: ssl.function.getdecimalseparator
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDecimalSeparator

Returns the current decimal separator as a string.

`GetDecimalSeparator` returns the current value of the decimal separator
setting. It takes no parameters and returns the separator text directly, such as
`.` or `,`. Use it when code needs the current decimal separator as text rather
than the numeric character code returned by [`GetDecimalSep`](GetDecimalSep.md).

## When to use

- When you need the current decimal separator as text.
- When building locale-aware numeric parsing or formatting logic.
- When comparing the active separator against a specific character.
- When restoring or logging the current separator around a temporary change.

## Syntax

```ssl
GetDecimalSeparator()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The current decimal separator.

## Best practices

!!! success "Do"
    - Retrieve the separator each time you need it, rather than storing it for long periods.
    - Use the value from this function in any numeric-to-string or string-to-numeric operation.
    - Validate numeric string inputs against the current separator returned by this function.

!!! failure "Don't"
    - Assume the value cannot change within the lifetime of your session. Dynamic retrieval ensures your logic always reflects the latest user or system setting.
    - Hardcode any decimal separator in your calculations or string formatting. Hardcoding reduces correctness, portability, and support for internationalization.
    - Trust user input to always use the correct separator for the environment. Validation prevents parsing errors and improves data quality when formats differ by user locale.

## Caveats

- If you cache the value and later change it with [`SetDecimalSeparator`](SetDecimalSeparator.md), the cached value will no longer match the current setting.

## Examples

### Display the current decimal separator

Display the current decimal separator in a user-facing message.

```ssl
:PROCEDURE DisplayDecimalSeparator;
	:DECLARE sDecimalSep, sSettingsLine;

	sDecimalSep := GetDecimalSeparator();
	sSettingsLine := "Decimal separator: " + sDecimalSep;

	UsrMes(sSettingsLine);
:ENDPROC;

/* Usage;
DoProc("DisplayDecimalSeparator");
```

[`UsrMes`](UsrMes.md) displays:

```
Decimal separator: .
```

### Validate user input against the active separator

Check whether a numeric text value uses the currently configured decimal separator.

```ssl
:PROCEDURE UsesCurrentDecimalSeparator;
	:PARAMETERS sRawInput;
	:DECLARE sDecimalSep, bHasDecimalSep, bHasComma, bHasPeriod;

	sDecimalSep := GetDecimalSeparator();
	bHasComma := "," $ sRawInput;
	bHasPeriod := "." $ sRawInput;
	bHasDecimalSep := sDecimalSep $ sRawInput;

	:IF bHasDecimalSep;
		/* Displays the matching-input message;
		UsrMes("Input uses the current decimal separator: " + sRawInput);
	:ELSE;
		:IF sDecimalSep == "," .AND. bHasPeriod;
			UsrMes("Input uses '.' but the current decimal separator is ','.");
		:ELSE;
			:IF sDecimalSep == "." .AND. bHasComma;
				UsrMes("Input uses ',' but the current decimal separator is '.'.");
			:ELSE;
				UsrMes("Input does not contain a decimal separator.");
			:ENDIF;
		:ENDIF;
	:ENDIF;

	:RETURN bHasDecimalSep;
:ENDPROC;

/* Usage;
DoProc("UsesCurrentDecimalSeparator", {"3.14"});
```

### Save and restore the separator around a temporary change

Capture the current separator, switch it temporarily, then restore the original value.

```ssl
:PROCEDURE RestoreDecimalSeparator;
	:DECLARE sOriginalSep, sPreviousSep, sCurrentSep, nSepCode;

	sOriginalSep := GetDecimalSeparator();
	sPreviousSep := SetDecimalSeparator(",");
	sCurrentSep := GetDecimalSeparator();
	nSepCode := GetDecimalSep();

	UsrMes("Previous: " + sPreviousSep);  /* Displays Previous: .;
	UsrMes("Current: " + sCurrentSep);  /* Displays Current: ,;
	UsrMes("Current code: " + LimsString(nSepCode));  /* Displays Current code: 44;

	SetDecimalSeparator(sOriginalSep);
:ENDPROC;

/* Usage;
DoProc("RestoreDecimalSeparator");
```

## Related

- [`GetDecimalSep`](GetDecimalSep.md)
- [`SetDecimalSeparator`](SetDecimalSeparator.md)
- [`string`](../types/string.md)
