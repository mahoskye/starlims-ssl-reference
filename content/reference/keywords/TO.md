---
title: "TO"
summary: "Sets the inclusive loop limit used by a :FOR loop."
id: ssl.keyword.to
element_type: keyword
category: loop
tags:
  - loop-control
  - for-loop
  - range
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# TO

Sets the inclusive loop limit used by a [`:FOR`](FOR.md) loop.

Use `:TO` inside a [`:FOR`](FOR.md) header to define the boundary value that the loop variable is tested against before each iteration. It works with the loop's start value and optional [`:STEP`](STEP.md) value to determine whether the loop continues.

When the step is zero or positive, SSL keeps looping while the current value is less than or equal to the `:TO` limit. When the step is negative, SSL keeps looping while the current value is greater than or equal to the `:TO` limit.

## Behavior

Within a [`:FOR`](FOR.md) header, `:TO` introduces the loop limit expression.

- If the step is zero or positive, the loop continues while the current value is less than or equal to the limit.
- If the step is negative, the loop continues while the current value is greater than or equal to the limit.
- The end boundary is inclusive, so a loop whose current value equals the limit still runs that iteration.

## When to use

- When a counted loop should stop at a specific numeric boundary.
- When the end of the loop range comes from a variable or expression.
- When the same [`:FOR`](FOR.md) pattern should support either ascending or descending iteration with [`:STEP`](STEP.md).

## Syntax

```ssl
:FOR nIndex := nStart :TO nEnd [:STEP nStep];
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nEnd` | Number | Yes | — | Numeric loop limit checked before each iteration. |

## Keyword group

**Group:** Loops
**Role:** separator

## Best practices

!!! success "Do"
    - Use `:TO` with a clear numeric limit so the loop boundary is easy to read.
    - Pair `:TO` with a negative [`:STEP`](STEP.md) when the loop should count downward.
    - Validate computed bounds when they come from user input or runtime data.

!!! failure "Don't"
    - Use `:TO` outside a [`:FOR`](FOR.md) header.
    - Assume a zero [`:STEP`](STEP.md) is safe. If the initial loop condition is true, the loop variable never advances.
    - Pass non-numeric values for the current value, limit, or step. SSL raises runtime errors for those cases.

## Caveats

- `:TO` is only valid as part of a [`:FOR`](FOR.md) header.
- The current value must be numeric at runtime or SSL raises `For stmt: Current value must be a number`.
- The limit value must be numeric at runtime or SSL raises `For stmt: Limit value must be a number`.
- The step value must be numeric at runtime or SSL raises `For stmt: Step value must be a number`.
- A step of `0` is accepted, but if the initial loop condition is true, the loop can become non-terminating because the loop variable does not change.
- `:TO` must be uppercase and colon-prefixed.

## Examples

### Counting up to a fixed limit

Iterates from 1 to 10 using `:TO 10` as the inclusive upper bound. Each iteration logs a step message.

```ssl
:PROCEDURE CountToTen;
    :DECLARE nIndex, sMessage;

    :FOR nIndex := 1 :TO 10;
        sMessage := "Step " + LimsString(nIndex);
        UsrMes(sMessage);
    :NEXT;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("CountToTen");
```

`UsrMes` displays one line per iteration:

```text
Step 1
...
Step 10
```

### Using a dynamic loop limit

Sets the `:TO` value from the array length so the loop processes every element. With three sample IDs, the loop runs three iterations.

```ssl
:PROCEDURE ProcessSampleBatch;
    :DECLARE aSamples, nLastRow, nIndex, sMessage;

    aSamples := {"S-1001", "S-1002", "S-1003"};
    nLastRow := ALen(aSamples);

    :FOR nIndex := 1 :TO nLastRow;
        sMessage := "Processing " + aSamples[nIndex];
        UsrMes(sMessage);
    :NEXT;

    :RETURN nLastRow;
:ENDPROC;

/* Usage;
DoProc("ProcessSampleBatch");
```

`UsrMes` displays one line per iteration:

```text
Processing S-1001
Processing S-1002
Processing S-1003
```

### Counting down to a lower limit

Pairs `:TO` with [`:STEP`](STEP.md) `-1` to count downward from 5 to the inclusive lower bound of 1. Five elements are collected in descending order.

```ssl
:PROCEDURE BuildCountdown;
    :DECLARE nIndex, aValues;

    aValues := {};

    :FOR nIndex := 5 :TO 1 :STEP -1;
        AAdd(aValues, nIndex);
    :NEXT;

    UsrMes("Countdown: " + LimsString(ALen(aValues)) + " items");

    :RETURN aValues;
:ENDPROC;

/* Usage;
DoProc("BuildCountdown");
```

`UsrMes` displays:

```text
Countdown: 5 items
```

## Related

- [`FOR`](FOR.md)
- [`STEP`](STEP.md)
- [`NEXT`](NEXT.md)
