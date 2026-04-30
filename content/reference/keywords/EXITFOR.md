---
title: "EXITFOR"
summary: "Terminates the innermost active :FOR loop immediately and continues with the statement after the matching :NEXT."
id: ssl.keyword.exitfor
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# EXITFOR

Terminates the innermost active [`:FOR`](FOR.md) loop immediately and continues with the statement after the matching [`:NEXT`](NEXT.md).

Use `:EXITFOR;` when a counted loop should stop early after a condition is met, such as finding the first matching row or detecting a stopping state. Control leaves the current [`:FOR`](FOR.md) body immediately, so later statements in that iteration do not run. In nested loops, `:EXITFOR` affects only the nearest enclosing [`:FOR`](FOR.md) loop.

## When to use

- When a counted loop should stop early after finding a target value or meeting a condition.
- When you want to avoid processing remaining items once the result is known.
- When only the innermost [`:FOR`](FOR.md) loop should exit, leaving outer loops running.

## Syntax

```ssl
:EXITFOR;
```

## Keyword group

**Group:** Loops
**Role:** modifier

## Best practices

!!! success "Do"
    - Use `:EXITFOR` to stop a [`:FOR`](FOR.md) loop once the target condition is met.
    - Keep the exit condition explicit with [`:IF`](IF.md) so the early exit is easy to read.
    - Preserve any state the caller needs after the loop, such as a found flag or result value.

!!! failure "Don't"
    - Use `:EXITFOR` outside a [`:FOR`](FOR.md) loop. That raises `Found :EXITFOR outside :FOR`.
    - Place `:EXITFOR` in a [`:FINALLY`](FINALLY.md) block. That raises `Cannot have :EXITFOR inside :FINALLY.`
    - Use `:EXITFOR` as a substitute for ordinary branching when the loop should continue running.

## Caveats

- `:EXITFOR` must be written in uppercase.
- Outside a [`:FOR`](FOR.md) loop, `:EXITFOR` raises `Found :EXITFOR outside :FOR`.
- Inside a [`:FINALLY`](FINALLY.md) block, `:EXITFOR` raises `Cannot have :EXITFOR inside :FINALLY.`

## Examples

### Finding the first matching record in a list

Stops iterating through an array after the first active sample is found. With the hardcoded data, `"Batch B"` at index 2 is the first active sample.

```ssl
:PROCEDURE FindFirstActiveSample;
    :DECLARE aSamples, nIndex, nSampleId, sSampleName, sStatus, sFoundMsg;

    /* Simulated sample rows;
    aSamples := {
        {1001, "Batch A", "INACTIVE"},
        {1002, "Batch B", "ACTIVE"},
        {1003, "Batch C", "ACTIVE"},
        {1004, "Batch D", "INACTIVE"}
    };

    sFoundMsg := "No active sample found";

    :FOR nIndex := 1 :TO ALen(aSamples);
        nSampleId := aSamples[nIndex, 1];
        sSampleName := aSamples[nIndex, 2];
        sStatus := aSamples[nIndex, 3];

        :IF sStatus == "ACTIVE";
            sFoundMsg := "Found " + sSampleName
                + " (ID " + LimsString(nSampleId) + ")";
            :EXITFOR;
        :ENDIF;
    :NEXT;

    UsrMes(sFoundMsg);

    :RETURN sFoundMsg;
:ENDPROC;

/* Usage;
DoProc("FindFirstActiveSample");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Found Batch B (ID 1002)
```

### Exit only the inner loop in nested FOR blocks

`:EXITFOR` exits only the innermost [`:FOR`](FOR.md) loop. A `bFound` flag signals the outer loop to exit on the next iteration. With `sTargetID` set to `"SMP-005"`, the match is at row 2, column 2.

```ssl
:PROCEDURE FindSampleInGrid;
    :DECLARE aSampleGrid, sTargetID, sFoundPos, nOuter, nInner, bFound;

    aSampleGrid := {
        {"SMP-001", "SMP-002", "SMP-003"},
        {"SMP-004", "SMP-005", "SMP-006"},
        {"SMP-007", "SMP-008", "SMP-009"}
    };
    sTargetID := "SMP-005";
    sFoundPos := "Not found";
    bFound := .F.;

    /* Search grid and stop inner loop at the first match;
    :FOR nOuter := 1 :TO 3;
        :FOR nInner := 1 :TO 3;
            :IF aSampleGrid[nOuter, nInner] == sTargetID;
                sFoundPos := "Row " + LimsString(nOuter) + ", Col " + LimsString(nInner);
                bFound := .T.;
                :EXITFOR;
            :ENDIF;
        :NEXT;

        :IF bFound;
            :EXITFOR;
        :ENDIF;
    :NEXT;

    UsrMes("Target: " + sTargetID + " -> " + sFoundPos);

    :RETURN bFound;
:ENDPROC;

/* Usage;
DoProc("FindSampleInGrid");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Target: SMP-005 -> Row 2, Col 2
```

## Related

- [`FOR`](FOR.md)
- [`NEXT`](NEXT.md)
- [`LOOP`](LOOP.md)
- [`EXITWHILE`](EXITWHILE.md)
