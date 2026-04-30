---
title: "StrSrch"
summary: "Finds a substring by occurrence number or from a specific 1-based starting position."
id: ssl.function.strsrch
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# StrSrch

Finds a substring by occurrence number or from a specific 1-based starting position.

`StrSrch()` searches `source` for `subStr` and returns a 1-based match position.
When `flag` is omitted or [`.F.`](../literals/false.md), `indexOrOccurence` means "which occurrence to return". When `flag` is [`.T.`](../literals/true.md), `indexOrOccurence` means "start searching at this 1-based position".

If `indexOrOccurence` is omitted, the function defaults to `1`. If `flag` is omitted, it defaults to [`.F.`](../literals/false.md). The function returns `0` when no match is found.

## When to use

- When you need the second, third, or later occurrence of a substring.
- When you need to continue searching from a known 1-based position.
- When [`At`](At.md) is too limited because it only returns the first occurrence.
- When parsing text in stages and you need a later exact substring match.

## Syntax

```ssl
StrSrch(subStr, source, [indexOrOccurence], [flag])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `subStr` | [string](../types/string.md) | yes | — | Substring to search for. |
| `source` | [string](../types/string.md) | yes | — | String to search. |
| `indexOrOccurence` | [number](../types/number.md) | no | `1` | Occurrence number when `flag` is [`.F.`](../literals/false.md), or 1-based starting position when `flag` is [`.T.`](../literals/true.md). |
| `flag` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Controls how `indexOrOccurence` is interpreted. |

## Returns

**[number](../types/number.md)** — The 1-based position of the matching substring, or `0` when no match is found.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `subStr` is [`NIL`](../literals/nil.md). | `Argument subStr cannot be null.` |
| `source` is [`NIL`](../literals/nil.md). | `Argument source cannot be null.` |
| `indexOrOccurence` is out of range for the selected mode. | `A negative [indexOrOccurence] value is not allowed.` |

## Best practices

!!! success "Do"
    - Use the default call form when you want the first occurrence.
    - Pass `2`, `3`, or higher with `flag` set to [`.F.`](../literals/false.md) when you need a later occurrence.
    - Pass a known position with `flag` set to [`.T.`](../literals/true.md) when continuing a staged parse.
    - Check for `0` before using the result as a string position.

!!! failure "Don't"
    - Assume the result is zero-based. A match at the first character returns `1`.
    - Assume `indexOrOccurence` always means the same thing. Its meaning changes when `flag` changes.
    - Pass [`NIL`](../literals/nil.md) for `subStr` or `source`. Null inputs raise a runtime error.
    - Use `StrSrch()` when [`At`](At.md) already covers your case. `StrSrch()` is most useful when you need a later occurrence or a controlled starting position.

## Caveats

- In start-position mode, passing `0` raises the same out-of-range error used for negative values.

## Examples

### Find the first occurrence of a delimiter

Use the default behavior to get the first exact substring match.

```ssl
:PROCEDURE FindFirstComma;
    :DECLARE sCsvLine, nCommaPos;

    sCsvLine := "Smith,John,1990-05-15,Active";
    nCommaPos := StrSrch(",", sCsvLine);

    UsrMes("First comma found at position " + LimsString(nCommaPos));
:ENDPROC;

/* Usage;
DoProc("FindFirstComma");
```

[`UsrMes`](UsrMes.md) displays:

```text
First comma found at position 6
```

### Find the second occurrence of a marker

Use occurrence mode explicitly when you need the Nth match rather than the first one.

```ssl
:PROCEDURE FindSecondMarker;
    :DECLARE sText, sMarker, nPos;

    sText := "Batch=Q1|Batch=Q2|Batch=Q3";
    sMarker := "Batch=";
    nPos := StrSrch(sMarker, sText, 2, .F.);

    :IF nPos == 0;
        UsrMes("Second marker not found");

        :RETURN 0;
    :ENDIF;

    UsrMes("Second marker starts at position " + LimsString(nPos));  /* Displays sample second marker position;

    :RETURN nPos;
:ENDPROC;

/* Usage;
DoProc("FindSecondMarker");
```

### Resume searching after an earlier match

Use start-position mode to continue searching after a known result without recounting occurrences.

```ssl
:PROCEDURE FindNextPipe;
    :DECLARE sHeader, nFirstPipe, nSecondPipe;

    sHeader := "STATUS=Logged|OWNER=JSMITH|BATCH=LAB-2026-0042";
    nFirstPipe := StrSrch("|", sHeader);

    :IF nFirstPipe == 0;
        :RETURN 0;
    :ENDIF;

    nSecondPipe := StrSrch("|", sHeader, nFirstPipe + 1, .T.);

    UsrMes("First pipe: " + LimsString(nFirstPipe));  /* Displays sample first pipe position;
    UsrMes("Second pipe: " + LimsString(nSecondPipe));  /* Displays sample second pipe position;

    :RETURN nSecondPipe;
:ENDPROC;

/* Usage;
DoProc("FindNextPipe");
```

## Related

- [`At`](At.md)
- [`LimsAt`](LimsAt.md)
- [`Rat`](Rat.md)
- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
