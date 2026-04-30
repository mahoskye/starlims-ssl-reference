---
title: "not-equals-legacy"
summary: "Returns .T. when two values are not equal under SSL's strict inequality rules."
id: ssl.operator.not-equals-legacy
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# not-equals-legacy

## What it does

Returns [`.T.`](../literals/true.md) when two values are not equal under SSL's strict inequality rules.

The `<>` operator is the legacy not-equals form. It is a full alias for [`not-equals`](not-equals.md) ([`!=`](not-equals.md)) and [`hash`](hash.md) ([`#`](hash.md)). All three behave identically: SSL evaluates strict equality first, then negates the result.

For strings, `<>` uses exact comparison, not prefix matching. For example, `"Logged" <> "Log"` returns [`.T.`](../literals/true.md) because strict equality returns [`.F.`](../literals/false.md). If you want loose prefix matching, use [`equals`](equals.md) with [`=`](equals.md) instead. For numbers, booleans, and dates, it compares values directly. For arrays and objects, it compares references rather than walking contents.

Type-mismatch behavior depends on the left operand. A string on the left compared with a non-string on the right returns [`.T.`](../literals/true.md). A numeric, boolean, or date value on the left compared with an incompatible right operand raises a runtime invalid-operand error instead of returning a boolean.

## When to use it

- When maintaining older SSL code that already uses the legacy form.
- When exact string inequality is required.
- When checking value inequality on numbers, booleans, and dates.
- When checking reference inequality on arrays and objects.

## Syntax

```ssl
bDifferent := vLeft <> vRight;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the strings are not exactly equal. |
| [string](../types/string.md) | non-string | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md). |
| [number](../types/number.md) | [number](../types/number.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the numeric values differ. |
| [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the boolean values differ. |
| [date](../types/date.md) | [date](../types/date.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the dates differ. |
| [array](../types/array.md) | [array](../types/array.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) unless both operands reference the same array instance. |
| [object](../types/object.md) | [object](../types/object.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) unless both operands reference the same object instance. |
| [`NIL`](../literals/nil.md) | [`NIL`](../literals/nil.md) | [boolean](../types/boolean.md) | Returns [`.F.`](../literals/false.md). |
| [`NIL`](../literals/nil.md) | non-[`NIL`](../literals/nil.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md). |
| code block | any | error | Raises a runtime error. |

## Precedence

- **Precedence:** Equality
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `<>` only when legacy code style or compatibility makes that form the clearer choice.
    - Guard dynamic values before comparing when operand types may vary at runtime.
    - Walk the structure yourself when a deep content comparison is needed for arrays and objects.

!!! failure "Don't"
    - Use `<>` in new code when [`!=`](not-equals.md) is the clearer house style.
    - Assume `<>` is the opposite of loose string matching with [`=`](equals.md). It negates strict equality instead.
    - Expect `<>` to coerce numbers, booleans, or dates to other types automatically.

## Errors and edge cases

- Code block left operand raises `Cannot compare to a code block`.

## Examples

### Comparing exact string values in legacy code

Checks whether two status strings differ. `"PENDING" <> "COMPLETE"` is [`.T.`](../literals/true.md), so the changed branch runs.

```ssl
:PROCEDURE CheckStatusChange;
    :DECLARE sStoredStatus, sCurrentStatus, bChanged, sMessage;

    sStoredStatus := "PENDING";
    sCurrentStatus := "COMPLETE";
    bChanged := sStoredStatus <> sCurrentStatus;

    :IF bChanged;
        sMessage := "Status changed from " + sStoredStatus + " to " + sCurrentStatus;
    :ELSE;
        sMessage := "Status did not change";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bChanged;
:ENDPROC;

/* Usage;
DoProc("CheckStatusChange");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Status changed from PENDING to COMPLETE
```

### Guarding operand types before numeric inequality

Checks runtime types first when a legacy comparison may receive mixed values. With both values numeric, `4 <> 3` is [`.T.`](../literals/true.md), and the mismatch branch runs.

```ssl
:PROCEDURE CheckReplicateMismatch;
    :DECLARE nExpected, nActual, sExpectedType, sActualType;
    :DECLARE bMismatch, sMessage;

    nExpected := 3;
    nActual := 4;
    sExpectedType := LimsTypeEx(nExpected);
    sActualType := LimsTypeEx(nActual);
    bMismatch := .F.;

    :IF sExpectedType == "NUMERIC" .AND. sActualType == "NUMERIC";
        bMismatch := nActual <> nExpected;

        :IF bMismatch;
            sMessage := "Replicate count differs";
        :ELSE;
            sMessage := "Replicate count matches";
        :ENDIF;
    :ELSE;
        sMessage := "Skipped comparison because both values must be numeric";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bMismatch;
:ENDPROC;

/* Usage;
DoProc("CheckReplicateMismatch");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Replicate count differs
```

### Distinguishing reference inequality from content checks

Shows that `<>` treats two separate arrays as different objects even when they hold the same values. The reference check returns [`.T.`](../literals/true.md); the element-wise walk shows no differences.

```ssl
:PROCEDURE CompareSnapshots;
    :DECLARE aPrevious, aCurrent, bRefDifferent, bValueDifferent;
    :DECLARE sMessage, nIndex;

    aPrevious := {"LAB-001", "LAB-002", "LAB-003"};
    aCurrent := {"LAB-001", "LAB-002", "LAB-003"};
    bRefDifferent := aPrevious <> aCurrent;
    bValueDifferent := .F.;

    :FOR nIndex := 1 :TO ALen(aPrevious);
        :IF aPrevious[nIndex] <> aCurrent[nIndex];
            bValueDifferent := .T.;
            :EXITFOR;
        :ENDIF;
    :NEXT;

    sMessage := "Reference differs: " + LimsString(bRefDifferent);
    UsrMes(sMessage); /* Displays reference-difference result;

    sMessage := "Element values differ: " + LimsString(bValueDifferent);
    UsrMes(sMessage); /* Displays element-difference result;

    :RETURN bRefDifferent;
:ENDPROC;

/* Usage;
DoProc("CompareSnapshots");
```

## Related elements

- [`equals`](equals.md)
- [`not-equals`](not-equals.md)
- [`hash`](hash.md)
