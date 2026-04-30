---
title: "STEP"
summary: "Sets the increment or decrement used by a :FOR loop between iterations."
id: ssl.keyword.step
element_type: keyword
category: loop
tags:
  - loop-control
  - for-loop
  - increment
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# STEP

Sets the increment or decrement used by a [`:FOR`](FOR.md) loop between iterations.

Use `:STEP` inside a [`:FOR`](FOR.md) header when the loop should move by a value other than the default `1`. The step expression controls both how the loop variable changes after each pass and which direction the loop tests for completion.

When `:STEP` is omitted, SSL uses `1`. When the step is zero or positive, the loop continues while the current value is less than or equal to the limit. When the step is negative, the loop continues while the current value is greater than or equal to the limit.

## Behavior

Within a [`:FOR`](FOR.md) loop, SSL evaluates the limit expression and step expression before the loop body starts, then reuses those values for the life of that loop.

After each iteration reaches [`:NEXT;`](NEXT.md), SSL adds the step value to the loop variable and checks whether another pass should run:

- If the step is zero or positive, the loop continues while the current value is less than or equal to the limit.
- If the step is negative, the loop continues while the current value is greater than or equal to the limit.

`:STEP` is only valid as part of a [`:FOR`](FOR.md) header. Use [`:NEXT;`](NEXT.md) to close the loop. `:ENDFOR` is not accepted as the closing keyword for SSL [`:FOR`](FOR.md) loops.

## When to use

- When a counted loop should advance by more than `1`.
- When a counted loop should run backward with a negative increment.
- When the step size should come from a numeric expression rather than a fixed literal.

## Syntax

```ssl
:FOR nIndex := nStart :TO nEnd [:STEP nStep];
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nStep` | Number | No | `1` | Numeric expression that determines how much the loop variable changes after each iteration. |

## Keyword group

**Group:** Loops
**Role:** modifier

## Best practices

!!! success "Do"
    - Use `:STEP` when the loop should move by a value other than the default `1`.
    - Use a negative step explicitly for descending loops.
    - Guard computed step values when `0` would create a non-terminating loop.

!!! failure "Don't"
    - Use `:STEP 0` unless the loop body has a deliberate exit path. A zero step does not advance the loop variable.
    - Assume changing the original step expression inside the loop body changes the current loop. SSL reuses the step value chosen before the body starts.
    - Use `:ENDFOR` instead of [`:NEXT;`](NEXT.md) to close a [`:FOR`](FOR.md) loop.

## Caveats

- The step value must be numeric at runtime. Non-numeric values raise the runtime error `For stmt: Step value must be a number`.
- The loop limit must also be numeric. If it is not, SSL raises `For stmt: Limit value must be a number`.
- A step of `0` is accepted, but if the initial loop condition is true, the loop does not progress and can run indefinitely.
- `:STEP` must be uppercase and colon-prefixed.

## Examples

### Counting by twos

Collects all even numbers from 2 to `nLimit` using `:STEP 2`. With `nLimit` set to `10`, the loop produces five elements.

```ssl
:PROCEDURE CountByTwos;
	:DECLARE nIndex, nLimit, aEvenNumbers;

	nLimit := 10;
	aEvenNumbers := {};

	:FOR nIndex := 2 :TO nLimit :STEP 2;
		AAdd(aEvenNumbers, nIndex);
	:NEXT;

	InfoMes(
		"Found " + LimsString(ALen(aEvenNumbers)) +
		" even numbers up to " + LimsString(nLimit)
	);

	:RETURN aEvenNumbers;
:ENDPROC;

/* Usage example;
DoProc("CountByTwos");
```

[`InfoMes`](../functions/InfoMes.md) displays:

```text
Found 5 even numbers up to 10
```

### Counting down with a negative step

Builds a countdown array from 5 to 1 using `:STEP -1`. With five iterations in descending order, the result array has five elements.

```ssl
:PROCEDURE BuildCountdown;
	:DECLARE nIndex, aValues, sMessage;

	aValues := {};

	:FOR nIndex := 5 :TO 1 :STEP -1;
		AAdd(aValues, nIndex);
	:NEXT;

	sMessage := "Countdown length: " + LimsString(ALen(aValues));
	UsrMes(sMessage);

	:RETURN aValues;
:ENDPROC;

/* Usage example;
DoProc("BuildCountdown");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Countdown length: 5
```

### Guarding a computed step value

Validates the step before entering the loop to prevent an infinite loop when the caller passes `0`. With `nStep` set to `0`, the guard fires and the procedure returns early.

```ssl
:PROCEDURE CollectPositions;
	:PARAMETERS nStart, nEnd, nStep;
	:DECLARE nIndex, aValues;

	aValues := {};

	:IF nStep == 0;
		UsrMes("Step must not be zero");
		:RETURN aValues;
	:ENDIF;

	:FOR nIndex := nStart :TO nEnd :STEP nStep;
		AAdd(aValues, nIndex);
	:NEXT;

	:RETURN aValues;
:ENDPROC;

/* Usage example;
DoProc("CollectPositions", {1, 10, 0});
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Step must not be zero
```

## Related

- [`FOR`](FOR.md)
- [`TO`](TO.md)
- [`NEXT`](NEXT.md)
- [`EXITFOR`](EXITFOR.md)
