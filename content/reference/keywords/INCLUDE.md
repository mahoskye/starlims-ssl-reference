---
title: "INCLUDE"
summary: "Inserts another SSL script's source into the current file so its statements compile as if they were written inline."
id: ssl.keyword.include
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# INCLUDE

Inserts another SSL script's source into the current file so its statements compile as if they were written inline.

The `:INCLUDE` keyword names another script whose source is added to the current script for compilation. Declarations, procedures, and other top-level statements from the included script are available to the including script as though they appeared at the include location.

`:INCLUDE` does not create a separate scope, does not add a call stack frame, and does not behave like a module import. The include target is written as an identifier or qualified identifier such as `Common.Helpers`.

## Behavior

`:INCLUDE` is written as a regular statement, but it is a compile-time source inclusion directive. The included script is not called at runtime; its source is incorporated into the current script for compilation.

Because the included source is inserted inline, its statements must still make sense at the point where they are included. In reviewed code, place `:INCLUDE` early in the file so required declarations and procedures are available before later statements depend on them.

If the same include target is encountered again while compiling a script, the later include is treated as empty. This prevents recursive re-inclusion, but it also means circular include chains can surface later as missing declarations or other compile errors instead of as a dedicated circular-include error.

## When to use

- When you need to share declarations, helper procedures, or common setup across multiple SSL scripts.
- When keeping repeated boilerplate in one reusable script makes maintenance simpler.
- When a script depends on shared top-level SSL code that should compile as part of the current script.

## Syntax

```ssl
:INCLUDE scriptName;
```

```ssl
:INCLUDE category.scriptName;
```

## Parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `scriptName` | Identifier or qualified identifier | Yes | The script name to inline into the current script for compilation. |

## Keyword group

**Group:** Declarations
**Role:** directive

## Best practices

!!! success "Do"
    - Place `:INCLUDE` near the top of the file so the inserted declarations and procedures are available before later code depends on them.
    - Use includes for shared top-level SSL code such as helper procedures, declarations, or common setup.
    - Keep include targets explicit and stable so other developers can tell where shared behavior comes from.

!!! failure "Don't"
    - Treat `:INCLUDE` like a runtime call or a namespace import. It inserts source text directly into the current script for compilation.
    - Scatter include directives deep inside procedural logic unless you have a specific structural reason. Early placement is easier to read and reason about.
    - Rely on repeated or circular includes as a control mechanism. Later repeats are ignored while compiling a script, which can hide the real source of missing declarations.

## Caveats

- `:INCLUDE` must be written in uppercase with the leading colon.
- The target name must use identifier syntax, not a quoted string.
- If the target script cannot be loaded, compilation fails.

## Examples

### Include shared declarations before script logic

Brings common declarations into a script before using them. `gcDefaultSampleId` is declared in the included `Common.SampleGlobals` script and is available to statements after the include.

```ssl
:INCLUDE Common.SampleGlobals;

:DECLARE sSampleId;

sSampleId := gcDefaultSampleId;

UsrMes("Processing sample " + sSampleId);
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Processing sample <gcDefaultSampleId>
```

### Include shared helper procedures and call them

Includes helper procedures from another script, then calls them with [`DoProc`](../functions/DoProc.md) from the current script. `GetOrderStatus` and `MarkOrderComplete` are both defined in the included `Common.OrderHelpers` script.

```ssl
:INCLUDE Common.OrderHelpers;

:DECLARE sOrderId, sStatus;

sOrderId := "ORDER-001";
sStatus := DoProc("GetOrderStatus", {sOrderId});

:IF sStatus == "Pending";
	DoProc("MarkOrderComplete", {sOrderId});
:ENDIF;
```

### Share reusable setup across multiple procedures

Uses a single include to make batch utilities available across related batch-processing steps in the same script. The helpers come from the included `Common.BatchUtilities` script.

```ssl
:INCLUDE Common.BatchUtilities;

:DECLARE sBatchId, aSamples, sMessage;

sBatchId := "BATCH-001";
aSamples := DoProc("LoadBatchSamples", {sBatchId});
DoProc("ValidateBatchSamples", {aSamples});

sMessage := DoProc("BuildBatchAuditMessage", {sBatchId});
InfoMes(sMessage);
```

[`InfoMes`](../functions/InfoMes.md) displays:

```text
<batch audit message>
```

## Related

- [`PARAMETERS`](PARAMETERS.md)
- [`DECLARE`](DECLARE.md)
- [`PROCEDURE`](PROCEDURE.md)
- [`PUBLIC`](PUBLIC.md)
