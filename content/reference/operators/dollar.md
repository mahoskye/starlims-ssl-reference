---
title: "dollar"
summary: "Tests whether the left string is found within the right operand as a substring."
id: ssl.operator.dollar
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# dollar

## What it does

Tests whether the left string is found within the right operand as a substring.

The dollar (`$`) operator performs substring containment for strings. The left
operand is the substring to look for, and the right operand is the string to search in. When both operands are strings, the result is boolean: [`.T.`](../literals/true.md) when the left string appears anywhere within the right string, otherwise [`.F.`](../literals/false.md). Matching is case-sensitive.

The operator is strict about operand types. If the left operand is not a string, the expression raises a runtime error. If the right operand is not a string, the expression also raises a runtime error. Use explicit conversion such as [`LimsString`](../functions/LimsString.md)`(...)` when you intentionally want string containment against a non-string value.

`$` is commonly contrasted with [`equals`](equals.md). [`=`](equals.md) performs prefix matching for strings, while `$` checks for a substring anywhere in the right operand. Operand order matters: `"Sample" $ "Lab Sample"` is [`.T.`](../literals/true.md), but `"Lab Sample" $ "Sample"` is [`.F.`](../literals/false.md).

## When to use it

- When checking whether a string contains a specific substring.
- When filtering or matching text values without resorting to a full pattern match or function call.
- When distinguishing from prefix-matching ([`=`](equals.md)) is important.

## Syntax

```ssl
bResult := needle $ haystack;
```

## Type behavior

| Left | Right | Result | Behavior |
| --- | --- | --- | --- |
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) if the left string is found anywhere within the right string; otherwise [`.F.`](../literals/false.md). |
| [string](../types/string.md) | non-string | error | Raises a runtime error because `$` does not implicitly convert the right operand to string. |
| non-string | any | error | Raises a runtime error because `$` is only implemented for string left operands. |

## Precedence

- **Precedence:** Comparison (same group as equality-style comparisons)
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Make sure both operands are strings before using `$`.
    - Double-check the order — the substring you want to find goes on the **left**, the string to search goes on the **right**.
    - Convert non-string values explicitly with [`LimsString`](../functions/LimsString.md)`(...)` before using `$`.
    - Wrap `$` in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when operand types cannot be guaranteed.

!!! failure "Don't"
    - Assume `$` will silently fall back to [`.F.`](../literals/false.md) for numbers, arrays, or objects. Non-string operands raise runtime errors.
    - Reverse operand order out of habit from other languages. The substring is always on the left.
    - Rely on `$` to convert the right operand for you. Convert explicitly first if that is the behavior you need.

## Errors and edge cases

- An empty string as the left operand (`"" $ sValue`) always returns [`.T.`](../literals/true.md) since every string contains the empty string.

## Examples

### Basic substring containment

Searches for `"quick"` inside `sText`. The substring is present, so `bFound` is [`.T.`](../literals/true.md) and the found branch runs.

```ssl
:PROCEDURE CheckSubstring;
    :DECLARE sText, sSearch, bFound;

    sText := "The quick brown fox";
    sSearch := "quick";

    bFound := sSearch $ sText;

    :IF bFound;
        UsrMes("Substring found");
    :ELSE;
        UsrMes("Substring not found");
    :ENDIF;

    :RETURN bFound;
:ENDPROC;

/* Usage;
DoProc("CheckSubstring");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Substring found
```

### Operand order and case sensitivity

Demonstrates that `$` requires the search term on the left and that matching is case-sensitive. `"sample"` (lowercase) does not match even though `"Sample"` does.

```ssl
:PROCEDURE DollarOperandOrder;
    :DECLARE sHaystack, sNeedle, bFound;

    sHaystack := "Laboratory Sample Analysis";
    sNeedle := "Sample";

    bFound := sNeedle $ sHaystack;
    UsrMes("Needle in haystack: " + LimsString(bFound));

    bFound := sHaystack $ sNeedle;
    UsrMes("Haystack in needle: " + LimsString(bFound));

    bFound := "sample" $ sHaystack;
    UsrMes("Lowercase search: " + LimsString(bFound));

    bFound := "Sample" $ sHaystack;
    UsrMes("Matching case search: " + LimsString(bFound));

    :RETURN bFound;
:ENDPROC;

/* Usage;
DoProc("DollarOperandOrder");
```

`UsrMes` displays:

```text
Needle in haystack: .T.
Haystack in needle: .F.
Lowercase search: .F.
Matching case search: .T.
```

### Converting a number before searching

Converts `nBatchNo` to a string with [`LimsString`](../functions/LimsString.md) before using `$`, then catches the error produced when an unconverted object is used as the right operand.

```ssl
:PROCEDURE SafeDollarComparison;
    :DECLARE sText, nBatchNo, vValue, bFound, oErr;

    sText := "Batch 12345 released";
    nBatchNo := 12345;

    bFound := LimsString(nBatchNo) $ sText;
    UsrMes("Explicit conversion result: " + LimsString(bFound));

    vValue := CreateLocal();

    :TRY;
        bFound := "Batch" $ vValue;
        UsrMes("Unexpected result: " + LimsString(bFound));
    :CATCH;
        oErr := GetLastSSLError();
        /* Displays on failure with runtime error details;
        UsrMes("Comparison failed: " + oErr:Description);
    :ENDTRY;

    :RETURN bFound;
:ENDPROC;

/* Usage;
DoProc("SafeDollarComparison");
```

`UsrMes` first displays:

```text
Explicit conversion result: .T.
```

## Related elements

- [`equals`](equals.md)
- [`strict-equals`](strict-equals.md)
