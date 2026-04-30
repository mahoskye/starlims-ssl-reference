---
title: "At"
summary: "Finds the first occurrence of a substring in a string and returns its one-based position."
id: ssl.function.at
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# At

Finds the first occurrence of a substring in a string and returns its one-based position.

`At` searches `sSource` for the first occurrence of `sSubString`. It returns a one-based match position, or `0` when the substring is not present.

The match is case-sensitive. Use `At` when you need the first occurrence, [`LimsAt`](LimsAt.md) when you need to start searching from a later position, and [`Rat`](Rat.md) when you need the last occurrence.

## When to use

- When you need to check whether a delimiter or marker appears in a string.
- When you need the position of the first match so you can split or trim text.
- When you need a simple presence test and `0` is sufficient to mean not found.
- When you want the first occurrence specifically, not the last or a later occurrence.

## Syntax

```ssl
At(sSubString, sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSubString` | [string](../types/string.md) | yes | — | Substring to look for. |
| `sSource` | [string](../types/string.md) | yes | — | String to search. |

## Returns

**[number](../types/number.md)** — The one-based position of the first match, or `0` when no match is found.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSubString` is [`NIL`](../literals/nil.md). | `Argument sSubString cannot be null.` |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Check for `0` before using the result as a string position.
    - Normalize case with [`Upper`](Upper.md) or [`Lower`](Lower.md) first when you need case-insensitive matching.
    - Use [`LimsAt`](LimsAt.md) when you need to continue searching after an earlier match.
    - Use [`Rat`](Rat.md) when you need the last occurrence instead of the first.

!!! failure "Don't"
    - Assume the return value is zero-based. `At` returns `1` for a match at the first character.
    - Assume the search ignores case. `At` only matches text with the same casing.
    - Pass [`NIL`](../literals/nil.md) for either argument. Null inputs raise a runtime error.
    - Use `At` when you actually need a later or last occurrence. Use [`LimsAt`](LimsAt.md) or [`Rat`](Rat.md) for those cases.

## Caveats

- The result is one-based, so convert carefully when working with zero-based external systems.
- An empty `sSubString` returns `1`, even when `sSource` is empty.

## Examples

### Find a delimiter in a value

Finds the first comma in a CSV-style value so later code can split the string at that position.

```ssl
:DECLARE sCsv, nCommaPos;

sCsv := "field1,field2";
nCommaPos := At(",", sCsv);

UsrMes("First comma position: " + LimsString(nCommaPos));
```

[`UsrMes`](UsrMes.md) displays:

```text
First comma position: 7
```

### Check for a tag without case sensitivity

Converts the source string to uppercase first, then searches for the uppercase tag so the match is case-insensitive.

```ssl
:PROCEDURE CheckUrgentTag;
    :DECLARE sInput, sUpperInput, nTagPos;

    sInput := "Please handle as UrGenT";
    sUpperInput := Upper(sInput);
    nTagPos := At("URGENT", sUpperInput);

    :IF nTagPos > 0;
        UsrMes("URGENT found at position " + LimsString(nTagPos));
    :ELSE;
        UsrMes("URGENT tag not found");
    :ENDIF;
:ENDPROC;

DoProc("CheckUrgentTag");
```

[`UsrMes`](UsrMes.md) displays:

```text
URGENT found at position 18
```

### Find repeated delimiters in sequence

Uses `At` for the first separator and [`LimsAt`](LimsAt.md) for the second and third, passing each result as the starting position for the next search.

```ssl
:PROCEDURE LocatePathSeparators;
    :DECLARE sPath, nFirstSlash, nSecondSlash, nThirdSlash;

    sPath := "Orders/2026/Incoming/Batch01";

    nFirstSlash := At("/", sPath);
    nSecondSlash := LimsAt("/", sPath, nFirstSlash + 1);
    nThirdSlash := LimsAt("/", sPath, nSecondSlash + 1);

    UsrMes("First slash: " + LimsString(nFirstSlash));
    /* Displays: First slash: 7;
    UsrMes("Second slash: " + LimsString(nSecondSlash));
    /* Displays: Second slash: 12;
    UsrMes("Third slash: " + LimsString(nThirdSlash));
    /* Displays: Third slash: 21;
:ENDPROC;

DoProc("LocatePathSeparators");
```

## Related

- [`LimsAt`](LimsAt.md)
- [`Rat`](Rat.md)
- [`Replace`](Replace.md)
- [`StrSrch`](StrSrch.md)
- [`StrTran`](StrTran.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
