---
title: "Scient"
summary: "Converts a number to its scientific notation string representation."
id: ssl.function.scient
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Scient

Converts a number to its scientific notation string representation.

`Scient` formats a numeric value as a string containing a mantissa and exponent, such as `1.23E5`. Zero returns `0E-0`, and negative values keep a leading minus sign. The mantissa uses the current environment's configured decimal separator, so the returned text may not always use `.`.

## When to use

- When you need a scientific-notation string for display, export, or logging.
- When you want the built-in `Scient` formatting rather than choosing the number of decimal places yourself.
- When your code needs to handle zero and negative numeric values consistently.

## Syntax

```ssl
Scient(nValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nValue` | [number](../types/number.md) | yes | — | The numeric value to convert to scientific notation. |

## Returns

**[string](../types/string.md)** — The scientific-notation string for `nValue`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nValue` is [`NIL`](../literals/nil.md). | `Value cannot be null.` |

## Best practices

!!! success "Do"
    - Treat the result as formatted text, not as a numeric value for further math.
    - Use this function when the built-in `Scient` output is acceptable as-is.
    - Account for zero and negative inputs if those values matter to the output you show or export.

!!! failure "Don't"
    - Assume the return value can be used directly in numeric calculations without converting it back.
    - Assume the mantissa always uses `.` as the decimal separator.
    - Use `Scient` when you need caller-controlled precision. Use [`ToScientific`](ToScientific.md) for that case.

## Examples

### Format a measurement result

Display one measurement in scientific notation.

```ssl
:PROCEDURE DisplayMeasurementScientific;
    :DECLARE nMeasurement, sScientific;

    nMeasurement := 0.000000325;
    sScientific := Scient(nMeasurement);

    UsrMes("Measurement in scientific notation: " + sScientific);
:ENDPROC;

/* Usage;
DoProc("DisplayMeasurementScientific");
```

[`UsrMes`](UsrMes.md) displays:

```text
Measurement in scientific notation: 0.325E-6
```

### Format multiple values for export

Format several numeric values before building an export payload.

```ssl
:PROCEDURE ExportMeasurementsToFlatFile;
    :DECLARE aValues, sLineOut, sScientific, nValue, nIndex;

    aValues := {0.00004523, 1256000.0, 0.0034};
    sLineOut := "RESULT";

    :FOR nIndex := 1 :TO ALen(aValues);
        nValue := aValues[nIndex];
        sScientific := Scient(nValue);
        sLineOut := sLineOut + Chr(9) + sScientific;
    :NEXT;

    UsrMes("Export line: " + sLineOut);
:ENDPROC;

/* Usage;
DoProc("ExportMeasurementsToFlatFile");
```

[`UsrMes`](UsrMes.md) displays:

```text
Export line: RESULT<TAB>0.4523E-4<TAB>1.256E6<TAB>0.34E-2
```

### Include zero and negative values in a scientific export

Build a multi-line export string that includes positive, zero, and negative values.

```ssl
:PROCEDURE BuildScientificExport;
    :DECLARE aValues, nIndex, nValue, sScientific, sLine, sExport;

    aValues := {1256000.0, 0.0, (0 - 0.0034)};
    sExport := "";

    :FOR nIndex := 1 :TO ALen(aValues);
        nValue := aValues[nIndex];
        sScientific := Scient(nValue);
        sLine := LimsString(nIndex) + "," + LimsString(nValue) + "," + sScientific;

        :IF Empty(sExport);
            sExport := sLine;
        :ELSE;
            sExport := sExport + Chr(13) + Chr(10) + sLine;
        :ENDIF;
    :NEXT;

    UsrMes(sExport);
:ENDPROC;

/* Usage;
DoProc("BuildScientificExport");
```

[`UsrMes`](UsrMes.md) displays:

```text
1,1256000,1.256E6
2,0,0E-0
3,-0.0034,-0.34E-2
```

## Related

- [`ToScientific`](ToScientific.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
