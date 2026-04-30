---
title: "IF"
summary: "Executes a block of statements only when a condition evaluates to true."
id: ssl.keyword.if
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IF

Executes a block of statements only when a condition evaluates to true.

`:IF` starts a conditional block in SSL. The condition expression is evaluated first. When it evaluates to true, the statements between `:IF` and [`:ELSE`](ELSE.md) or [`:ENDIF`](ENDIF.md) run. When it evaluates to false, that block is skipped and control moves to the optional [`:ELSE`](ELSE.md) block if one is present.

`:IF` must always be closed with [`:ENDIF;`](ENDIF.md). [`:ELSE;`](ELSE.md) is optional, but when used it must appear between the `:IF` body and [`:ENDIF;`](ENDIF.md). Execution continues with the next statement after [`:ENDIF;`](ENDIF.md) after the chosen branch finishes.

## Behavior

`:IF` is a control-flow keyword, not a function call. It takes a condition expression followed by a terminating semicolon, an optional sequence of statements in the `:IF` body, an optional [`:ELSE`](ELSE.md) section, and a closing [`:ENDIF;`](ENDIF.md).

Use [`:ELSE`](ELSE.md) when false-case handling belongs in the same decision block. For exact string comparisons inside conditions, prefer [`==`](../operators/strict-equals.md) instead of [`=`](../operators/equals.md) because [`=`](../operators/equals.md) performs prefix matching for strings in SSL.

## When to use

- When you need to execute certain statements only for records that meet a dynamic condition, such as quality checks or data validation.
- When alternate logic paths are required based on runtime data or user actions, for example, handling missing input or edge cases.
- When integrating error checks or early exits that should prevent further processing under specific circumstances.

## Syntax

```ssl
:IF condition;
    /* Statements to run when condition is true;
:ELSE;
    /* Optional statements to run when condition is false;
:ENDIF;
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `condition` | Expression | Yes | The expression evaluated to decide whether the `:IF` body runs. |

## Keyword group

**Group:** Control Flow
**Role:** opener

## Best practices

!!! success "Do"
    - Carefully design your condition to be explicit and unambiguous.
    - Always close each `:IF` with a matching [`:ENDIF`](ENDIF.md) and use [`:ELSE`](ELSE.md) when alternate branches are needed.
    - Limit each `:IF` block to a single logical decision when possible.

!!! failure "Don't"
    - Write complex nested conditions that are difficult to read or debug. Clear conditions reduce maintenance complexity and misinterpretation.
    - Omit [`:ENDIF`](ENDIF.md) or misalign [`:ENDIF`](ENDIF.md) and [`:ELSE`](ELSE.md), which can cause unreachable code or errors.
    - Overload a single `:IF` with unrelated checks connected by complex boolean logic. Keeping blocks focused improves clarity and simplifies future changes.

## Caveats

- `:IF`, [`:ELSE`](ELSE.md), and [`:ENDIF`](ENDIF.md) are case-sensitive SSL keywords and must be written in uppercase with the leading colon.

## Examples

### Run a guarded action

Executes the assignment only when the balance meets the minimum threshold. With `nBalance` set to `5000`, the condition is true and `bApproved` is set to [`.T.`](../literals/true.md).

```ssl
:PROCEDURE CheckApproval;
    :DECLARE nBalance, nMinBalance, bApproved;

    nBalance := 5000;
    nMinBalance := 1000;
    bApproved := .F.;

    :IF nBalance >= nMinBalance;
        bApproved := .T.;
    :ENDIF;

    :RETURN bApproved;
:ENDPROC;

/* Usage;
DoProc("CheckApproval");
```

### Choose between two branches

Handles both the true and false outcomes in a single conditional block. With `nTotal` set to `150` and `nCount` to `5`, the `:ELSE` branch runs and reports the average.

```ssl
:PROCEDURE CalculateAverage;
    :PARAMETERS nTotal, nCount;
    :DECLARE nAverage, sResult;

    :IF nCount == 0;
        sResult := "Cannot calculate average: sample count is zero";
        nAverage := 0;
        UsrMes(sResult);
    :ELSE;
        nAverage := nTotal / nCount;
        sResult := "Average calculated: " + LimsString(nAverage);
        InfoMes(sResult);
    :ENDIF;

    :RETURN nAverage;
:ENDPROC;

/* Usage;
DoProc("CalculateAverage", {150, 5});
```

With `nCount` set to `5`, [`InfoMes`](../functions/InfoMes.md) displays:

```text
Average calculated: 30
```

### Combine validation and exact matching

Uses multiple conditions to route processing and demonstrates exact string comparison with [`==`](../operators/strict-equals.md). With `sStatus` set to `"Logged"` and `bHasResult` to [`.T.`](../literals/true.md), the `:IF` condition is true and `sAction` is set to `"Release"`.

```ssl
:PROCEDURE RouteSample;
    :PARAMETERS sStatus, bHasResult;
    :DECLARE sAction;

    sAction := "Hold";

    :IF sStatus == "Logged" .AND. bHasResult;
        sAction := "Release";
    :ELSE;
        sAction := "Review";
    :ENDIF;

    :RETURN sAction;
:ENDPROC;

/* Usage;
DoProc("RouteSample", {"Logged", .T.});
```

## Related

- [`ELSE`](ELSE.md)
- [`ENDIF`](ENDIF.md)
