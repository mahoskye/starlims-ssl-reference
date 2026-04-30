---
title: "less-than"
summary: "Compares two values of the same supported type and returns .T. when the left operand is strictly less than the right operand."
id: ssl.operator.less-than
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# less-than

## What it does

Compares two values of the same supported type and returns [`.T.`](../literals/true.md) when the left operand is strictly less than the right operand.

The `<` operator supports number, date, and string comparisons. Numbers are compared numerically, dates are compared chronologically, and strings are compared with case-sensitive invariant ordering. If the operands are different types, or if the left operand type does not support `<`, the comparison raises a runtime error instead of returning a boolean value.

## When to use it

- When a value must be strictly below a numeric threshold.
- When checking whether one date occurs before another.
- When comparing string keys with SSL's built-in case-sensitive ordering.

## Syntax

```ssl
vLeft < vRight
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left number is less than the right number. |
| [date](../types/date.md) | [date](../types/date.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left date is earlier than the right date. |
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left string sorts before the right string in case-sensitive invariant order. |

## Precedence

- **Precedence:** Relational
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `<` only with matching supported types: number, date, or string.
    - Use [`less-than-or-equal`](less-than-or-equal.md) when the boundary value should also pass.
    - Validate or normalize input before comparing dynamic values.

!!! failure "Don't"
    - Rely on implicit type conversion between strings, numbers, and dates. `<` raises a runtime error for mismatched types.
    - Use `<` when equality should pass. Use [`less-than-or-equal`](less-than-or-equal.md) for inclusive checks.
    - Assume string ordering follows user-locale rules. SSL uses case-sensitive invariant ordering.

## Errors and edge cases

- Comparing a value against [`NIL`](../literals/nil.md) raises a runtime error instead of returning a boolean value.
- String comparisons are case-sensitive and culture-invariant, which can give results that differ from end-user alphabetical expectations.

## Examples

### Checking whether a reading is below a limit

Compares `nReading` against `nMinimum`. With 12 < 15, the result is [`.T.`](../literals/true.md) and the below-minimum branch runs.

```ssl
:PROCEDURE CheckMinimumThreshold;
    :DECLARE nReading, nMinimum, bIsBelowMinimum, sResult;

    nReading := 12;
    nMinimum := 15;
    bIsBelowMinimum := nReading < nMinimum;

    :IF bIsBelowMinimum;
        sResult := "Reading is below the minimum threshold";
    :ELSE;
        sResult := "Reading is not below the minimum threshold";
    :ENDIF;

    UsrMes(sResult);

    :RETURN bIsBelowMinimum;
:ENDPROC;

/* Usage;
DoProc("CheckMinimumThreshold");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Reading is below the minimum threshold
```

### Checking whether a sample date is before a cutoff

Compares two dates. With 03/28/2024 < 03/31/2024, the result is [`.T.`](../literals/true.md) and the before-cutoff branch runs.

```ssl
:PROCEDURE CheckDateCutoff;
    :DECLARE dSampleDate, dCutoffDate, bIsBeforeCutoff, sMessage;

    dSampleDate := CToD("03/28/2024");
    dCutoffDate := CToD("03/31/2024");
    bIsBeforeCutoff := dSampleDate < dCutoffDate;

    :IF bIsBeforeCutoff;
        sMessage := "Sample date is before the cutoff: " + DToC(dSampleDate);
    :ELSE;
        sMessage := "Sample date is on or after the cutoff: " + DToC(dSampleDate);
    :ENDIF;

    InfoMes(sMessage);

    :RETURN bIsBeforeCutoff;
:ENDPROC;

/* Usage;
DoProc("CheckDateCutoff");
```

[`InfoMes`](../functions/InfoMes.md) displays:

```text
Sample date is before the cutoff: 03/28/2024
```

### Guarding a dynamic comparison with [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md)

Uses [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when operand types are dynamic. Here `sLeft` is a string and `nRight` is a number, so the comparison raises a runtime error and the [`:CATCH`](../keywords/CATCH.md) branch runs. The exact error description is runtime-dependent.

```ssl
:PROCEDURE CompareDynamicValues;
    :DECLARE sLeft, nRight, bIsLessThan, oError, sMessage;

    sLeft := "25";
    nRight := 100;
    bIsLessThan := .F.;

    :TRY;
        bIsLessThan := sLeft < nRight;
        sMessage := "Comparison result: " + LimsString(bIsLessThan);
        InfoMes(sMessage);
    :CATCH;
        oError := GetLastSSLError();
        sMessage := "Comparison failed: " + oError:Description;
        InfoMes(sMessage);
    :ENDTRY;

    :RETURN bIsLessThan;
:ENDPROC;

/* Usage;
DoProc("CompareDynamicValues");
```

[`InfoMes`](../functions/InfoMes.md) displays an error message. The exact description varies by runtime:

```text
Comparison failed: <runtime error description>
```

## Related elements

- [`greater-than`](greater-than.md)
- [`less-than-or-equal`](less-than-or-equal.md)
- [`greater-than-or-equal`](greater-than-or-equal.md)
