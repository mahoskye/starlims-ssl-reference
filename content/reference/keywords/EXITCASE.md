---
title: "EXITCASE"
summary: "Ends the current :CASE or :OTHERWISE branch and continues after :ENDCASE."
id: ssl.keyword.exitcase
element_type: keyword
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# EXITCASE

Ends the current [`:CASE`](CASE.md) or [`:OTHERWISE`](OTHERWISE.md) branch and continues with the first statement after [`:ENDCASE`](ENDCASE.md) `;`.

Use `:EXITCASE;` inside a [`:BEGINCASE`](BEGINCASE.md) block when a matching branch should stop the whole block immediately. When `:EXITCASE;` is present, execution continues with the statement after [`:ENDCASE`](ENDCASE.md) `;`. Without it, later [`:CASE`](CASE.md) expressions can still be evaluated and additional matching case bodies can run.

`:EXITCASE` does not take parameters and does not return a value. It is valid only as the last statement of a [`:CASE`](CASE.md) or [`:OTHERWISE`](OTHERWISE.md) branch within a [`:BEGINCASE`](BEGINCASE.md) block, directly in the branch body.

## When to use

- When one matching branch should prevent all later branches from being evaluated.
- When you want a [`:BEGINCASE`](BEGINCASE.md) block to behave like an either-or selection.
- When you want the control-flow stop to be explicit instead of relying on the reader to reason about fall-through.

## Syntax

```ssl
:EXITCASE;
```

## Keyword group

**Group:** Control Flow
**Role:** modifier

## Best practices

!!! success "Do"
    - End each [`:CASE`](CASE.md) and [`:OTHERWISE`](OTHERWISE.md) branch with `:EXITCASE;` unless you intentionally want later matching branches to run.
    - Use `:EXITCASE;` to make single-branch [`:BEGINCASE`](BEGINCASE.md) behavior explicit.
    - Keep `:EXITCASE;` on its own line as the last statement of the branch body.

!!! failure "Don't"
    - Omit `:EXITCASE;` by accident. Without it, later [`:CASE`](CASE.md) expressions are still evaluated and more than one branch body may run.
    - Place statements after `:EXITCASE;` in the same branch, or put `:EXITCASE;` inside an [`:IF`](IF.md) within the branch. Both are compile-time errors (`unexpected token`).
    - Use `:EXITCASE;` outside a [`:BEGINCASE`](BEGINCASE.md) structure.

## Caveats

- SSL keywords are case-sensitive. Write `:EXITCASE` in uppercase.
- `:EXITCASE;` cannot be made conditional. To leave the block from part of a branch, restructure the branch (for example, split it into separate [`:CASE`](CASE.md) conditions) instead of nesting `:EXITCASE;` in an [`:IF`](IF.md).

## Examples

### Stop after the first matching branch

`:EXITCASE;` prevents later branches from running after the current match. The third condition also accepts `"HIGH"`, so with `sStatus` set to `"HIGH"` both the second and third conditions are true. The second branch runs, and its `:EXITCASE;` ends the block before the third condition is evaluated. Without it, the third body would also run and replace the priority with `"Queue for normal processing"`.

```ssl
:PROCEDURE GetSamplePriority;
    :PARAMETERS sStatus;
    :DECLARE sPriority, sMessage;

    sPriority := "";

    :BEGINCASE;
    :CASE sStatus == "CRITICAL";
        sPriority := "Immediate attention required";
        :EXITCASE;
    :CASE sStatus == "HIGH";
        sPriority := "Process within 24 hours";
        :EXITCASE;
    :CASE sStatus == "HIGH" .OR. sStatus == "STANDARD";
        sPriority := "Queue for normal processing";
        :EXITCASE;
    :OTHERWISE;
        sPriority := "Manual review required";
        :EXITCASE;
    :ENDCASE;

    sMessage := "Sample priority: " + sPriority;
    UsrMes(sMessage);

    :RETURN sPriority;
:ENDPROC;

/* Usage;
DoProc("GetSamplePriority", {"HIGH"});
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
Sample priority: Process within 24 hours
```

### Classify a result value with exclusive branches

Each branch uses `:EXITCASE;` so only one category applies. With `nResultValue` set to `95`, both conditions are true (95 >= 90 and 95 >= 75). The first branch runs and its `:EXITCASE;` ends the block, so the result is `"Critical"`. Without it, the second body would also run and replace the category with `"Warning"`.

```ssl
:PROCEDURE ClassifyResult;
    :PARAMETERS nResultValue;
    :DECLARE sCategory;

    sCategory := "";

    :BEGINCASE;
    :CASE nResultValue >= 90;
        sCategory := "Critical";
        :EXITCASE;
    :CASE nResultValue >= 75;
        sCategory := "Warning";
        :EXITCASE;
    :OTHERWISE;
        sCategory := "Normal";
        :EXITCASE;
    :ENDCASE;

    UsrMes(sCategory);

    :RETURN sCategory;
:ENDPROC;

/* Usage;
DoProc("ClassifyResult", {95});
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
Critical
```

## Related

- [`BEGINCASE`](BEGINCASE.md)
- [`CASE`](CASE.md)
- [`OTHERWISE`](OTHERWISE.md)
- [`ENDCASE`](ENDCASE.md)
