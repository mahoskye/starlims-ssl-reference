---
title: "Branch"
summary: "Transfers control to a label in the current procedure."
id: ssl.function.branch
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Branch

Transfers control to a label in the current procedure.

`Branch` requires exactly one argument. If that argument is a string literal, SSL uses that literal text as the branch target. If it is any other expression, SSL evaluates it, converts the result to a string, and compares that text against the labels registered in the current procedure. If a computed target does not match any label, execution continues with the next statement.

For normal label declarations such as [`:LABEL CLEANUP;`](label.md), the target text must match the stored label text, so the usual form is `Branch("LABEL CLEANUP")`. Forward references are supported within the same procedure because labels are collected before code generation. When `Branch` is used inside a [`:TRY`](../keywords/TRY.md) or [`:CATCH`](../keywords/CATCH.md) region, SSL leaves that protected region before transferring control.
`Branch` does not return a useful value.

## When to use

- When you need to jump to a shared cleanup or recovery section in the same procedure.
- When maintaining legacy SSL that already uses labels for explicit control flow.
- When a fixed or computed label target is clearer than duplicating the same exit logic in several places.

## Syntax

```ssl
Branch(vTarget)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vTarget` | any | yes | — | Target label text. A string literal is used directly as the target text. Any other expression is evaluated and converted to a string before SSL compares it to the labels registered in the current procedure. |

## Returns

**NIL** — Does not return a value for application logic. Redirects control flow when a matching label is found.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| More than one argument is provided. | `Branch with too many arguments` |
| The branch target argument is missing. | `Branch target missing` |

## Best practices

!!! success "Do"
    - Use descriptive labels that make the jump target obvious, such as `CLEANUP` or `RECOVER`.
    - For labels declared with [`:LABEL name;`](label.md), pass the matching target text such as `"LABEL CLEANUP"`.
    - Prefer one shared cleanup or recovery label over repeating the same shutdown logic in several places.

!!! failure "Don't"
    - Pass plain label names such as `"CLEANUP"` for a normal [`:LABEL CLEANUP;`](label.md) target. The text must match the stored label name exactly.
    - Use `Branch` as a substitute for ordinary [`:IF`](../keywords/IF.md), [`:FOR`](../keywords/FOR.md), [`:WHILE`](../keywords/WHILE.md), or [`:RETURN`](../keywords/RETURN.md) flow when structured control is sufficient.
    - Assume a computed target will raise an error when it does not match. A computed miss simply falls through to the next statement.

## Caveats

- For [`:LABEL name;`](label.md), the usual branch target is `"LABEL name"`. For mashed labels such as [`:LABELNAME;`](label.md), the target text must match that exact token text instead.

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

DoProc("SkipStepsIfValidationFails");
```

### Use a computed target

Builds the branch target string dynamically based on `sMode` and shows that the computed value `"LABEL REVIEW"` routes execution to the `REVIEW` label.

```ssl
:PROCEDURE RouteWorkflow;
    :DECLARE sMode, sTarget;

    sMode := "REVIEW";
    sTarget := "LABEL FINISH";

    :IF sMode == "RETRY";
        sTarget := "LABEL RETRY";
    :ENDIF;

    :IF sMode == "REVIEW";
        sTarget := "LABEL REVIEW";
    :ENDIF;

    Branch(sTarget);

    UsrMes("No matching label was found");
    :RETURN "NONE";

    :LABEL RETRY;
    UsrMes("Retrying the workflow step");
    :RETURN "RETRY";

    :LABEL FINISH;
    UsrMes("Finishing the workflow");
    :RETURN "DONE";

    :LABEL REVIEW;
    UsrMes("Reviewing the workflow before completion");
    :RETURN "REVIEW";
:ENDPROC;

DoProc("RouteWorkflow");
```

### Leave a TRY block for shared cleanup

Uses `Branch` inside a [`:TRY`](../keywords/TRY.md) block to jump to a shared cleanup label when an early-exit condition is detected, demonstrating that `Branch` exits the protected region before transferring control.

```ssl
:PROCEDURE SaveBatch;
    :DECLARE sBatchID, bCleanup, oErr;

    sBatchID := "B-100";
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

DoProc("SaveBatch");
```

## Related

- [`LABEL`](../keywords/LABEL.md)
