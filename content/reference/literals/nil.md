---
title: "nil"
summary: "NIL is the SSL literal for an explicit absent value. It is case-insensitive, so NIL, nil, and Nil are all valid spellings."
id: ssl.literal.nil
element_type: literal
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# nil

## What it does

`NIL` is the SSL literal for an explicit absent value. It is case-insensitive, so `NIL`, `nil`, and `Nil` are all valid spellings.

`NIL` only compares equal to `NIL` itself. Both [`=`](../operators/equals.md) and [`==`](../operators/strict-equals.md) return [`.T.`](true.md) for `NIL` compared with `NIL`, and [`.F.`](false.md) for `NIL` compared with non-`NIL` values such as `""`. Use [`Empty`](../functions/Empty.md)`()` when you want to treat `NIL` and the empty string the same way.

When a variable is declared with [`:DECLARE`](../keywords/DECLARE.md), it starts as an empty string, not `NIL`. An explicit `NIL` check therefore stays false until you actually assign `NIL`.

`NIL` is distinct from [`.F.`](false.md). Use `NIL` for absence and [`.F.`](false.md) for boolean false.

## Syntax

`NIL`

- **Type:** NIL
- **Case:** case-insensitive

## Comparison behavior

| Expression | Result | Notes |
| --- | --- | --- |
| `NIL = NIL` | [`.T.`](true.md) | NIL equals itself |
| `NIL == NIL` | [`.T.`](true.md) | Exact equality is also true |
| `NIL = ""` | [`.F.`](false.md) | NIL is not an empty string |
| `NIL == ""` | [`.F.`](false.md) | Same - use [`Empty`](../functions/Empty.md)`()` to treat both as "no value" |
| [`Empty`](../functions/Empty.md)`(NIL)` | [`.T.`](true.md) | NIL is considered empty |
| [`LimsTypeEx`](../functions/LimsTypeEx.md)`(NIL)` | `"NIL"` | Runtime type name for NIL values |

## Notes for daily SSL work

!!! success "Do"
    - Use `NIL` to intentionally indicate "no value" rather than an empty string.
    - Compare explicitly to `NIL` when an API uses `NIL` as a sentinel result.
    - Use [`Empty`](../functions/Empty.md)`()` when you want to treat both `NIL` and `""` as "no value."

!!! failure "Don't"
    - Assume a freshly declared variable is `NIL`. Variables from [`:DECLARE`](../keywords/DECLARE.md) start as empty string, not `NIL`.
    - Use `= ""` to check for absence when `NIL` is also possible. `NIL = ""` is [`.F.`](false.md); use [`Empty`](../functions/Empty.md)`()` instead.
    - Use `NIL` when you really mean boolean false. `NIL` and [`.F.`](false.md) are different values.

## Errors and edge cases

- [`LimsString`](../functions/LimsString.md)`(NIL)` returns the string `"NIL"`.

## Examples

### Distinguishing NIL from empty string

Declares `sValue`, which starts as an empty string (not `NIL`), then assigns `NIL` explicitly. The first pair of checks shows the initial empty-string state; the second pair shows the state after the `NIL` assignment.

```ssl
:PROCEDURE DemonstrateNilVsEmpty;
    :DECLARE sValue;

    /* :DECLARE initializes to empty string, not NIL;
    UsrMes("After DECLARE — is empty: " + LimsString(Empty(sValue)));
    UsrMes("After DECLARE — is NIL: " + LimsString(sValue = NIL));

    sValue := NIL;

    UsrMes("After NIL assign — is empty: " + LimsString(Empty(sValue)));
    UsrMes("After NIL assign — is NIL: " + LimsString(sValue = NIL));

    :RETURN sValue;
:ENDPROC;

/* Usage;
DoProc("DemonstrateNilVsEmpty");
```

### Using NIL as a lookup sentinel

Passes `NIL` as the default to [`LSearch`](../functions/LSearch.md) so the procedure can distinguish "no row found" from an empty result. With `"S-999"` absent from the database, `FindSample` returns `NIL`, and both the direct comparison and [`Empty`](../functions/Empty.md)`()` check confirm the absence.

```ssl
:PROCEDURE FindSample;
    :PARAMETERS sSampleID;
    :DECLARE sName;

    sName := LSearch("
        SELECT sample_name FROM sample WHERE sample_id = ?
    ", NIL,, {sSampleID});

    :RETURN sName;
:ENDPROC;

:PROCEDURE CheckSampleLookup;
    :DECLARE sResult;

    sResult := DoProc("FindSample", {"S-999"});

    :IF sResult == NIL;
        UsrMes("Sample not found");
    :ELSE;
        UsrMes("Found: " + sResult);
    :ENDIF;

    :IF Empty(sResult);
        UsrMes("No result (from Empty check)");
    :ENDIF;

    :RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("CheckSampleLookup");
```

## Related elements

- [`false`](false.md)
- [`true`](true.md)
