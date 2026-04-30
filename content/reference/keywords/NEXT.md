---
title: "NEXT"
summary: "Closes a :FOR loop and returns control to the loop's increment-and-test step."
id: ssl.keyword.next
element_type: keyword
category: loop
tags:
  - loop-control
  - for-loop
  - block-terminator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# NEXT

Closes a [`:FOR`](FOR.md) loop and returns control to the loop's increment-and-test step.

Use `:NEXT;` as the required closing keyword for a [`:FOR`](FOR.md) block. After the loop body runs, control reaches `:NEXT;`, the loop variable is updated by the current step, and SSL checks whether another iteration should run. If the loop remains in range, execution returns to the top of the loop body. Otherwise, execution continues with the statement after `:NEXT;`.

`:NEXT;` is the required terminator for [`:FOR`](FOR.md) loops in SSL. It is not a standalone loop-control statement like [`:LOOP;`](LOOP.md) or [`:EXITFOR;`](EXITFOR.md).

## Behavior

`:NEXT;` has no arguments and no return value.

Within a [`:FOR`](FOR.md) loop, SSL reaches `:NEXT;` after the current iteration's body finishes. At that point, the loop variable is incremented or decremented by the loop step, then SSL evaluates whether the loop should continue. If the loop condition still holds, the next iteration starts. If not, execution resumes after `:NEXT;`.

Because `:NEXT;` is the required [`:FOR`](FOR.md) terminator, omitting it or placing it outside the matching loop breaks the [`:FOR`](FOR.md) block structure.

## When to use

- When closing any [`:FOR`](FOR.md) loop.
- When you need the loop variable to advance and the loop condition to be checked again.
- When writing counted loops that must end with the standard SSL `:FOR ... :NEXT` structure.

## Syntax

```ssl
:NEXT;
```

## Keyword group

**Group:** Loops
**Role:** closer

## Best practices

!!! success "Do"
    - Place `:NEXT;` immediately after the full body of the [`:FOR`](FOR.md) loop it closes.
    - Keep the loop body indented consistently so the matching [`:FOR`](FOR.md) and `:NEXT;` are easy to read.
    - Put statements that should run once after the loop below `:NEXT;`, not inside the loop body.

!!! failure "Don't"
    - Treat `:NEXT;` like [`:LOOP;`](LOOP.md) or [`:EXITFOR;`](EXITFOR.md). `:NEXT;` closes the loop block; it does not skip or terminate an iteration early.
    - Omit `:NEXT;` from a [`:FOR`](FOR.md) loop. SSL requires it to close the block.
    - Place unrelated statements between the intended end of the loop body and `:NEXT;` in a way that makes the loop boundary unclear.

## Caveats

- `:NEXT;` must be written as an uppercase colon-prefixed keyword.
- Code after `:NEXT;` runs only after the loop finishes, not after each iteration.
- Use [`:EXITFOR;`](EXITFOR.md) to leave a loop early and [`:LOOP;`](LOOP.md) to skip to the next iteration. `:NEXT;` serves a different role.

## Examples

### Closing a simple counted loop

Shows the standard [`:FOR`](FOR.md) `... :NEXT` structure. With `nLimit` set to `5`, five messages are printed.

```ssl
:PROCEDURE CountSamples;
    :DECLARE nIndex, nLimit, sMessage;

    nLimit := 5;

    :FOR nIndex := 1 :TO nLimit;
        sMessage := "Processing sample iteration " + LimsString(nIndex);
        UsrMes(sMessage);
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("CountSamples");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Processing sample iteration 1
Processing sample iteration 2
Processing sample iteration 3
Processing sample iteration 4
Processing sample iteration 5
```

### Running follow-up work after the loop ends

Demonstrates that statements after `:NEXT;` run once, after all loop iterations complete. The summary message is printed after the loop builds all three IDs.

```ssl
:PROCEDURE BuildSampleList;
    :DECLARE aSampleIDs, nIndex, sSummary;

    aSampleIDs := {};

    :FOR nIndex := 1 :TO 3;
        AAdd(aSampleIDs, "SMP-" + LimsString(nIndex));
    :NEXT;

    sSummary := "Created " + LimsString(ALen(aSampleIDs)) + " sample IDs";
    UsrMes(sSummary);

    :RETURN aSampleIDs;
:ENDPROC;

/* Usage;
DoProc("BuildSampleList");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Created 3 sample IDs
```

## Related

- [`FOR`](FOR.md)
- [`TO`](TO.md)
- [`STEP`](STEP.md)
- [`EXITFOR`](EXITFOR.md)
- [`LOOP`](LOOP.md)
