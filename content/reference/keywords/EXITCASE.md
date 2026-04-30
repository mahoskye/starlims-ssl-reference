---
title: "EXITCASE"
summary: "Ends the current :CASE or :OTHERWISE branch and continues after :ENDCASE."
id: ssl.keyword.exitcase
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# EXITCASE

Ends the current [`:CASE`](CASE.md) or [`:OTHERWISE`](OTHERWISE.md) branch and continues with the first statement after [`:ENDCASE`](ENDCASE.md) `;`.

Use `:EXITCASE;` inside a [`:BEGINCASE`](BEGINCASE.md) block when a matching branch should stop the whole block immediately. When `:EXITCASE;` is present, execution continues with the statement after [`:ENDCASE`](ENDCASE.md) `;`. Without it, later [`:CASE`](CASE.md) expressions can still be evaluated and additional matching case bodies can run.

`:EXITCASE` does not take parameters and does not return a value. It is valid only inside a [`:CASE`](CASE.md) or [`:OTHERWISE`](OTHERWISE.md) branch within a [`:BEGINCASE`](BEGINCASE.md) block.

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
    - Keep `:EXITCASE;` on its own line at the end of the branch body.

!!! failure "Don't"
    - Omit `:EXITCASE;` by accident. Without it, later [`:CASE`](CASE.md) expressions are still evaluated and more than one branch body may run.
    - Place statements after `:EXITCASE;` in the same branch. That code is unreachable and makes the block harder to read.
    - Use `:EXITCASE;` outside a [`:BEGINCASE`](BEGINCASE.md) structure.

## Caveats

- SSL keywords are case-sensitive. Write `:EXITCASE` in uppercase.

## Examples

### Stop after the first matching branch

`:EXITCASE;` prevents later branches from running after the current match. With `sStatus` set to `"HIGH"`, only the second branch executes and the procedure reports its priority message.

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
    :CASE sStatus == "STANDARD";
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

[`UsrMes`](../functions/UsrMes.md) displays:

```
Sample priority: Process within 24 hours
```

### Classify a result value with exclusive branches

Each branch uses `:EXITCASE;` so only one category applies. With `nResultValue` set to `80`, the second branch matches (80 >= 75) and the first is skipped (80 < 90).

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
DoProc("ClassifyResult", {80});
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Warning
```

## Related

- [`BEGINCASE`](BEGINCASE.md)
- [`CASE`](CASE.md)
- [`OTHERWISE`](OTHERWISE.md)
- [`ENDCASE`](ENDCASE.md)
