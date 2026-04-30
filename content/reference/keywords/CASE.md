---
title: "CASE"
summary: "Executes a block of statements if a specific boolean expression evaluates to true within a CASE structure."
id: ssl.keyword.case
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CASE

Executes a block of statements if a specific boolean expression evaluates to true within a CASE structure.

The `:CASE` keyword defines one conditional branch inside a [`:BEGINCASE`](BEGINCASE.md) ...
[`:ENDCASE`](ENDCASE.md) block. Each `:CASE` takes a boolean expression. When execution reaches [`:BEGINCASE`](BEGINCASE.md), SSL evaluates the `:CASE` expressions in order and runs the statements for each matching branch it reaches. If a branch should stop evaluation of later branches, end that branch with [`:EXITCASE`](EXITCASE.md). Without [`:EXITCASE`](EXITCASE.md), later `:CASE` expressions are still evaluated and additional matching bodies can run. If no earlier `:CASE` body runs, the [`:OTHERWISE`](OTHERWISE.md) block runs when present. `:CASE` is not a value-matching switch label; each branch uses its own standalone boolean expression.

## Behavior

`:CASE` must appear inside a [`:BEGINCASE`](BEGINCASE.md) block and is valid only as part of that structure. A [`:BEGINCASE`](BEGINCASE.md) block requires at least one `:CASE` branch and must end with [`:ENDCASE`](ENDCASE.md).

Each `:CASE` expression is converted to a logical value at runtime. If that conversion fails, execution raises a runtime error. Use explicit logical expressions so branch selection is predictable.

## When to use

- When you need to select one of several distinct branches of code based on complex boolean conditions.
- When each alternative must be guarded by its own logical test, rather than checked against a single value.
- When you want to replace a sequence of IF/ELSE chains with a more readable structure.
- When the conditions may overlap, and you want explicit control over whether later matching branches can still run.

## Syntax

```ssl
:CASE expression;
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expression` | Logical expression | Yes | The condition evaluated for this branch. When it evaluates to true, SSL runs the statements in that `:CASE` body. |

## Keyword group

**Group:** Control Flow
**Role:** separator

## Best practices

!!! success "Do"
    - Write clear boolean expressions for each `:CASE` branch.
    - End each `:CASE` body with [`:EXITCASE`](EXITCASE.md) unless you intentionally want later matching branches to run.
    - Include [`:OTHERWISE`](OTHERWISE.md) when the structure needs a default path.

!!! failure "Don't"
    - Assume [`:BEGINCASE`](BEGINCASE.md) behaves like a traditional switch statement. Each `:CASE` uses its own boolean expression, not a shared value match.
    - Omit [`:EXITCASE`](EXITCASE.md) by accident. Without it, later `:CASE` expressions are still evaluated and additional matching bodies can run.
    - Use expressions that may fail logical conversion at runtime.

## Examples

### Using CASE to select a processing path

Route an input value to a different calculation branch based on multiple logical tests. With `sSampleType` set to `"STANDARD"` and `nRawValue` of `75`, the first `:CASE` matches and applies a 10% adjustment.

```ssl
:PROCEDURE CalculateSampleResult;
    :DECLARE sSampleType, nRawValue, nFinalResult, sReport;

    sSampleType := "STANDARD";
    nRawValue := 75;

    :BEGINCASE;
    :CASE sSampleType == "STANDARD" .AND. nRawValue >= 50;
        nFinalResult := nRawValue * 1.10;
        sReport := "Standard sample passed QC with result: "
            + LimsString(nFinalResult);
        :EXITCASE;
    :CASE sSampleType == "STANDARD" .AND. nRawValue < 50;
        nFinalResult := nRawValue * 0.95;
        sReport := "Standard sample requires review with result: "
            + LimsString(nFinalResult);
        :EXITCASE;
    :CASE sSampleType == "BLINDQC";
        nFinalResult := nRawValue * 1.05;
        sReport := "Blind QC result adjusted to: "
            + LimsString(nFinalResult);
        :EXITCASE;
    :OTHERWISE;
        nFinalResult := nRawValue;
        sReport := "Unrecognized sample type processed as-is: "
            + LimsString(nFinalResult);
        :EXITCASE;
    :ENDCASE;

    UsrMes(sReport);

    :RETURN nFinalResult;
:ENDPROC;

/* Usage;
DoProc("CalculateSampleResult");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Standard sample passed QC with result: 82.5
```

### Route sample status to branch-specific actions

Dispatch a sample through different processing paths based on its status string. Each branch calls a dedicated procedure and records a result code. With `sSampleID` of `"S001"` and `sStatus` of `"NEW"`, the first branch runs.

```ssl
:PROCEDURE ProcessSampleStatus;
    :PARAMETERS sSampleID, sStatus;
    :DECLARE sMessage, nResult;

    nResult := 0;

    /* Route status handling through a CASE block;

    :BEGINCASE;
    :CASE sStatus == "NEW";
        DoProc("RegisterSample", {sSampleID});
        nResult := 1;
        sMessage := "Sample " + sSampleID + " registered successfully";
        :EXITCASE;
    :CASE sStatus == "IN_PROGRESS";
        DoProc("UpdateLocation", {sSampleID, "ANALYSIS_LAB"});
        nResult := 2;
        sMessage := "Sample " + sSampleID + " moved to analysis lab";
        :EXITCASE;
    :CASE sStatus == "COMPLETE";
        DoProc("GenerateReport", {sSampleID});
        nResult := 3;
        sMessage := "Report generated for sample " + sSampleID;
        :EXITCASE;
    :CASE sStatus == "CANCELLED";
        DoProc("LogCancellation", {sSampleID});
        nResult := 4;
        sMessage := "Sample " + sSampleID + " cancelled and logged";
        :EXITCASE;
    :OTHERWISE;
        ErrorMes("Unexpected status " + sStatus + " for sample " + sSampleID);
        /* Displays an error for an unexpected status;
        nResult := -1;
        :EXITCASE;
    :ENDCASE;

    :IF nResult > 0;
        InfoMes(sMessage);
        /* Displays the branch-specific status message;
    :ENDIF;

    :RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("ProcessSampleStatus", {"S001", "NEW"});
```

## Related

- [`BEGINCASE`](BEGINCASE.md)
- [`OTHERWISE`](OTHERWISE.md)
- [`ENDCASE`](ENDCASE.md)
- [`EXITCASE`](EXITCASE.md)
