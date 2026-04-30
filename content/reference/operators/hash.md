---
title: "hash"
summary: "Returns .T. when two values are not equal and .F. when they are equal."
id: ssl.operator.hash
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# hash

## What it does

Returns [`.T.`](../literals/true.md) when two values are not equal and [`.F.`](../literals/false.md) when they are equal.

The `#` operator tests for inequality. It delegates to the same equality logic as [`=`](equals.md), then negates the result. For numbers, booleans, and dates, the comparison is exact. For strings, the comparison uses the same prefix semantics as [`=`](equals.md): `"Logged" # "Log"` is [`.F.`](../literals/false.md) because `"Logged" = "Log"` is [`.T.`](../literals/true.md). For arrays and objects, `#` compares by reference — two distinct arrays or objects with identical contents are not equal under `#`.

`#` is a full alias for [`not-equals`](not-equals.md) ([`!=`](not-equals.md)). Both behave identically.

Type-mismatch behavior depends on the left operand. A string on the left returns [`.T.`](../literals/true.md) when the right operand is not a string (because the underlying [`=`](equals.md) returns [`.F.`](../literals/false.md)). A number, date, or boolean on the left raises a runtime error when the right operand is an incompatible type.

## When to use it

- When testing whether two values differ.
- When filtering out a sentinel or default value in a condition.
- When either `#` or [`!=`](not-equals.md) is already used throughout the codebase and you want to stay consistent.

## Syntax

```ssl
bResult := vLeft # vRight;
```

## Type behavior

| Left | Right | Result | Behavior |
| --- | --- | --- | --- |
| [number](../types/number.md) | [number](../types/number.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the values differ numerically. |
| [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the boolean values differ. |
| [date](../types/date.md) | [date](../types/date.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the dates differ. |
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the strings are not equal under SSL's prefix matching. |
| [string](../types/string.md) | non-string | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) (underlying [`=`](equals.md) returns [`.F.`](../literals/false.md)). |
| [array](../types/array.md) | [array](../types/array.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) unless both operands reference the same array instance. |
| [object](../types/object.md) | [object](../types/object.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) unless both operands reference the same object instance. |
| NIL | NIL | [boolean](../types/boolean.md) | Returns [`.F.`](../literals/false.md). |
| NIL | non-[`NIL`](../literals/nil.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md). |
| number/boolean/date | incompatible | error | Raises a runtime invalid-operand error. |

## Precedence

- **Precedence:** Equality
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `#` or [`!=`](not-equals.md) for testing inequality of supported types.
    - Validate operand types before using `#`, or wrap the comparison in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when types are not guaranteed.
    - Walk the structure yourself when you need a deep content comparison for arrays and objects.

!!! failure "Don't"
    - Assume `#` and [`!=`](not-equals.md) behave differently. They are full aliases with identical logic.
    - Assume `#` silently returns [`.T.`](../literals/true.md) for any type mismatch. Only a string-on-left path behaves that way; numeric, date, and boolean left operands with incompatible rights raise a runtime error.
    - Assume `#` walks array or object contents. It only compares references.

## Errors and edge cases

- [`NIL`](../literals/nil.md) only equals another [`NIL`](../literals/nil.md); `NIL # "anything"` is [`.T.`](../literals/true.md).
- String comparisons are case-sensitive.

## Examples

### Comparing two numbers for inequality

Sets `bMismatch` to [`.T.`](../literals/true.md) when `nMeasured` and `nExpected` differ. With 42 and 40, the values differ and [`IIf`](../functions/IIf.md) selects `"YES"`.

```ssl
:PROCEDURE CompareTwoNumbers;
    :DECLARE nMeasured, nExpected, bMismatch, sResult;

    nMeasured := 42;
    nExpected := 40;
    bMismatch := nMeasured # nExpected;

    sResult := "Values differ? " + IIf(bMismatch, "YES", "NO");
    UsrMes(sResult);

    :RETURN bMismatch;
:ENDPROC;

/* Usage;
DoProc("CompareTwoNumbers");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Values differ? YES
```

### Reference inequality vs element-wise comparison

Shows that `#` on two distinct arrays always returns [`.T.`](../literals/true.md) (different references), even when the contents are identical. The element-wise walk must be done by hand. After mutating one element, the walk detects the difference.

```ssl
:PROCEDURE DetectArrayDifference;
    :DECLARE aPrevious, aCurrent, bChanged, sResult;
    :DECLARE nIndex, nLen, bAnyDiffer;

    aPrevious := {"LAB-001", "LAB-002", "LAB-003"};
    aCurrent  := {"LAB-001", "LAB-002", "LAB-003"};

    /* Reference inequality: two distinct arrays, so # is .T.;
    bChanged := aPrevious # aCurrent;
    sResult := "Reference differs? " + IIf(bChanged, "YES", "NO");
    UsrMes(sResult);
    /* Displays: Reference differs? YES;

    /* Element-wise walk: contents are equal;
    bAnyDiffer := .F.;
    nLen := ALen(aPrevious);
    :IF nLen # ALen(aCurrent);
        bAnyDiffer := .T.;
    :ELSE;
        :FOR nIndex := 1 :TO nLen;
            :IF aPrevious[nIndex] # aCurrent[nIndex];
                bAnyDiffer := .T.;
                :EXITFOR;
            :ENDIF;
        :NEXT;
    :ENDIF;

    sResult := "Any element differs? " + IIf(bAnyDiffer, "YES", "NO");
    UsrMes(sResult);
    /* Displays: Any element differs? NO;

    /* Mutate one element and re-check;
    aCurrent[2] := "LAB-099";
    bAnyDiffer := .F.;
    :FOR nIndex := 1 :TO ALen(aPrevious);
        :IF aPrevious[nIndex] # aCurrent[nIndex];
            bAnyDiffer := .T.;
            :EXITFOR;
        :ENDIF;
    :NEXT;

    sResult := "Any element differs after edit? " + IIf(bAnyDiffer, "YES", "NO");
    UsrMes(sResult);
    /* Displays: Any element differs after edit? YES;

    :RETURN bAnyDiffer;
:ENDPROC;

/* Usage;
DoProc("DetectArrayDifference");
```

## Related elements

- [`not-equals`](not-equals.md)
- [`not-equals-legacy`](not-equals-legacy.md)
- [`equals`](equals.md)
