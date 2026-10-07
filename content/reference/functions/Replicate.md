---
title: "Replicate"
summary: "Creates a string by repeating the source string a specified number of times."
id: ssl.function.replicate
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# Replicate

Creates a string by repeating the source string a specified number of times.

`Replicate` returns a new string made up of `sSource` repeated `nCount` times. When `sSource` is empty the result is always `""` regardless of `nCount`. When `nCount` is zero the result is also `""`. A negative `nCount` or a [`NIL`](../literals/nil.md) argument raises an error.

## When to use

- When you need to build a separator, padding, or ruler string of a fixed width.
- When you need to generate a repeated token pattern such as `?,?,?` for SQL placeholders.
- When you want to repeat an entire substring pattern rather than extract or pad individual characters.

## Syntax

```ssl
Replicate(sSource, nCount)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | Source string to be repeated |
| `nCount` | [number](../types/number.md) | yes | — | Number of times to repeat the source string |

## Returns

**[string](../types/string.md)** — String consisting of the source string repeated `nCount` times

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument source cannot be null. Replicate().` |
| `nCount` is [`NIL`](../literals/nil.md). | `Argument count cannot be null. Replicate().` |
| `nCount` is negative. | `Argument count cannot be less then zero. Replicate().` |

## Best practices

!!! success "Do"
    - Always validate that `nCount` is zero or greater before calling the function.
    - Handle cases where the source string may be empty to avoid unnecessary processing.
    - Use this function to generate consistent string patterns, such as repeated separators.
    - Build padding by repeating one character, for example `sValue + Replicate(" ", 10 - Len(sValue))`, guarding against a negative count.

!!! failure "Don't"
    - Assume the function handles negative counts gracefully. Negative counts raise an error that halts execution if unhandled.
    - Expect a non-empty result when `sSource` is empty, even with a positive count. The function always returns `""` when `sSource` is empty.

## Examples

### Repeat a pattern a fixed number of times

Repeat a short pattern and show the result with its length.

```ssl
:PROCEDURE BuildRepeatPattern;
    :DECLARE sPattern, nCount, sResult;

    sPattern := "-*-";
    nCount := 5;
    sResult := Replicate(sPattern, nCount);

    UsrMes("Pattern: " + sResult);
    /* Logs: Pattern: -*--*--*--*--*-;
    UsrMes("Length: " + LimsString(Len(sResult)));
    /* Logs: Length: 15;
:ENDPROC;

/* Usage;
DoProc("BuildRepeatPattern");
```

### Build a separator line

Build a separator line and surround a title with it.

```ssl
:PROCEDURE DisplaySeparator;
    :DECLARE sSeparator, sTitle, sOutput, nWidth;

    nWidth := 40;
    sTitle := "Analysis Results";
    sSeparator := Replicate("-", nWidth);
    sOutput := sSeparator + Chr(10) +
        sTitle + " | Generated: " + DToC(Today()) + Chr(10) +
        sSeparator;

    UsrMes(sOutput);
:ENDPROC;

/* Usage;
DoProc("DisplaySeparator");
```

[`UsrMes`](UsrMes.md) logs:

```text
----------------------------------------
Analysis Results | Generated: <date>
----------------------------------------
```

`<date>` is the current date, so it varies from day to day. The date text follows the current session date format, set with [`DateFormat`](DateFormat.md).

### Generate SQL `IN` clause placeholders

Use `Replicate` to build a comma-separated `?` list for a parameterized `IN` clause, then trim the trailing comma.

```ssl
:PROCEDURE BuildInPlaceholders;
    :PARAMETERS nCount;
    :DECLARE sTemp, sPlaceholders;

    :IF nCount <= 0;
        UsrMes("Count must be positive.");
        :RETURN "";
    :ENDIF;

    sTemp := Replicate("?,", nCount);
    sPlaceholders := Left(sTemp, Len(sTemp) - 1);

    UsrMes(sPlaceholders);

    :RETURN sPlaceholders;
:ENDPROC;

/* Usage;
DoProc("BuildInPlaceholders", {1});
DoProc("BuildInPlaceholders", {4});
```

For `nCount = 1`:

```text
?
```

For `nCount = 4`:

```text
?,?,?,?
```

## Related

- [`Left`](Left.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
