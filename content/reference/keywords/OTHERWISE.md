---
title: "OTHERWISE"
summary: "Executes the default branch of a :BEGINCASE block when no earlier :CASE branch runs."
id: ssl.keyword.otherwise
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# OTHERWISE

Executes the default branch of a [`:BEGINCASE`](BEGINCASE.md) block when no earlier [`:CASE`](CASE.md) branch runs.

## Behavior

Use `:OTHERWISE` inside [`:BEGINCASE`](BEGINCASE.md) after one or more [`:CASE`](CASE.md) branches to handle the fallback path. It does not take an expression. Its body runs only when no earlier [`:CASE`](CASE.md) condition evaluated to [`.T.`](../literals/true.md).

`:OTHERWISE` is optional, but when it is present it must appear after all [`:CASE`](CASE.md) branches and before [`:ENDCASE`](ENDCASE.md). If no [`:CASE`](CASE.md) branch runs and there is no `:OTHERWISE` branch, execution continues after [`:ENDCASE`](ENDCASE.md) with no fallback action.

## When to use

- When a [`:BEGINCASE`](BEGINCASE.md) block needs a fallback path for inputs that do not match any [`:CASE`](CASE.md) condition.
- When unmatched values require a defined action, error message, or default behavior.
- When you want to catch unexpected inputs and log them or route them to a default handler.

## Syntax

```ssl
:OTHERWISE;
```

## Keyword group

**Group:** Control Flow
**Role:** default branch

## Best practices

!!! success "Do"
    - Add an `:OTHERWISE` branch when unmatched inputs still need defined behavior.
    - Keep `:OTHERWISE` after all [`:CASE`](CASE.md) branches and usually end its body with `:EXITCASE;` for consistency with the rest of the [`:BEGINCASE`](BEGINCASE.md) block.

!!! failure "Don't"
    - Put `:OTHERWISE` before a later [`:CASE`](CASE.md) branch or outside a [`:BEGINCASE`](BEGINCASE.md) block.
    - Use `:OTHERWISE` as a substitute for a missing condition when a normal [`:CASE`](CASE.md) branch would describe the logic more clearly.

## Caveats

- [`:BEGINCASE`](BEGINCASE.md) requires at least one [`:CASE`](CASE.md) branch before `:OTHERWISE` can appear.
- A [`:BEGINCASE`](BEGINCASE.md) block can contain at most one `:OTHERWISE` branch.
- Keywords are case-sensitive, so write `:OTHERWISE` in uppercase.

## Examples

### Providing a fallback status message

Shows how `:OTHERWISE` handles a status string that matches none of the listed [`:CASE`](CASE.md) conditions. With `sStatus` set to `"Draft"` or `"Approved"`, a matching branch runs; with `"UNKNOWN"`, no branch matches and `:OTHERWISE` provides the fallback.

```ssl
:PROCEDURE ShowDocumentStatus;
    :PARAMETERS sStatus;
    :DECLARE sMessage;

    :BEGINCASE;
    :CASE sStatus == "Draft";
        sMessage := "Document is still in draft";
        InfoMes(sMessage);
        :EXITCASE;
    :CASE sStatus == "Approved";
        sMessage := "Document is approved";
        InfoMes(sMessage);
        :EXITCASE;
    :OTHERWISE;
        sMessage := "Document status is not recognized: " + sStatus;
        UsrMes(sMessage);  /* Displays fallback status for unmatched input;
        :EXITCASE;
    :ENDCASE;
:ENDPROC;

/* Usage;
DoProc("ShowDocumentStatus", {"UNKNOWN"});
```

### Routing unmatched work to a support queue

Routes workflow tasks to a specialized team based on task type. With `oTask:Type` set to `"PATHOLOGY"`, no specific team matches and `:OTHERWISE` routes the task to general support.

```ssl
:PROCEDURE RouteWorkflowTask;
    :PARAMETERS oTask;
    :DECLARE sTaskType, sAssignedGroup, sLogMsg;

    sTaskType := Upper(oTask:Type);

    :BEGINCASE;
    :CASE sTaskType == "CHEMISTRY";
        sAssignedGroup := "Chemistry Lab Team";
        DoProc("NotifyChemistryTeam", {oTask});
        :EXITCASE;
    :CASE sTaskType == "MICROBIOLOGY";
        sAssignedGroup := "Micro Lab Team";
        DoProc("NotifyMicroTeam", {oTask});
        :EXITCASE;
    :CASE sTaskType == "CALIBRATION";
        sAssignedGroup := "Instrumentation Team";
        DoProc("NotifyInstrumentTeam", {oTask});
        :EXITCASE;
    :OTHERWISE;
        sAssignedGroup := "General Support Group";
        DoProc("NotifySupportTeam", {oTask});
        sLogMsg := "Task type " + sTaskType + " was routed to general support";
        UsrMes(sLogMsg);
        /* Displays fallback routing message for unmatched task types;
        :EXITCASE;
    :ENDCASE;

    oTask:AssignedGroup := sAssignedGroup;

    :RETURN sAssignedGroup;
:ENDPROC;

/* Usage;
:DECLARE oTask;
oTask := CreateLocal();
oTask:Type := "PATHOLOGY";
DoProc("RouteWorkflowTask", {oTask});
```

### Applying a policy fallback after multi-condition checks

Resolves a release action from role, workflow stage, and override flag. With `sUserRole` set to `"TECHNICIAN"` and `sStage` set to `"REVIEW"`, no specific combination matches and `:OTHERWISE` escalates the action.

```ssl
:PROCEDURE ResolveReleaseAction;
    :PARAMETERS sUserRole, sStage, bHasOverride;
    :DECLARE sAction, sAuditMsg;

    sUserRole := Upper(sUserRole);
    sStage := Upper(sStage);

    :BEGINCASE;
    :CASE sUserRole == "ADMIN";
        sAction := "APPROVE";
        :EXITCASE;
    :CASE sUserRole == "SUPERVISOR" .AND. sStage == "REVIEW";
        sAction := "APPROVE";
        :EXITCASE;
    :CASE sUserRole == "ANALYST" .AND. sStage == "DRAFT" .AND. bHasOverride;
        sAction := "SUBMIT_FOR_REVIEW";
        :EXITCASE;
    :OTHERWISE;
        sAction := "ESCALATE";
        sAuditMsg := "Unhandled role/stage combination: " + sUserRole + "/" + sStage;
        UsrMes(sAuditMsg);
        /* Displays escalation message for an unmatched role and stage;
        :EXITCASE;
    :ENDCASE;

    :RETURN sAction;
:ENDPROC;

/* Usage;
DoProc("ResolveReleaseAction", {"TECHNICIAN", "REVIEW", .F.});
```

## Related

- [`BEGINCASE`](BEGINCASE.md)
- [`CASE`](CASE.md)
- [`EXITCASE`](EXITCASE.md)
- [`ENDCASE`](ENDCASE.md)
