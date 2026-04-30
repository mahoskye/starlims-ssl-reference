---
title: "WHILE"
summary: "Repeats a block of statements as long as a supplied condition evaluates to true."
id: ssl.keyword.while
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# WHILE

Repeats a block of statements as long as a supplied condition evaluates to true.

The `:WHILE` keyword starts a loop that evaluates a condition before each iteration. When the condition is true, SSL executes the loop body and then tests the condition again. When the condition becomes false, execution continues with the first statement after [`:ENDWHILE`](ENDWHILE.md).

`:WHILE` is a control-flow statement, not an expression. It must be written as a statement block that begins with `:WHILE condition;` and ends with [`:ENDWHILE`](ENDWHILE.md). The condition must evaluate to a boolean value at runtime.

Use [`:EXITWHILE`](EXITWHILE.md) to leave the current `:WHILE` loop immediately. Use [`:LOOP`](LOOP.md) to skip the remainder of the current iteration and jump back to the next condition check.

## Behavior

`:WHILE` performs a pre-test loop. SSL checks the condition before entering the body, so a `:WHILE` block may execute zero times.

The loop body can contain any valid SSL statements, including nested loops, conditionals, and error handling blocks. [`:EXITWHILE`](EXITWHILE.md) exits the current `:WHILE` immediately. [`:LOOP`](LOOP.md) continues with the next iteration by returning to the loop's condition check.

`:WHILE` does not produce a value. Its purpose is flow control only.

## When to use

- When you need to process input, such as reading lines from a file, until
  there are no more lines to read.
- When performing repetitive calculations that must continue until a specific
  result or threshold is reached.
- Anytime you do not know in advance how many iterations are required, or the
  number of iterations depends on values that change inside the loop.

## Syntax

