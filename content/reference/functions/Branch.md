---
title: "Branch"
summary: "Transfers control to a label in the current procedure."
id: ssl.function.branch
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# Branch

Transfers control to a label in the current procedure.

`Branch` requires exactly one argument. If that argument is a string literal, SSL uses that literal text as the branch target, and it must match a label in the current procedure exactly, including case. A literal target that matches no label stops the script from compiling, so none of it runs. If the argument is any other expression, `Branch` never jumps: no label matches a computed target, even when its text is exactly the label's, and execution continues with the next statement without an error. This holds at script level and inside procedures, and for variables, parameters and expressions such as `"LABEL " + "SKIP"`. Always pass the target as a string literal.

For normal label declarations such as [`:LABEL CLEANUP;`](../keywords/LABEL.md), the target text must match the label as written after the colon, so the usual form is `Branch("LABEL CLEANUP")`. You can branch to a label that appears later in the same procedure. When `Branch` is used inside a [`:TRY`](../keywords/TRY.md) or [`:CATCH`](../keywords/CATCH.md) region, SSL leaves that protected region before transferring control.
`Branch` does not return a useful value.

## When to use

- When you need to jump to a shared cleanup or recovery section in the same procedure.
- When maintaining legacy SSL that already uses labels for explicit control flow.
- When a jump to a fixed label is clearer than duplicating the same exit logic in several places.

## Syntax

```ssl
Branch(vTarget)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vTarget` | any | yes | — | Target label text. A string literal is used directly as the target text and must match a label exactly, including case. Any other expression never matches a label, so the call falls through to the next statement. |

## Returns

**NIL** — Does not return a value for application logic. Redirects control flow when a matching label is found.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| More than one argument is provided. | `Compile-time error: <line>:<column> Branch with too many arguments` |

## Best practices

!!! success "Do"
    - Use descriptive labels that make the jump target obvious, such as `CLEANUP` or `RECOVER`.
    - For labels declared with [`:LABEL name;`](../keywords/LABEL.md), pass the matching target text such as `"LABEL CLEANUP"`.
    - Pass the target as a string literal. When the target depends on runtime data, choose among literal `Branch` calls with [`:IF`](../keywords/IF.md) or [`:BEGINCASE`](../keywords/BEGINCASE.md).
    - Prefer one shared cleanup or recovery label over repeating the same shutdown logic in several places.

!!! failure "Don't"
    - Pass plain label names such as `"CLEANUP"` for a normal [`:LABEL CLEANUP;`](../keywords/LABEL.md) target. The text must match the label exactly as written after the colon.
    - Change the case of the target text. `Branch("label cleanup")` does not match `:LABEL CLEANUP;`, and the script does not compile.
    - Pass a variable, parameter or expression as the target. A computed target never reaches a label. Use a string literal.
    - Use `Branch` as a substitute for ordinary [`:IF`](../keywords/IF.md), [`:FOR`](../keywords/FOR.md), [`:WHILE`](../keywords/WHILE.md), or [`:RETURN`](../keywords/RETURN.md) flow when structured control is sufficient.
    - Expect an error from a computed target. It falls through silently, so the jump is lost without any sign.

## Caveats

- Calling `Branch()` without a target stops the script from compiling, so no runtime error can be caught.
- For [`:LABEL name;`](../keywords/LABEL.md), the usual branch target is `"LABEL name"`. For mashed labels such as [`:LABELNAME;`](../keywords/LABEL.md), the target text must match that exact token text instead.
- A string-literal target that matches no label stops the script from compiling, so none of the script runs and no [`:TRY`](../keywords/TRY.md) can catch the failure. Matching is case-sensitive: a literal `Branch("label skip")` for [`:LABEL SKIP;`](../keywords/LABEL.md) fails the same way.
- A computed target never jumps, at script level or inside a procedure, even when its text exactly matches a label (verified on STARLIMS 12). Execution continues with the next statement, and no error is raised.
- An [`:ERROR`](../keywords/ERROR.md) handler can branch back to a label before `:ERROR`, so a retry loop works. Branching the other way, from the protected statements to a label inside the handler, raises a runtime error: `Exception has been thrown by the target of an invocation.`

## Examples

### Skip process steps based on condition

Jumps to `LABEL SKIP_PROCESS_STEPS` when validation fails, bypassing the registration step and landing directly at the shared exit label.

```ssl
:PROCEDURE SkipStepsIfValidationFails;
    :DECLARE nAge, bValid;

    nAge := 15;
    bValid := nAge >= 18;

    :IF .NOT. bValid;
        UsrMes("Validation failed");
        Branch("LABEL SKIP_PROCESS_STEPS");
    :ENDIF;

    UsrMes("Processing registration for age " + LimsString(nAge));
    :RETURN .T.;

    :LABEL SKIP_PROCESS_STEPS;
    UsrMes("Registration was skipped");
    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("SkipStepsIfValidationFails");
```

### Choose a target at run time with literal calls

Selects the jump from `sMode` with [`:IF`](../keywords/IF.md) blocks, each holding a string-literal target, instead of building the target text in a variable. With `sMode` set to `"REVIEW"`, the second `Branch` call jumps to the `REVIEW` label.

```ssl
:PROCEDURE RouteWorkflow;
    :DECLARE sMode;

    sMode := "REVIEW";

    :IF sMode == "RETRY";
        Branch("LABEL RETRY");
    :ENDIF;

    :IF sMode == "REVIEW";
        Branch("LABEL REVIEW");
    :ENDIF;

    UsrMes("Finishing the workflow");
    :RETURN "DONE";

    :LABEL RETRY;
    UsrMes("Retrying the workflow step");
    :RETURN "RETRY";

    :LABEL REVIEW;
    UsrMes("Reviewing the workflow before completion");
    :RETURN "REVIEW";
:ENDPROC;

/* Usage;
DoProc("RouteWorkflow");
```

[`UsrMes`](UsrMes.md) logs:

```text
Reviewing the workflow before completion
```

### Leave a TRY block for shared cleanup

Uses `Branch` inside a [`:TRY`](../keywords/TRY.md) block to jump to a shared cleanup label when an early-exit condition is detected, demonstrating that `Branch` exits the protected region before transferring control.

```ssl
:PROCEDURE SaveBatch;
    :DECLARE sBatchID, bCleanup, oErr;

    sBatchID := "";
    bCleanup := .F.;

    :TRY;
        :IF Empty(sBatchID);
            bCleanup := .T.;
            Branch("LABEL CLEANUP");
        :ENDIF;

        UsrMes("Saving batch " + sBatchID);
        :RETURN .T.;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes(oErr:Description);
        bCleanup := .T.;
    :ENDTRY;

    :LABEL CLEANUP;
    :IF bCleanup;
        UsrMes("Batch save aborted");
    :ENDIF;

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("SaveBatch");
```

## Related

- [`LABEL`](../keywords/LABEL.md)
- [`ERROR`](../keywords/ERROR.md)
