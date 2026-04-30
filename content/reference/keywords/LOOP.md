---
title: "LOOP"
summary: "Skips the rest of the current :WHILE or :FOR iteration and continues with the next iteration of the innermost active loop."
id: ssl.keyword.loop
element_type: keyword
category: loop
tags:
  - loop-control
  - continue
  - for-loop
  - while-loop
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LOOP

Skips the rest of the current [`:WHILE`](WHILE.md) or [`:FOR`](FOR.md) iteration and continues with the next iteration of the innermost active loop.

Use `:LOOP;` when the current item should be ignored but the loop itself should keep running. Any statements after `:LOOP` in the same iteration are skipped.
In nested loops, `:LOOP` affects only the nearest enclosing [`:WHILE`](WHILE.md) or [`:FOR`](FOR.md).

## Behavior

`:LOOP` has no arguments and no return value. It is a loop-control keyword, not an expression.

`:LOOP` is only valid inside an active [`:WHILE`](WHILE.md) or [`:FOR`](FOR.md) loop. Using it outside either loop raises `Found :LOOP outside :WHILE/:FOR`. It is also a compile-time error to place `:LOOP` inside a [`:FINALLY`](FINALLY.md) block, where it raises `Cannot have :LOOP inside :FINALLY.`

When `:LOOP` runs inside a [`:WHILE`](WHILE.md), control jumps to the loop's next condition check. When it runs inside a [`:FOR`](FOR.md), control jumps to the loop's increment step and then evaluates whether another iteration should run.

## When to use

- When the current [`:WHILE`](WHILE.md) or [`:FOR`](FOR.md) iteration should be skipped, but later iterations should still run.
- When validation fails for the current item and the remaining work for that item should be ignored.
- When an early guard makes the loop body clearer than wrapping the rest of the iteration in extra nested [`:IF`](IF.md) blocks.

## Syntax

```ssl
:LOOP;
```

## Keyword group

**Group:** Loops
**Role:** modifier

## Best practices

!!! success "Do"
    - Use `:LOOP` for guard-style early skips when the loop should continue.
    - Place `:LOOP` immediately after the condition that makes the current item invalid or irrelevant.
    - Keep required per-iteration state updates before `:LOOP`, or in a place that still runs on skipped iterations.

!!! failure "Don't"
    - Use [`:EXITFOR`](EXITFOR.md) or [`:EXITWHILE`](EXITWHILE.md) when only the current iteration should be skipped. Those keywords terminate the loop instead of continuing it.
    - Place `:LOOP` inside a [`:FINALLY`](FINALLY.md) block. That raises `Cannot have :LOOP inside :FINALLY.`
    - Place `:LOOP` where required cleanup or bookkeeping would be skipped unintentionally.
    - Assume code after `:LOOP` still runs for that iteration. It never does.

## Caveats

- `:LOOP` must be written as an uppercase colon-prefixed keyword.

## Examples

### Skip invalid entries in a FOR loop

Processes only non-empty sample IDs and skips blank entries using `:LOOP`. With 4 valid entries in the input array, the output count is `4`.

```ssl
:PROCEDURE ProcessValidSamples;
    :DECLARE aSamples, aValidSamples, sSampleID, nIndex;

    aSamples := {"SAMPLE-001", "", "SAMPLE-002", "SAMPLE-003", "", "SAMPLE-004"};
    aValidSamples := {};

    :FOR nIndex := 1 :TO ALen(aSamples);
        sSampleID := aSamples[nIndex];

        :IF Empty(sSampleID);
            :LOOP;
        :ENDIF;

        AAdd(aValidSamples, sSampleID);
    :NEXT;

    UsrMes("Valid sample count: " + LimsString(ALen(aValidSamples)));

    :RETURN aValidSamples;
:ENDPROC;

DoProc("ProcessValidSamples");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Valid sample count: 4
```

### Skip blank and duplicate entries in a WHILE loop

Uses `:LOOP` twice: once to skip blanks and once to skip duplicates already collected. With the input array, 3 unique non-empty IDs are collected.

```ssl
:PROCEDURE CollectUniqueSamples;
    :DECLARE aInputs, aUniqueSamples, sSampleID, nIndex, nInner, bExists;

    aInputs := {"SMP-001", "", "SMP-002", "SMP-001", "SMP-003", ""};
    aUniqueSamples := {};
    nIndex := 1;

    :WHILE nIndex <= ALen(aInputs);
        sSampleID := aInputs[nIndex];
        nIndex := nIndex + 1;

        :IF Empty(sSampleID);
            :LOOP;
        :ENDIF;

        bExists := .F.;

        :FOR nInner := 1 :TO ALen(aUniqueSamples);
            :IF aUniqueSamples[nInner] == sSampleID;
                bExists := .T.;
                :EXITFOR;
            :ENDIF;
        :NEXT;

        :IF bExists;
            :LOOP;
        :ENDIF;

        AAdd(aUniqueSamples, sSampleID);
    :ENDWHILE;

    UsrMes("Unique sample count: " + LimsString(ALen(aUniqueSamples)));

    :RETURN aUniqueSamples;
:ENDPROC;

DoProc("CollectUniqueSamples");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Unique sample count: 3
```

## Related

- [`EXITFOR`](EXITFOR.md)
- [`EXITWHILE`](EXITWHILE.md)
- [`FOR`](FOR.md)
- [`WHILE`](WHILE.md)
- [`NEXT`](NEXT.md)
- [`ENDWHILE`](ENDWHILE.md)
