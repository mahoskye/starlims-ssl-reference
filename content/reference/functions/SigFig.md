---
title: "SigFig"
summary: "Returns a string produced by applying a named rounding standard to a numeric value."
id: ssl.function.sigfig
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SigFig

Returns a string produced by applying a named rounding standard to a numeric value.

`SigFig(sStandard, nDigits, nValue)` returns a string result and requires all three arguments. `SigFig` behaves the same as [`StdRound`](StdRound.md): it accepts the same arguments, raises the same null-argument errors, and recognizes the same named standards (`FDA`, `EPA`, and `ISO`). Use it when existing SSL code or published interfaces expect `SigFig`, and treat the result as formatted text rather than as a numeric value.

## When to use

- When existing STARLIMS code or documentation already uses `SigFig` and you need the matching string result.
- When a workflow requires a named rounding standard such as `FDA`, `EPA`, or `ISO`.
- When the rounded value will be displayed, exported, or stored as text rather than used directly in more arithmetic.

## Syntax

```ssl
SigFig(sStandard, nDigits, nValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sStandard` | [string](../types/string.md) | yes | — | Rounding standard name. The implementation has explicit handling for `FDA`, `EPA`, and `ISO`. |
| `nDigits` | [number](../types/number.md) | yes | — | Digit count passed to the rounding routine. |
| `nValue` | [number](../types/number.md) | yes | — | Numeric value to round and format. |

## Returns

**[string](../types/string.md)** — The formatted string returned by the selected rounding routine.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sStandard` is [`NIL`](../literals/nil.md). | `Argument sStandard cannot be null.` |
| `nDigits` is [`NIL`](../literals/nil.md). | `Argument nDigits cannot be null.` |
| `nValue` is [`NIL`](../literals/nil.md). | `Argument nValue cannot be null.` |

## Best practices

!!! success "Do"
    - Pass an explicit supported standard such as `FDA`, `EPA`, or `ISO`.
    - Treat the return value as a string, especially before concatenating, exporting, or storing it.
    - Compare the result with [`StdRound`](StdRound.md) when reviewing legacy code, because both functions produce the same output.
    - Trim the result when needed before fixed-width export handling, especially for `ISO` output.

!!! failure "Don't"
    - Assume `SigFig` returns a numeric value. It returns formatted text, which can affect later calculations.
    - Pass [`NIL`](../literals/nil.md) for any argument. The function raises an error instead of supplying defaults.
    - Rely on undocumented standard names. The verified implementation only branches on `FDA`, `EPA`, and `ISO`.
    - Use `SigFig` as a drop-in replacement for every ordinary rounding need when plain numeric rounding is sufficient.

## Caveats

- The result string replaces `.` with the system decimal separator before returning.
- Negative values keep the minus sign in the returned string.
- For `ISO`, the returned string can be left-padded to a total length of 15 characters.

## Examples

### Format one reported value

Use `SigFig` to produce the string that will be shown in a report line.

```ssl
:PROCEDURE FormatReportedValue;
    :DECLARE sStandard, sRounded;
    :DECLARE nDigits, nValue;

    sStandard := "FDA";
    nDigits := 2;
    nValue := 12.3456;

    sRounded := SigFig(sStandard, nDigits, nValue);

    UsrMes("Reported value: " + sRounded);

    :RETURN sRounded;
:ENDPROC;

/* Usage;
DoProc("FormatReportedValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
Reported value: <rounded value>
```

### Compare multiple standards for the same input

Loop through several requests so the same input pattern can be handled with different named standards.

```ssl
:PROCEDURE ReviewRoundedValues;
    :DECLARE aRequests, aRow;
    :DECLARE sStandard, sRounded, sLine;
    :DECLARE nDigits, nValue, nIndex;

    aRequests := {
        {"FDA", 2, 12.3456},
        {"EPA", 3, 0.012345},
        {"ISO", 2, 98.7654}
    };

    :FOR nIndex := 1 :TO ALen(aRequests);
        aRow := aRequests[nIndex];
        sStandard := aRow[1];
        nDigits := aRow[2];
        nValue := aRow[3];

        sRounded := SigFig(sStandard, nDigits, nValue);
        sLine := sStandard + ": " + sRounded;

        UsrMes(sLine);  /* Displays: <standard>: <rounded value>;
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("ReviewRoundedValues");
```

### Normalize ISO output before export

Trim the display value for an export row while still keeping the original rounded string available when needed.

```ssl
:PROCEDURE BuildExportValue;
    :PARAMETERS sStandard, nDigits, nValue;
    :DECLARE sRounded, sDisplay, oErr;

    :TRY;
        sRounded := SigFig(sStandard, nDigits, nValue);
        sDisplay := sRounded;

        :IF sStandard == "ISO";
            sDisplay := AllTrim(sRounded);
        :ENDIF;

        :RETURN "VALUE=" + sDisplay + "|RAW=" + sRounded;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("BuildExportValue failed: " + oErr:Description);

        :RETURN "";
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("BuildExportValue", {"ISO", 2, 98.7654});
```

## Related

- [`Round`](Round.md)
- [`StdRound`](StdRound.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
