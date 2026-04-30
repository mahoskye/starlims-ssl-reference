---
title: "LimsAt"
summary: "Finds the first occurrence of a substring in a string at or after a 1-based starting position."
id: ssl.function.limsat
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsAt

Finds the first occurrence of a substring in a string at or after a 1-based starting position.

`LimsAt` returns the first matching position using SSL's 1-based indexing. When `nOffset` is omitted, the search starts at position 1. If no match is found at or after the starting position, the function returns `0`.

The function raises an error when `sSubString` or `sSource` is [`NIL`](../literals/nil.md). `nOffset` uses 1-based indexing, and values less than `1` start the search from the beginning of the string.

## When to use

- When you need the first match after a known 1-based position.
- When you need to begin searching from a later 1-based position.
- When parsing text in stages and continuing each search after an earlier match.

## Syntax

```ssl
LimsAt(sSubString, sSource, [nOffset])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSubString` | [string](../types/string.md) | yes | — | Substring to search for. |
| `sSource` | [string](../types/string.md) | yes | — | String to search. |
| `nOffset` | [number](../types/number.md) | no | `1` | 1-based starting position for the search. |

## Returns

**[number](../types/number.md)** — The 1-based position of the first match at or after `nOffset`, or `0` when no match is found.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSubString` is [`NIL`](../literals/nil.md). | `Argument sSubString cannot be null.` |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Test the result against `0` before using it as a position.
    - Pass `nPos + 1` when you want to continue searching after an earlier match.
    - Use `LimsAt` when you need the first match after a known position.
    - Validate inputs that may be [`NIL`](../literals/nil.md) before calling the function.

!!! failure "Don't"
    - Check for `-1` — `LimsAt` returns `0` when no match is found.
    - Pass a 0-based offset copied from another language without converting it.
    - Expect [`NIL`](../literals/nil.md) arguments to return `0` or [`NIL`](../literals/nil.md) — they raise an error.
    - Use `LimsAt` when you actually need the last occurrence or pattern-based search.

## Caveats

- The result is 1-based, so a return value of `1` is a valid match at the first character.

## Examples

### Locate a dash in a sample ID

Search `"ABC-12345"` for a dash. `LimsAt` returns `0` when nothing is found and a positive 1-based position otherwise — the dash in this input is at position 4.

```ssl
:PROCEDURE FindDashPosition;
    :DECLARE sSampleId, nDashPos;

    sSampleId := "ABC-12345";
    nDashPos := LimsAt("-", sSampleId);

    :IF nDashPos == 0;
        UsrMes("Dash not found");
        :RETURN 0;
    :ENDIF;

    UsrMes("Sample ID: " + sSampleId);
    UsrMes("Dash found at position: " + LimsString(nDashPos));

    :RETURN nDashPos;
:ENDPROC;

/* Usage;
DoProc("FindDashPosition");
```

`UsrMes` displays:

```text
Sample ID: ABC-12345
Dash found at position: 4
```

### Find the second occurrence of a separator

Use the first match's position as the offset for the second `LimsAt` call. In `"Orders/2026/Incoming/Batch01"`, the first [`/`](../operators/divide.md) is at position 7 and the second is at position 12.

```ssl
:PROCEDURE FindSecondSlash;
    :DECLARE sPath, nFirstSlash, nSecondSlash;

    sPath := "Orders/2026/Incoming/Batch01";
    nFirstSlash := LimsAt("/", sPath);

    :IF nFirstSlash == 0;
        :RETURN 0;
    :ENDIF;

    nSecondSlash := LimsAt("/", sPath, nFirstSlash + 1);

    UsrMes("First slash: " + LimsString(nFirstSlash));
    UsrMes("Second slash: " + LimsString(nSecondSlash));

    :RETURN nSecondSlash;
:ENDPROC;

/* Usage;
DoProc("FindSecondSlash");
```

`UsrMes` displays:

```text
First slash: 7
Second slash: 12
```

### Extract a field value after a known label

Locate the `OWNER=` label with `LimsAt`, use [`Len`](Len.md) to calculate the value start position, then find the closing [`|`](../operators/or.md) with a second `LimsAt` call before extracting the value with [`SubStr`](SubStr.md). The header `"STATUS=Logged|OWNER=JSMITH|BATCH=LAB-2026-0042"` yields `"JSMITH"`.

```ssl
:PROCEDURE ExtractOwnerValue;
    :DECLARE sHeader, sLabel, sOwner;
    :DECLARE nLabelPos, nValuePos, nNextPipe;

    sHeader := "STATUS=Logged|OWNER=JSMITH|BATCH=LAB-2026-0042";
    sLabel := "OWNER=";
    nLabelPos := LimsAt(sLabel, sHeader);

    :IF nLabelPos == 0;
        :RETURN "";
    :ENDIF;

    nValuePos := nLabelPos + Len(sLabel);
    nNextPipe := LimsAt("|", sHeader, nValuePos);

    :IF nNextPipe == 0;
        sOwner := SubStr(sHeader, nValuePos);
    :ELSE;
        sOwner := SubStr(sHeader, nValuePos, nNextPipe - nValuePos);
    :ENDIF;

    UsrMes("Owner: " + sOwner);

    :RETURN sOwner;
:ENDPROC;

/* Usage;
DoProc("ExtractOwnerValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
Owner: JSMITH
```

## Related

- [`At`](At.md)
- [`Rat`](Rat.md)
- [`StrSrch`](StrSrch.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
