---
title: "ENDWHILE"
summary: "Closes a :WHILE loop block."
id: ssl.keyword.endwhile
element_type: keyword
category: control-flow
tags:
  - while-loop
  - block-closer
  - looping
  - control-flow
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ENDWHILE

Closes a [`:WHILE`](WHILE.md) loop block.

`:ENDWHILE` marks the end of the statements governed by a preceding [`:WHILE`](WHILE.md). When execution reaches the end of the loop body, control returns to the [`:WHILE`](WHILE.md) condition for the next test. If the condition is still true, another iteration starts. If the condition is false, execution continues with the next statement after `:ENDWHILE;`.

`:ENDWHILE` does not take parameters or expressions. It is only used as the closing keyword for a [`:WHILE`](WHILE.md) block.

## Behavior

`:ENDWHILE` closes this loop form:

```ssl
:WHILE condition;
    /* loop body;
:ENDWHILE;
```

Only statements between [`:WHILE`](WHILE.md) and `:ENDWHILE` belong to the loop body.
Statements after `:ENDWHILE;` run only after the loop finishes.

## When to use

- When you need to close a [`:WHILE`](WHILE.md) loop explicitly.
- When you want the loop body boundaries to be clear in nested or longer logic.

## Syntax

```ssl
:ENDWHILE;
```

## Keyword group

**Group:** Loops
**Role:** closer

## Best practices

!!! success "Do"
    - Pair each `:ENDWHILE` with the [`:WHILE`](WHILE.md) it closes.
    - Keep repeated work inside the loop body, before `:ENDWHILE;`.
    - Align `:ENDWHILE` with its matching [`:WHILE`](WHILE.md) to make nesting clear.

!!! failure "Don't"
    - Treat `:ENDWHILE` as a standalone statement unrelated to a [`:WHILE`](WHILE.md) block. It is a structural closer, not an independent control-flow action.
    - Place statements after `:ENDWHILE;` if they must run on every iteration. Code after the closer runs only after the loop exits.

## Caveats

- `:ENDWHILE` closes a [`:WHILE`](WHILE.md) block; it is not used for [`:FOR`](FOR.md) loops.
- `:ENDWHILE` must be written as an uppercase colon-prefixed keyword.

## Examples

### Closing a countdown loop

`:ENDWHILE;` marks the end of the loop body. On each iteration the counter is decremented and a message displays; when `nCount` reaches `0` the loop exits and `"Done"` prints.

```ssl
:PROCEDURE Countdown;
    :DECLARE nCount, sMessage;

    nCount := 5;

    :WHILE nCount > 0;
        sMessage := "Countdown: " + LimsString(nCount);
        UsrMes(sMessage);
        /* Displays countdown values while nCount is greater than zero;
        nCount := nCount - 1;
    :ENDWHILE;

    UsrMes("Done");
:ENDPROC;

/* Usage;
DoProc("Countdown");
```

## Related

- [`WHILE`](WHILE.md)
- [`EXITWHILE`](EXITWHILE.md)
