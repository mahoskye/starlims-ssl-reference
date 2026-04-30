---
title: "Round"
summary: "Rounds a numeric value to a specific number of decimal places using a configurable midpoint handling strategy."
id: ssl.function.round
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Round

Rounds a numeric value to a specific number of decimal places using a configurable midpoint handling strategy.

`Round` rounds `nValue` to `nDigits` decimal places. When `sMidPointRounding` is `"AwayFromZero"` (case-insensitive), halfway values round away from zero; any other value or omitting the argument selects banker's rounding (`"ToEven"`). If `nValue` is already an integer, it is returned unchanged.

## When to use

- When calculations require rounded results for consistent reporting, pricing, or presentation.
- When business rules dictate rounding midpoint numbers in a specific way (e.g., always away from zero, or using banker's rounding).
- When validating or formatting numeric input to match regulatory, user, or data export requirements.
- When precise control over decimal places is necessary in scientific, statistical, or financial workflows.

## Syntax

```ssl
Round(nValue, nDigits, [sMidPointRounding])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nValue` | [number](../types/number.md) | yes | — | The number to be rounded. |
| `nDigits` | [number](../types/number.md) | yes | — | Number of decimal places to round to. |
| `sMidPointRounding` | [string](../types/string.md) | no | `"ToEven"` | Rounding midpoint mode. Pass `"AwayFromZero"` (case-insensitive) to round halfway values away from zero; any other value or omitting the argument entirely selects banker's rounding. |

## Returns

**[number](../types/number.md)** — The rounded number.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nValue` is not a number. | `First parameter must be a number` |
| `nDigits` is not a number. | `Second parameter must be a number` |

## Best practices

!!! success "Do"
    - Pass `"AwayFromZero"` explicitly when you need that rounding mode, and rely on the default when you want banker's rounding.
    - Check that both `nValue` and `nDigits` are numbers before calling.
    - Use a minimal, necessary number of decimal places for your domain.

!!! failure "Don't"
    - Assume `sMidPointRounding` must always be supplied — omitting it selects the `"ToEven"` default.
    - Assume the function will coerce strings or [`NIL`](../literals/nil.md) to numbers. Non-numeric input for `nValue` or `nDigits` raises an error.
    - Request more digits than needed; excessive precision may reduce clarity or introduce bias.

## Caveats

- Floating-point rounding may not always match visual or manual expectations due to binary representation. For example, `Round(2.675, 2)` may return `2.67`, not `2.68`.
- Very large values for `nDigits` are not supported; stay within standard double-precision range.

## Examples

### Round a laboratory measurement for a report

Format a measurement value for display in a report, ensuring only two decimals are shown.

```ssl
:PROCEDURE FormatMeasurementForReport;
    :DECLARE nRawReading, nRounded, sReportLine;
    nRawReading := 12.3456789;
    nRounded := Round(nRawReading, 2, "ToEven");
    sReportLine := "Result: " + LimsString(nRounded);
    UsrMes(sReportLine);
:ENDPROC;

/* Usage;
DoProc("FormatMeasurementForReport");
```

[`UsrMes`](UsrMes.md) displays:

```
Result: 12.35
```

### Round tax amounts away from zero for compliance

Round monetary amounts for tax calculations, requiring rounding away from zero on midpoint values.

```ssl
:PROCEDURE CalculateTaxAmount;
    :DECLARE nUnitPrice, nQuantity, nSubtotal, nTaxRate, nTaxAmount;
    :DECLARE nRoundedTax, nTotal, sMessage;

    nUnitPrice := 29.99;
    nQuantity := 7;
    nTaxRate := 0.0825;

    nSubtotal := nUnitPrice * nQuantity;
    nTaxAmount := nSubtotal * nTaxRate;

    nRoundedTax := Round(nTaxAmount, 2, "AwayFromZero");
    nTotal := nSubtotal + nRoundedTax;

    sMessage := "Subtotal: " + LimsString(nSubtotal) + ", Tax: " + LimsString(nRoundedTax);
    sMessage := sMessage + ", Total: " + LimsString(nTotal);
    UsrMes(sMessage);

    :RETURN nTotal;
:ENDPROC;

/* Usage;
DoProc("CalculateTaxAmount");
```

[`UsrMes`](UsrMes.md) displays:

```
Subtotal: 209.93, Tax: 17.32, Total: 227.25
```

### Avoid cumulative bias when aggregating a large dataset

Aggregate thousands of floating-point results where unbiased rounding is critical to avoid drift over time.

```ssl
:PROCEDURE DemoUnbiasedRounding;
    :DECLARE nRawSum, nUnbiasedSum, nBiasedSum, nUnbiasedDrift, nBiasedDrift;
    :DECLARE nValue, nIndex, nCount, nRunningUnbiased, nRunningBiased;
    :DECLARE sResult;

    nRawSum := 0;
    nRunningUnbiased := 0;
    nRunningBiased := 0;
    nCount := 2000;

    :FOR nIndex := 1 :TO nCount;
        nValue := 0.00125 + (nIndex * 0.00003);
        nRawSum := nRawSum + nValue;
        nRunningUnbiased := nRunningUnbiased + Round(nValue, 4, "ToEven");
        nRunningBiased := nRunningBiased + Round(nValue, 4, "AwayFromZero");
    :NEXT;

    nUnbiasedSum := Round(nRunningUnbiased, 4, "ToEven");
    nBiasedSum := Round(nRunningBiased, 4, "ToEven");
    nUnbiasedDrift := Abs(nRawSum - nUnbiasedSum);
    nBiasedDrift := Abs(nRawSum - nBiasedSum);

    sResult := "Unbiased aggregation drift: " + LimsString(nUnbiasedDrift);
    /* Displays an unbiased drift value;
    UsrMes(sResult);

    sResult := "Biased aggregation drift: " + LimsString(nBiasedDrift);
    /* Displays a larger drift value;
    UsrMes(sResult);

    :RETURN nUnbiasedSum;
:ENDPROC;

/* Usage;
DoProc("DemoUnbiasedRounding");
```

## Related

- [`RoundPoint5`](RoundPoint5.md)
- [`SigFig`](SigFig.md)
- [`StdRound`](StdRound.md)
- [`number`](../types/number.md)
