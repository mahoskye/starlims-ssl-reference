---
title: "ValidateNumeric"
summary: "Determines whether a string is a valid numeric value under the current STARLIMS numeric settings."
id: ssl.function.validatenumeric
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ValidateNumeric

Determines whether a string is a valid numeric value under the current STARLIMS numeric settings.

`ValidateNumeric` checks whether `sNumber` matches the runtime's current numeric validation rules. It trims surrounding whitespace, never accepts hexadecimal input, and returns [`.T.`](../literals/true.md) only when the string is accepted as a numeric value under the active decimal and group separator settings.

Blank strings return [`.F.`](../literals/false.md). Inputs with more than one configured decimal separator return [`.F.`](../literals/false.md). Group separators are only accepted when the current numeric settings allow them. Passing [`NIL`](../literals/nil.md) for `sNumber` raises an error instead of returning [`.F.`](../literals/false.md).

In environments using the legacy numeric validation rules, `ValidateNumeric` behaves like [`IsNumeric`](IsNumeric.md)`(sNumber, .F.)`.

## When to use

- When validating text input before calling [`Val`](Val.md) or [`ToNumeric`](ToNumeric.md).
- When imported data must follow the current decimal and group separator settings.
- When hexadecimal values must be rejected.

## Syntax

```ssl
ValidateNumeric(sNumber)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sNumber` | [string](../types/string.md) | yes | — | String to validate. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when `sNumber` is valid under the current numeric settings; otherwise [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sNumber` is [`NIL`](../literals/nil.md). | `Argument sNumber cannot be null.` |

## Best practices

!!! success "Do"
    - Use `ValidateNumeric` before [`Val`](Val.md) or [`ToNumeric`](ToNumeric.md) when invalid input should be rejected cleanly.
    - Test example inputs against the current decimal and group separator settings in your system.
    - Use this function when hexadecimal text must not be accepted.

!!! failure "Don't"
    - Assume grouped numbers are always valid. They only pass when the current numeric settings allow group separators.
    - Use `ValidateNumeric` when hexadecimal input should be allowed. Use [`IsNumeric`](IsNumeric.md) with `bAllowHex` instead.
    - Treat an error on [`NIL`](../literals/nil.md) input as a normal [`.F.`](../literals/false.md) result.

## Examples

### Validate a text field before conversion

Check a user-entered value before converting it with [`Val`](Val.md). The failure branch displays a prompt; the success branch displays the converted numeric value.

```ssl
:PROCEDURE ValidateNumericInput;
    :DECLARE sUserInput, bIsValid, nValue;

    sUserInput := "42.5";
    bIsValid := ValidateNumeric(sUserInput);

    :IF !bIsValid;
        UsrMes("Enter a valid number.");
        :RETURN .F.;
    :ENDIF;

    nValue := Val(sUserInput);
    UsrMes("Accepted value: " + LimsString(nValue));

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateNumericInput");
```

[`UsrMes`](UsrMes.md) displays:

```text
Accepted value: 42.5
```

### Build a candidate string with the current separators

Compose a number string from the active decimal and group separators and validate it. The output depends on the runtime separator settings.

```ssl
:PROCEDURE ValidateUsingCurrentSeparators;
	:DECLARE sDecimalSep, sGroupSep, sCandidate, bIsValid;

	sDecimalSep := GetDecimalSeparator();
	sGroupSep := GetGroupSeparator();
	sCandidate := "1" + sGroupSep + "234" + sDecimalSep + "56";
	bIsValid := ValidateNumeric(sCandidate);

	UsrMes("Candidate: " + sCandidate);
	/* Displays the constructed candidate string;
	UsrMes("Valid under current settings: " + LimsString(bIsValid));
	/* Displays whether the candidate is valid;

	:RETURN bIsValid;
:ENDPROC;

/* Usage;
DoProc("ValidateUsingCurrentSeparators");
```

### Filter imported values and collect invalid rows

Validate a batch of imported string values and accumulate the ones that fail into a separate array for review. The expected output uses the sample data above where `"INVALID"` is the only non-numeric value.

```ssl
:PROCEDURE ReviewImportedValues;
	:DECLARE aSampleRows, aValidValues, aInvalidRows;
	:DECLARE sValue, nIndex;

	aSampleRows := {"100.50", "202.75", "INVALID", "45.00"};
	aValidValues := {};
	aInvalidRows := {};

	:FOR nIndex := 1 :TO ALen(aSampleRows);
		sValue := aSampleRows[nIndex];

		:IF ValidateNumeric(sValue);
			AAdd(aValidValues, sValue);
		:ELSE;
			AAdd(aInvalidRows, {nIndex, sValue});
		:ENDIF;
	:NEXT;

	UsrMes("Valid values: " + LimsString(ALen(aValidValues)));
	UsrMes("Invalid rows: " + LimsString(ALen(aInvalidRows)));

	:RETURN ALen(aInvalidRows) == 0;
:ENDPROC;

/* Usage;
DoProc("ReviewImportedValues");
```

[`UsrMes`](UsrMes.md) displays:

```text
Valid values: 3
Invalid rows: 1
```

## Related

- [`IsNumeric`](IsNumeric.md)
- [`ToNumeric`](ToNumeric.md)
- [`Val`](Val.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
