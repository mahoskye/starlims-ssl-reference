---
title: "ToScientific"
summary: "Converts a numeric value to a scientific-notation string."
id: ssl.function.toscientific
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ToScientific

Converts a numeric value to a scientific-notation string.

`ToScientific` formats a numeric value using scientific notation and returns the formatted text. The optional `nDecimalPlaces` argument controls how many digits appear after the decimal point. If `nDecimalPlaces` is omitted, the function uses `2`.

## When to use

- When you need a scientific-notation string for display, export, or logging.
- When the caller must control the number of digits after the decimal point.
- When [`Scient`](Scient.md) is too fixed and you need explicit precision in the output.

## Syntax

```ssl
ToScientific(nNumber, [nDecimalPlaces])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nNumber` | [number](../types/number.md) | yes | — | Numeric value to format |
| `nDecimalPlaces` | [number](../types/number.md) | no | `2` | Integer number of digits after the decimal point |

## Returns

**[string](../types/string.md)** — The scientific-notation string for `nNumber`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nNumber` is not numeric. | `Argument 'nNumber' must be a numeric.` |
| `nDecimalPlaces` is not an integer. | `Argument 'nDecimalPlaces' must be an integer.` |

## Best practices

!!! success "Do"
    - Pass an explicit `nDecimalPlaces` value when downstream formatting must be consistent.
    - Use this function when you need caller-controlled scientific formatting.
    - Keep the result as display or export text rather than using it for further math.

!!! failure "Don't"
    - Pass a string, object, or other non-numeric value as `nNumber`.
    - Pass a fractional precision such as `2.5` for `nDecimalPlaces`.
    - Use this function when plain numeric formatting is sufficient and scientific notation is not wanted.

## Examples

### Format one measurement with the default precision

Convert a numeric result to scientific notation without passing the optional precision argument. The default is two decimal places.

```ssl
:PROCEDURE FormatMeasuredValue;
    :DECLARE nMeasurement, sScientific;

    nMeasurement := 0.000315;
    sScientific := ToScientific(nMeasurement);

    UsrMes("Concentration: " + sScientific + " mol/L");
:ENDPROC;

/* Usage;
DoProc("FormatMeasuredValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
Concentration: 3.15E-004 mol/L
```

### Apply a fixed precision to several values

Format several values with the same precision and concatenate them into an export line separated by tab characters.

```ssl
:PROCEDURE BuildScientificExportLine;
    :DECLARE aRawValues, sOutput, sScientific, nValue, nDecimal, nIndex;

    aRawValues := {0.0000456, 0.0001234, 5678900.0};
    nDecimal := 3;
    sOutput := "RESULTS";

    :FOR nIndex := 1 :TO ALen(aRawValues);
        nValue := aRawValues[nIndex];
        sScientific := ToScientific(nValue, nDecimal);

        sOutput := sOutput + Chr(9) + sScientific;
    :NEXT;

    UsrMes("Export line: " + sOutput);
:ENDPROC;

/* Usage;
DoProc("BuildScientificExportLine");
```

[`UsrMes`](UsrMes.md) displays:

```text
Export line: RESULTS<TAB>4.560E-005<TAB>1.234E-004<TAB>5.679E+006
```

### Validate a user-supplied precision before formatting

Check that the precision input is numeric and an integer before passing it to `ToScientific`. This guards against type and format errors before the call rather than catching them after.

```ssl
:PROCEDURE FormatWithRequestedPrecision;
    :PARAMETERS sPrecision;
    :DEFAULT sPrecision, "4";
    :DECLARE nMeasurement, nPrecision, sScientific;

    nMeasurement := 0.00000152;

    :IF !IsNumeric(sPrecision);
        UsrMes("Precision must be numeric.");

        :RETURN "";
    :ENDIF;

    nPrecision := ToNumeric(sPrecision);

    :IF Integer(nPrecision) != nPrecision;
        UsrMes("Precision must be an integer.");

        :RETURN "";
    :ENDIF;

    sScientific := ToScientific(nMeasurement, nPrecision);

    UsrMes("Formatted value: " + sScientific);

    :RETURN sScientific;
:ENDPROC;

/* Usage;
DoProc("FormatWithRequestedPrecision");
```

[`UsrMes`](UsrMes.md) displays:

```text
Formatted value: 1.5200E-006
```

## Related

- [`Scient`](Scient.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