```ssl
:WHILE condition;
    /* loop body;
:ENDWHILE;
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `condition` | Boolean expression | Yes | — | Expression evaluated before each iteration. The loop continues while it evaluates to true. |

## Keyword group

**Group:** Loops
**Role:** opener

## Best practices

!!! success "Do"
    - Update the condition state inside the loop so progress toward termination is clear.
    - Use `:WHILE` when the number of iterations depends on values that change at runtime.
    - Use [`:EXITWHILE`](EXITWHILE.md) or [`:LOOP`](LOOP.md) deliberately when they make the loop flow easier to read.

!!! failure "Don't"
    - Rely on a condition that never changes within the block, because that can create an unintended infinite loop.
    - Use `:WHILE` when a [`:FOR`](FOR.md) loop expresses a fixed-count iteration more clearly.
    - Use [`:EXITWHILE`](EXITWHILE.md) or [`:LOOP`](LOOP.md) outside a loop, or inside a [`:FINALLY`](FINALLY.md) block, because those forms are invalid.

## Caveats

- Omitting the matching [`:ENDWHILE`](ENDWHILE.md) causes a compile-time error.
- If the condition does not evaluate to a boolean value at runtime, SSL raises a runtime error.
- [`:EXITWHILE`](EXITWHILE.md) outside a `:WHILE` block causes a compile-time error:
  `Found :EXITWHILE outside :WHILE`.
- [`:LOOP`](LOOP.md) outside a `:WHILE` or [`:FOR`](FOR.md) block causes a compile-time error:
  `Found :LOOP outside :WHILE/:FOR`.
- [`:EXITWHILE`](EXITWHILE.md) and [`:LOOP`](LOOP.md) are not allowed inside [`:FINALLY`](FINALLY.md) blocks.
- Keywords are case-sensitive and must be uppercase, for example `:WHILE` and [`:ENDWHILE`](ENDWHILE.md).

## Examples

### Processing user input until completion

Reads simulated input, continuing only while the source returns non-empty, non-`"QUIT"` values. With the inline [`IIf`](../functions/IIf.md) stand-in returning `""` on the fourth call, the loop runs four iterations.

```ssl
:PROCEDURE ProcessUserInputs;
    :DECLARE sInput, nCount, aInputs;

    aInputs := {};
    nCount := 0;
    sInput := "initial";

    /* Continue until the source returns blank or QUIT;
    :WHILE !Empty(sInput) .AND. sInput != "QUIT";
        nCount += 1;
        AAdd(aInputs, sInput);

        /* Replace this with the real input source in production code;
        sInput := IIf(nCount < 4, "item_" + LimsString(nCount), "");
    :ENDWHILE;

    UsrMes("Processed " + LimsString(nCount) + " inputs");

    :RETURN aInputs;
:ENDPROC;

/* Usage;
DoProc("ProcessUserInputs");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Processed 4 inputs
```

### Recalculating values until a threshold is met

Applies Newton's method to approximate a square root, looping until successive estimates differ by less than `0.01`. With `nTarget` set to `50`, the loop converges to approximately `7.07`; with `150`, it converges to approximately `12.25`.

```ssl
:PROCEDURE CalculateSquareRoot;
    :PARAMETERS nTarget;
    :DECLARE nEstimate, nPrevious, nDiff, sResult;

    nEstimate := nTarget / 2;
    nDiff := 1;

    :WHILE nDiff > 0.01;
        nPrevious := nEstimate;
        nEstimate := (nEstimate + nTarget / nEstimate) / 2;
        nDiff := Abs(nPrevious - nEstimate);
    :ENDWHILE;

    sResult := "Square root of " + LimsString(nTarget) + " = " + LimsString(nEstimate);
    UsrMes(sResult);

    :RETURN nEstimate;
:ENDPROC;

:PROCEDURE DemonstrateIteration;
    :DECLARE nTarget, nResult;

    nTarget := 50;
    nResult := DoProc("CalculateSquareRoot", {nTarget});
    nTarget := 150;
    nResult := DoProc("CalculateSquareRoot", {nTarget});
:ENDPROC;

/* Usage;
DoProc("DemonstrateIteration");
```

[`UsrMes`](../functions/UsrMes.md) displays twice:

```text
Square root of 50 = 7.07...
Square root of 150 = 12.25...
```

### Nested loops with conditional exit

Scans a 4×3 sample grid to find `"SAMPLE-003"`, exiting the inner loop with [`:EXITWHILE`](EXITWHILE.md) when found and stopping the outer loop via the `!bFound` condition. With `sTarget` set to `"SAMPLE-003"`, the match is in row 3, column 1.

```ssl
:PROCEDURE ProcessSampleMatrix;
    :DECLARE aSampleGrid, oResult, nRow, nCol, nRows, nCols, sTarget, bFound, sLog;
    :DECLARE nTargetRow, nTargetCol;

    aSampleGrid := {
        {"SAMPLE-001", "Pending", "2024-01-15"},
        {"SAMPLE-002", "Active", "2024-01-16"},
        {"SAMPLE-003", "Pending", "2024-01-17"},
        {"SAMPLE-004", "Complete", "2024-01-18"}
    };

    nRows := ALen(aSampleGrid);
    nCols := ALen(aSampleGrid[1]);
    sTarget := "SAMPLE-003";
    bFound := .F.;
    nTargetRow := 0;
    nTargetCol := 0;
    sLog := "";

    oResult := CreateLocal();
    oResult:status := "Not Found";
    oResult:target := sTarget;

    nRow := 1;
    :WHILE nRow <= nRows .AND. !bFound;
        nCol := 1;

        :WHILE nCol <= nCols;
            :IF aSampleGrid[nRow, nCol] == sTarget;
                nTargetRow := nRow;
                nTargetCol := nCol;
                bFound := .T.;
                sLog := sLog + "Target found at row " + LimsString(nTargetRow);
                sLog := sLog + ", col " + LimsString(nTargetCol) + ".";
                :EXITWHILE;
            :ENDIF;

            nCol += 1;
        :ENDWHILE;

        :IF !bFound;
            sLog := sLog + "Row " + LimsString(nRow) + " scanned. ";
        :ENDIF;

        nRow += 1;
    :ENDWHILE;

    :IF bFound;
        oResult:status := "Found";
        oResult:row := nTargetRow;
        oResult:column := nTargetCol;
        oResult:value := aSampleGrid[nTargetRow, nTargetCol];
    :ENDIF;

    UsrMes(sLog);

    :RETURN oResult;
:ENDPROC;

/* Usage;
DoProc("ProcessSampleMatrix");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Row 1 scanned. Row 2 scanned. Target found at row 3, col 1.
```

## Related

- [`ENDWHILE`](ENDWHILE.md)
- [`EXITWHILE`](EXITWHILE.md)
- [`FOR`](FOR.md)
- [`LOOP`](LOOP.md)
