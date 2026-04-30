---
title: "IIf"
summary: "Selects one of two values based on a boolean condition."
id: ssl.function.iif
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IIf

Selects one of two values based on a boolean condition.

`IIf` returns `vTrueValue` when `bCondition` is true and `vFalseValue` when `bCondition` is false. The condition argument must be a boolean value and cannot be [`NIL`](../literals/nil.md). The second and third arguments can be any value type.

## When to use

- When you need a compact two-way value choice inside an assignment or return.
- When both possible values are already available as literals or variables.
- When using a full [`:IF`](../keywords/IF.md) block would make a simple expression harder to read.

## Syntax

```ssl
IIf(bCondition, vTrueValue, vFalseValue)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `bCondition` | [boolean](../types/boolean.md) | yes | — | Condition indicating which value to return |
| `vTrueValue` | any | yes | — | Value to return if `bCondition` is true |
| `vFalseValue` | any | yes | — | Value to return if `bCondition` is false |

## Returns

**any** — `vTrueValue` when `bCondition` is [`.T.`](../literals/true.md); otherwise `vFalseValue`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `bCondition` is [`NIL`](../literals/nil.md). | `Null argument passed to IIf()` |
| The call does not supply exactly three arguments. | `Invalid number of arguments for function IIF.` |

## Best practices

!!! success "Do"
    - Use `IIf` for short, direct two-way value selection.
    - Pass a boolean expression for `bCondition`.
    - Prefer literals or previously assigned variables for `vTrueValue` and `vFalseValue`.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) as `bCondition`.
    - Rely on `IIf` to avoid evaluating the unused branch.
    - Build long nested `IIf` chains when a regular [`:IF`](../keywords/IF.md) block is clearer.

## Caveats

- `IIf` is a normal function call. Its arguments are evaluated before the function returns either `vTrueValue` or `vFalseValue`.
- The compiler validates `IIf` calls specially and raises a compile-time error when the call does not contain exactly three arguments.
- The compiler can warn when the second or third argument is not a constant or a variable name.

## Examples

### Assign a label based on a boolean flag

Select a status label for display based on a boolean flag, showing the most direct use of `IIf` as a compact conditional assignment.

```ssl
:PROCEDURE GetApprovalStatus;
    :DECLARE bIsApproved, sStatusLabel;

    bIsApproved := .T.;
    sStatusLabel := IIf(bIsApproved, "Approved", "Pending Review");

    UsrMes(sStatusLabel);

    :RETURN sStatusLabel;
:ENDPROC;

/* Usage;
DoProc("GetApprovalStatus");
```

[`UsrMes`](UsrMes.md) displays:

```text
Approved
```

### Select a prepared SQL filter

Build a SQL filter clause dynamically by selecting between two pre-prepared filter strings, showing how `IIf` can be embedded directly inside a string concatenation expression.

```ssl
:PROCEDURE BuildSampleQuery;
    :DECLARE bLoggedOnly, sStatusFilter, sDateFilter, sSQL;

    bLoggedOnly := .T.;
    sStatusFilter := "status = 'Logged'";
    sDateFilter := "logdate >= SYSDATE - 7";

    sSQL := "
        SELECT sampleid, status, logdate
        FROM sample
        WHERE " + IIf(bLoggedOnly, sStatusFilter, sDateFilter) + "
        ORDER BY logdate DESC
    ";

    :RETURN sSQL;
:ENDPROC;

/* Usage;
DoProc("BuildSampleQuery");
```

### Prepare both branch values before calling IIf

Illustrates the recommended style: compute both branch values before the `IIf` call rather than inline, making both branches easier to read and avoiding complex expressions inside the call itself.

```ssl
:PROCEDURE GetReportLabel;
    :DECLARE bUseDetailed, sShortLabel, sDetailedLabel, sLabel;

    bUseDetailed := .T.;

    sShortLabel := "QC Summary";
    sDetailedLabel := "QC Summary - Includes exception details";

    sLabel := IIf(bUseDetailed, sDetailedLabel, sShortLabel);

    :RETURN sLabel;
:ENDPROC;

/* Usage;
DoProc("GetReportLabel");
```

## Related

- [`IF`](../keywords/IF.md)
- [`BEGINCASE`](../keywords/BEGINCASE.md)
- [`boolean`](../types/boolean.md)
