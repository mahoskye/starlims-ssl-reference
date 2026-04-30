---
title: "FOR"
summary: "Executes a counted loop by assigning a numeric variable, checking it against a numeric limit, and updating it after each iteration."
id: ssl.keyword.for
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# FOR

Executes a counted loop by assigning a numeric variable, checking it against a numeric limit, and updating it after each iteration.

The `:FOR` keyword defines a counted loop. It initializes a numeric loop variable, checks whether the current value is still within the loop limit, runs the loop body, then updates the variable by the step value before testing again. [`:STEP`](STEP.md) is optional and defaults to `1`. A `:FOR` loop always closes with [`:NEXT`](NEXT.md)`;`, and [`:EXITFOR`](EXITFOR.md)`;` can leave the loop early.

The limit expression and optional step expression are evaluated once before the loop starts. Changing the variables used in those expressions inside the loop body does not change the current loop's bounds.

## Behavior

`:FOR` runs in this order:

1. Assign the start value to the loop variable.
2. Check whether the current value is still within the loop limit.
3. Run the loop body.
4. Add the step value to the loop variable.
5. Repeat until the exit condition fails, then continue after [`:NEXT`](NEXT.md)`;`.

When the step is zero or positive, the loop continues while the current value is less than or equal to the limit. When the step is negative, the loop continues while the current value is greater than or equal to the limit.

## When to use

- When you need to execute a block of statements a known number of times.
- When iterating through arrays with an explicit numeric index.
- When counting upward or downward by a fixed increment.

## Syntax

```ssl
:FOR nIndex := nStart :TO nEnd [:STEP nStep];
```

## Parameters

| Name | Description |
|------|-------------|
| `nIndex` | Numeric loop variable assigned before the first iteration and updated after each iteration. |
| `nStart` | Initial numeric value assigned to the loop variable. |
| `nEnd` | Numeric loop limit checked before each iteration. |
| `nStep` | Optional numeric increment or decrement. If omitted, SSL uses `1`. |

## Keyword group

**Group:** Loops
**Role:** opener

## Best practices

!!! success "Do"
    - Use [`:STEP`](STEP.md) only when you need an increment other than the default `1`.
    - Use distinct loop variables in nested loops so the control flow stays readable.

!!! failure "Don't"
    - Omit the closing [`:NEXT`](NEXT.md)`;` or use [`:EXITFOR`](EXITFOR.md)`;` outside a `:FOR ... :NEXT` block.
    - Rely on changes to the original limit or step expressions inside the loop body.

## Caveats

- Leaving out the required closing [`:NEXT`](NEXT.md)`;` causes a parse error.
- [`:EXITFOR`](EXITFOR.md)`;` outside a `:FOR` loop causes a compile-time error with the message `Found :EXITFOR outside :FOR`.
- The start, limit, and step values must be numeric at runtime.
- If the start value is already past the limit for the chosen step direction, the loop body does not run.
- A step of `0` prevents the loop variable from advancing, which can create a non-terminating loop when the initial condition is true.

## Examples

### Iterating from 1 to 5

Runs the loop body for each integer from `1` to `5`, printing a count message on each iteration.

```ssl
:PROCEDURE CountToFive;
    :DECLARE nIndex, sMessage;

    :FOR nIndex := 1 :TO 5;
        sMessage := "Count is " + LimsString(nIndex);
        UsrMes(sMessage);
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("CountToFive");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Count is 1
Count is 2
Count is 3
Count is 4
Count is 5
```

### Using STEP to count by 2

[`:STEP`](STEP.md) changes the increment between iterations. The loop builds a comma-separated list of even numbers up to `10`.

```ssl
:PROCEDURE ListEvenNumbers;
    :DECLARE nIndex, nMax, sResult;

    nMax := 10;
    sResult := "Even numbers up to " + LimsString(nMax) + ": ";

    :FOR nIndex := 2 :TO nMax :STEP 2;
        :IF nIndex > 2;
            sResult := sResult + ", ";
        :ENDIF;

        sResult := sResult + LimsString(nIndex);
    :NEXT;

    UsrMes(sResult);
:ENDPROC;

/* Usage;
DoProc("ListEvenNumbers");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Even numbers up to 10: 2, 4, 6, 8, 10
```

### Counting backward and stopping early

A negative [`:STEP`](STEP.md) counts downward; [`:EXITFOR`](EXITFOR.md) stops the loop as soon as the target is found. Searching from the end, `nSampleId` `1042` is at position `2`.

```ssl
:PROCEDURE FindPrioritySample;
    :DECLARE aSamples, nIndex, nSampleId, sStatus, sResult;
    :DECLARE bFound;

    aSamples := {
        {1001, "Normal"},
        {1042, "Critical"},
        {1087, "Normal"},
        {1105, "Normal"}
    };

    nSampleId := 1042;
    bFound := .F.;
    sResult := "Sample not found";

    :FOR nIndex := ALen(aSamples) :TO 1 :STEP -1;
        :IF aSamples[nIndex, 1] == nSampleId;
            sStatus := aSamples[nIndex, 2];

            :IF sStatus == "Critical";
                sResult := "Critical sample found at position " + LimsString(nIndex);
                bFound := .T.;
                :EXITFOR;
            :ENDIF;

            sResult := "Sample " + LimsString(nSampleId) + " has status: "
                + sStatus;
        :ENDIF;
    :NEXT;

    InfoMes(sResult);

    :RETURN bFound;
:ENDPROC;

/* Usage;
DoProc("FindPrioritySample");
```

[`InfoMes`](../functions/InfoMes.md) displays:

```text
Critical sample found at position 2
```

## Related

- [`NEXT`](NEXT.md)
- [`TO`](TO.md)
- [`STEP`](STEP.md)
- [`EXITFOR`](EXITFOR.md)
