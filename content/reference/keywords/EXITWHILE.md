---
title: "EXITWHILE"
summary: "Terminates the innermost active :WHILE loop and continues with the statement after the matching :ENDWHILE."
id: ssl.keyword.exitwhile
element_type: keyword
category: loop
tags:
  - loop-control
  - exit
  - while-loop
  - early-exit
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# EXITWHILE

Terminates the innermost active [`:WHILE`](WHILE.md) loop and continues with the statement after the matching [`:ENDWHILE`](ENDWHILE.md).

Use `:EXITWHILE;` when a [`:WHILE`](WHILE.md) loop should stop as soon as a condition is met, such as finding a match, detecting a fatal validation problem, or reaching a stopping state that makes more iterations unnecessary. Control leaves the current [`:WHILE`](WHILE.md) body immediately, so later statements in that iteration do not run. In nested loops, `:EXITWHILE` affects only the nearest enclosing [`:WHILE`](WHILE.md).

## When to use

- When a [`:WHILE`](WHILE.md) loop should stop as soon as a target condition is satisfied.
- When a critical condition inside the loop means the remaining iterations should be skipped.
- When an early exit makes the loop clearer than adding more nested [`:IF`](IF.md) blocks.

## Syntax

```ssl
:EXITWHILE;
```

## Keyword group

**Group:** Loops
**Role:** modifier

## Best practices

!!! success "Do"
    - Use `:EXITWHILE` to stop a [`:WHILE`](WHILE.md) loop once the loop's goal has been reached.
    - Keep the exit condition explicit with [`:IF`](IF.md) so the early exit is easy to follow.
    - Preserve any state the caller needs after the loop, such as a found flag or error message.

!!! failure "Don't"
    - Use `:EXITWHILE` outside a [`:WHILE`](WHILE.md) loop. That raises `Found :EXITWHILE outside :WHILE`.
    - Place `:EXITWHILE` in a [`:FINALLY`](FINALLY.md) block. That raises `Cannot have :EXITWHILE inside :FINALLY.`
    - Use `:EXITWHILE` as a substitute for ordinary loop conditions when the loop should exit naturally.

## Caveats

- `:EXITWHILE` must be written as an uppercase colon-prefixed keyword.
- Outside a [`:WHILE`](WHILE.md) loop, `:EXITWHILE` raises `Found :EXITWHILE outside :WHILE`.
- Inside a [`:FINALLY`](FINALLY.md) block, `:EXITWHILE` raises `Cannot have :EXITWHILE inside :FINALLY.`

## Examples

### Stop validation at the first critical error

Exits the [`:WHILE`](WHILE.md) loop as soon as a missing sample ID is detected. The hardcoded batch has an empty entry at position 4, so validation halts there and returns [`.F.`](../literals/false.md).

```ssl
:PROCEDURE ValidateSampleBatch;
    :DECLARE aSamples, sSampleID, nCount, nIndex, bCriticalError, sErrorMsg;

    aSamples := {"SA-1001", "SA-1002", "SA-1003", "", "SA-1005"};
    nCount := ALen(aSamples);
    nIndex := 1;
    bCriticalError := .F.;
    sErrorMsg := "";

    :WHILE nIndex <= nCount;
        sSampleID := aSamples[nIndex];

        :IF Empty(sSampleID);
            bCriticalError := .T.;
            sErrorMsg := "Sample ID is required at position " + LimsString(nIndex);
            ErrorMes(sErrorMsg);  /* Displays on failure: missing sample ID message;
            :EXITWHILE;
        :ENDIF;

        UsrMes("Validated: " + sSampleID);
        nIndex := nIndex + 1;
    :ENDWHILE;

    :IF bCriticalError;
        :RETURN .F.;
    :ENDIF;

    UsrMes("Batch validation complete");

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateSampleBatch");
```

### Exit only the inner WHILE in nested loops

`:EXITWHILE` exits only the nearest [`:WHILE`](WHILE.md). A `bFound` flag signals the outer loop to exit on the next check. With `sTargetID` set to `"SMP-005"`, the match is at row 2, column 2.

```ssl
:PROCEDURE FindTargetCell;
    :DECLARE aSampleGrid, sTargetID, sFoundPos, nRow, nCol, bFound;

    aSampleGrid := {
        {"SMP-001", "SMP-002", "SMP-003"},
        {"SMP-004", "SMP-005", "SMP-006"},
        {"SMP-007", "SMP-008", "SMP-009"}
    };
    sTargetID := "SMP-005";
    sFoundPos := "Not found";
    nRow := 1;
    bFound := .F.;

    :WHILE nRow <= ALen(aSampleGrid);
        nCol := 1;

        :WHILE nCol <= ALen(aSampleGrid[nRow]);
            :IF aSampleGrid[nRow, nCol] == sTargetID;
                sFoundPos := "Row " + LimsString(nRow) + ", Col " + LimsString(nCol);
                bFound := .T.;
                :EXITWHILE;
            :ENDIF;

            nCol := nCol + 1;
        :ENDWHILE;

        :IF bFound;
            :EXITWHILE;
        :ENDIF;

        nRow := nRow + 1;
    :ENDWHILE;

    UsrMes(sFoundPos);

    :RETURN sFoundPos;
:ENDPROC;

/* Usage;
DoProc("FindTargetCell");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Row 2, Col 2
```

## Related

- [`WHILE`](WHILE.md)
- [`ENDWHILE`](ENDWHILE.md)
- [`EXITFOR`](EXITFOR.md)
- [`LOOP`](LOOP.md)
