---
title: "strict-equals"
summary: "Returns .T. when two values are strictly equal under SSL equality rules."
id: ssl.operator.strict-equals
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# strict-equals

## What it does

Returns [`.T.`](../literals/true.md) when two values are strictly equal under SSL equality rules.

The `==` operator uses exact equality for strings, numbers, booleans, and dates. For arrays and objects, it checks whether both operands reference the same instance rather than comparing contents. `NIL == NIL` returns [`.T.`](../literals/true.md), while [`NIL`](../literals/nil.md) compared with a non-[`NIL`](../literals/nil.md) value returns [`.F.`](../literals/false.md). Comparing a code block raises a runtime error.

For strings, `==` requires an exact match - it does not use the prefix matching behavior of [`equals`](equals.md). For example, `"Logged" == "Log"` returns [`.F.`](../literals/false.md), while `"Logged" = "Log"` returns [`.T.`](../literals/true.md).

Type-mismatch behavior depends on the left operand. A string on the left compared with a non-string on the right returns [`.F.`](../literals/false.md). A numeric, boolean, or date value on the left compared with an incompatible right operand raises a runtime invalid-operand error.

## When to use it

- When exact string equality is required (not prefix matching).
- When checking exact value equality on numbers, booleans, and dates.
- When checking reference equality on arrays and objects.
- When guarding dynamic comparisons where operand types may vary at runtime.

## Syntax

```ssl
bEqual := vLeft == vRight;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) only when both strings are exactly equal. |
| [string](../types/string.md) | non-string | [boolean](../types/boolean.md) | Returns [`.F.`](../literals/false.md). |
| [number](../types/number.md) | [number](../types/number.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when both numeric values are exactly equal. |
| [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when both boolean values are the same. |
| [date](../types/date.md) | [date](../types/date.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when both date values are equal. |
| [array](../types/array.md) | [array](../types/array.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) only when both operands reference the same array instance. |
| [object](../types/object.md) | [object](../types/object.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) only when both operands reference the same object instance. |
| [`NIL`](../literals/nil.md) | [`NIL`](../literals/nil.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md). |
| [`NIL`](../literals/nil.md) | non-[`NIL`](../literals/nil.md) | [boolean](../types/boolean.md) | Returns [`.F.`](../literals/false.md). |
| code block | any | error | Raises a runtime error. |

## Precedence

- **Precedence:** Equality
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `==` for exact string equality and exact value checks.
    - Use `==` when you intentionally want reference equality for arrays or objects.
    - Guard dynamic values before comparing when runtime types may differ.

!!! failure "Don't"
    - Use `==` when you want string prefix behavior. Use [`equals`](equals.md) for that case.
    - Assume `==` compares arrays or objects by content. It only checks whether both operands reference the same instance.
    - Assume `==` coerces numbers, booleans, or dates to other types automatically.

## Errors and edge cases

- Code block left operand raises `Cannot compare to a code block`.

## Examples

### Comparing two strings exactly

Shows that `==` requires an exact match. `"Logged" == "Log"` is [`.F.`](../literals/false.md) because `"Log"` is not the full string - use [`equals`](equals.md) for prefix checks.

```ssl
:PROCEDURE CheckExactStatus;
    :DECLARE sExpected, sActual, bMatch, sMessage;

    sExpected := "Logged";
    sActual := "Log";
    bMatch := sExpected == sActual;

    :IF bMatch;
        sMessage := "Status matches exactly";
    :ELSE;
        sMessage := "Status does not match exactly";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bMatch;
:ENDPROC;

/*
Usage:
DoProc("CheckExactStatus")
;
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Status does not match exactly
```

### Guarding dynamic values before strict comparison

Checks runtime types first when a comparison may receive mixed values. With `vLeft = 42` (number) and `vRight = "42"` (string), the types differ and the comparison is skipped.

```ssl
:PROCEDURE CompareDynamicValues;
    :DECLARE vLeft, vRight, sLeftType, sRightType, bMatch, sMessage;

    vLeft := 42;
    vRight := "42";
    sLeftType := LimsTypeEx(vLeft);
    sRightType := LimsTypeEx(vRight);
    bMatch := .F.;

    :IF sLeftType == sRightType;
        bMatch := vLeft == vRight;
        sMessage := "Strict comparison completed";
    :ELSE;
        sMessage := "Skipped comparison because the operand types differ";
    :ENDIF;

    UsrMes(sMessage);

    UsrMes("Match result: " + LimsString(bMatch));
    /* Displays the boolean result;

    :RETURN bMatch;
:ENDPROC;

/*
Usage:
DoProc("CompareDynamicValues")
;
```

### Checking reference equality for objects

Shows that `==` returns [`.T.`](../literals/true.md) when two variables point to the same instance (`oAlias`) but [`.F.`](../literals/false.md) when they point to different instances with the same property values (`oSecond`).

```ssl
:PROCEDURE CompareObjectReferences;
    :DECLARE oFirst, oSecond, oAlias, bSameRef, bDifferentRef;

    oFirst := CreateLocal();
    oFirst:sampleId := "S-1001";

    oSecond := CreateLocal();
    oSecond:sampleId := "S-1001";

    oAlias := oFirst;
    bSameRef := oFirst == oAlias;
    bDifferentRef := oFirst == oSecond;

    :IF bSameRef;
        UsrMes("oFirst and oAlias reference the same object");
    :ENDIF;

    :IF !bDifferentRef;
        UsrMes("oFirst and oSecond are different objects even though their values match");
    :ENDIF;

    :RETURN bSameRef;
:ENDPROC;

/*
Usage:
DoProc("CompareObjectReferences")
;
```

## Related elements

- [`equals`](equals.md)
- [`not-equals`](not-equals.md)
- [`not-equals-legacy`](not-equals-legacy.md)
- [`hash`](hash.md)
