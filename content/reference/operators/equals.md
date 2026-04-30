---
title: "equals"
summary: "Compares two values for equality, using prefix matching for strings, exact matching for numbers, booleans, and dates, and reference equality for arrays and objects."
id: ssl.operator.equals
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# equals

## What it does

Compares two values for equality, using prefix matching for strings, exact matching for numbers, booleans, and dates, and reference equality for arrays and objects.

The `=` operator is type-aware. For strings, it is a loose comparison: it returns [`.T.`](../literals/true.md) when the right operand is empty, when both strings are identical, or when the left string starts with the right string. For numbers, booleans, and dates, `=` performs exact equality. Arrays and object values compare by reference, not by content.

For strings, `=` is not exact-match equality. `"Logged" = "Log"` returns [`.T.`](../literals/true.md) because the left string starts with the right string. Use [`strict-equals`](strict-equals.md) when a string comparison must be exact.

Type-mismatch behavior depends on the left operand. A string on the left returns [`.F.`](../literals/false.md) when the right operand is not a string. Numeric, boolean, and date values on the left raise a runtime invalid-operand error when the right operand is an incompatible type.

`NIL = NIL` returns [`.T.`](../literals/true.md). [`NIL`](../literals/nil.md) compared with any non-[`NIL`](../literals/nil.md) value returns [`.F.`](../literals/false.md).

## When to use it

- When you intentionally want prefix matching for strings.
- When comparing numbers, booleans, or dates for exact equality.
- When checking reference equality for arrays and objects.
- When [`strict-equals`](strict-equals.md) is too strict for your use case.

## Syntax

```ssl
bEqual := vLeft = vRight;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the right string is empty, when both strings are equal, or when the left string starts with the right string. |
| [string](../types/string.md) | non-string | [boolean](../types/boolean.md) | Returns [`.F.`](../literals/false.md). |
| [number](../types/number.md) | [number](../types/number.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when both numeric values are exactly equal. |
| [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when both boolean values are the same. |
| [date](../types/date.md) | [date](../types/date.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when both dates are equal. |
| [array](../types/array.md) | [array](../types/array.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) only when both operands reference the same array instance. |
| [object](../types/object.md) | [object](../types/object.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) only when both operands reference the same object instance. |
| NIL | NIL | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md). |
| NIL | non-[`NIL`](../literals/nil.md) | [boolean](../types/boolean.md) | Returns [`.F.`](../literals/false.md). |
| code block | any | error | Raises a runtime error. |

## Precedence

- **Precedence:** Equality
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `=` for string prefix checks only when prefix matching is the intended behavior.
    - Check operand types before using `=` in dynamic code paths.
    - Use [`strict-equals`](strict-equals.md) when the comparison must reject prefixes.

!!! failure "Don't"
    - Use `=` for exact string equality. `=` treats an empty right operand as a match and accepts prefixes.
    - Assume `=` performs type coercion. Comparing numbers, dates, or booleans to incompatible types raises runtime errors.
    - Assume arrays or objects are compared by content. `=` only checks whether both operands reference the same instance.

## Errors and edge cases

- String comparison is case-sensitive and uses prefix semantics, not exact-match semantics.
- `"" = "abc"` is [`.F.`](../literals/false.md), but `"abc" = ""` is [`.T.`](../literals/true.md) because an empty right operand always matches.
- Left operand is a code block: raises `== : Cannot compare to a code block`.

## Examples

### Checking whether a status starts with a prefix

Compares `sStatus` against `"Log"` using prefix matching. Because `"Logged"` starts with `"Log"`, `bIsLogged` is [`.T.`](../literals/true.md) and the matching branch runs.

```ssl
:PROCEDURE CheckLoggedStatus;
    :DECLARE sStatus, bIsLogged, sMessage;

    sStatus := "Logged";
    bIsLogged := sStatus = "Log";

    :IF bIsLogged;
        sMessage := "Status starts with Log";
    :ELSE;
        sMessage := "Status does not start with Log";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bIsLogged;
:ENDPROC;

/* Usage;
DoProc("CheckLoggedStatus");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Status starts with Log
```

### Comparing numeric values for exact equality

Uses `=` for numeric equality. With both `nExpected` and `nActual` set to 3, the comparison is [`.T.`](../literals/true.md) and the matching branch runs.

```ssl
:PROCEDURE CheckReplicateCount;
    :DECLARE nExpected, nActual, bMatch, sMessage;

    nExpected := 3;
    nActual := 3;
    bMatch := nActual = nExpected;

    :IF bMatch;
        sMessage := "Replicate count matches";
    :ELSE;
        sMessage := "Replicate count differs";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bMatch;
:ENDPROC;

/* Usage;
DoProc("CheckReplicateCount");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Replicate count matches
```

### Guarding dynamic values before comparing

Checks runtime types before applying `=` to avoid invalid-operand errors. With `nLeftValue = 42` (number) and `sRightValue = "42"` (string), the types differ and the comparison is skipped.

```ssl
:PROCEDURE SafeLooseEquality;
    :DECLARE nLeftValue, sRightValue, sLeftType, sRightType, bMatch, sMessage;

    nLeftValue := 42;
    sRightValue := "42";
    sLeftType := LimsTypeEx(nLeftValue);
    sRightType := LimsTypeEx(sRightValue);
    bMatch := .F.;

    :IF sLeftType == "STRING" .AND. sRightType == "STRING";
        bMatch := nLeftValue = sRightValue;
        sMessage := "Loose string comparison completed";
    :ELSE;
        :IF sLeftType == "NUMERIC" .AND. sRightType == "NUMERIC";
            bMatch := nLeftValue = sRightValue;
            sMessage := "Numeric equality comparison completed";
        :ELSE;
            sMessage := "Skipped: operands have different types";
        :ENDIF;
    :ENDIF;

    UsrMes(sMessage);  /* Displays the selected status message;
    UsrMes("Match result: " + LimsString(bMatch));  /* Displays the match result;

    :RETURN bMatch;
:ENDPROC;

/* Usage;
DoProc("SafeLooseEquality");
```

`UsrMes` displays:

```text
Skipped: operands have different types
Match result: .F.
```

## Related elements

- [`strict-equals`](strict-equals.md)
- [`not-equals`](not-equals.md)
- [`not-equals-legacy`](not-equals-legacy.md)
- [`hash`](hash.md)
