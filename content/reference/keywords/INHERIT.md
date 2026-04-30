---
title: "INHERIT"
summary: "Specifies the parent class for an SSL class."
id: ssl.keyword.inherit
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# INHERIT

Specifies the parent class for an SSL class.

!!! info "One class per script"
    SSL allows only one [`:CLASS`](CLASS.md) definition per script file. Use `:INHERIT` in the child class file, and define the parent class in a separate script.

Use `:INHERIT` immediately after [`:CLASS`](CLASS.md) `ClassName;` to make the new class derive from a parent class. The parent can be a plain class name or a qualified name such as `Category.ParentClass`, so the child class can inherit fields, methods, and inherited behavior from that parent. If `:INHERIT` is omitted, the class still inherits from the standard built-in base class.

The keyword can only appear directly after the class declaration, and only one parent class can be specified.

## Behavior

`:INHERIT` modifies a [`:CLASS`](CLASS.md) definition. The inherited class becomes the parent for member lookup, so child methods can use [`Base:MethodName()`](Base.md) to call inherited behavior and can access inherited fields through normal class member rules.

The keyword does not stand alone and is not used in script code outside a class definition.

## When to use

- When a new class should reuse fields or methods from an existing parent class.
- When a child class needs to override behavior and still call the parent implementation with [`Base:MethodName()`](Base.md).
- When several class scripts should share a common structure or API.

## Syntax

```ssl
:INHERIT ClassName;
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ClassName` | Identifier | Yes | The parent class to inherit from. This can be a plain name such as `BaseValidator` or a qualified name such as `Lab.BaseValidator`. |

## Keyword group

**Group:** Declarations
**Role:** modifier

## Best practices

!!! success "Do"
    - Place `:INHERIT` immediately after [`:CLASS`](CLASS.md) `ClassName;`.
    - Use a plain or qualified parent class name such as `BaseValidator` or `Lab.BaseValidator`.
    - Use [`Base:MethodName()`](Base.md) in child methods when you want to extend, not replace, inherited behavior.

!!! failure "Don't"
    - Put [`:DECLARE`](DECLARE.md) statements or methods before `:INHERIT` because SSL only accepts `:INHERIT` directly after the class declaration.
    - Use inheritance just to reach unrelated data or helper methods because it creates fragile class hierarchies.

## Caveats

- `:INHERIT` is valid only inside a [`:CLASS`](CLASS.md) definition.
- SSL keywords are case-sensitive, so write `:INHERIT` in uppercase.

## Examples

### Creating a derived class for shared validation logic

Reuses a parent method from a child class. With `sSampleId` set to `""`, the validation fails and the error message is displayed.

Base class script:

```ssl
:CLASS ValidationBase;
:DECLARE sFieldName, sValue;

:PROCEDURE SetField;
    :PARAMETERS sName, sVal;

    sFieldName := sName;
    sValue := sVal;
:ENDPROC;

:PROCEDURE IsBlank;
    :RETURN Empty(sValue);
:ENDPROC;

:PROCEDURE Constructor;
:ENDPROC;
```

Derived class script:

```ssl
:CLASS SampleValidator;
:INHERIT ValidationBase;
:DECLARE sSampleId;

:PROCEDURE ValidateId;
    :DECLARE bBlank;

    Me:SetField("SampleID", sSampleId);
    bBlank := Me:IsBlank();

    :IF bBlank;
        :RETURN "SampleID is required";
    :ENDIF;

    :RETURN "";
:ENDPROC;

:PROCEDURE Constructor;
    sSampleId := "";
:ENDPROC;
```

Usage:

```ssl
:PROCEDURE RunValidation;
    :DECLARE oVal, sResult;

    oVal := CreateUdObject("SampleValidator");
    oVal:sSampleId := "";
    sResult := oVal:ValidateId();

    :IF !Empty(sResult);
        UsrMes(sResult);
    :ENDIF;

    :RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("RunValidation");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
SampleID is required
```

### Specializing a base report class

Overrides a parent method and still calls the parent implementation via [`Base:`](Base.md). The derived constructor sets the title and compliance values; `GetHeader` extends the base header with standard and limit details.

Base class script:

```ssl
:CLASS BaseReport;
:DECLARE sTitle;

:PROCEDURE GetHeader;
    :RETURN "Report: " + sTitle;
:ENDPROC;

:PROCEDURE Constructor;
    sTitle := "Generic Report";
:ENDPROC;
```

Derived class script:

```ssl
:CLASS EnvReport;
:INHERIT BaseReport;

:DECLARE nContaminantLimit, sRegStandard;

:PROCEDURE GetHeader;
    :DECLARE sHeader;

    sHeader := Base:GetHeader();
    sHeader := sHeader + " | Standard: " + sRegStandard;
    sHeader := sHeader + " | Limit: " + LimsString(nContaminantLimit) + " ppm";

    :RETURN sHeader;
:ENDPROC;

:PROCEDURE Constructor;
    sTitle := "Environmental Compliance";
    nContaminantLimit := 50;
    sRegStandard := "EPA-2018";
:ENDPROC;
```

Usage:

```ssl
:PROCEDURE ShowReportHeader;
    :DECLARE oReport;

    oReport := CreateUdObject("EnvReport");
    UsrMes(oReport:GetHeader());
:ENDPROC;

/* Usage;
DoProc("ShowReportHeader");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Report: Environmental Compliance | Standard: EPA-2018 | Limit: 50 ppm
```

### Building a polymorphic workflow hierarchy

Demonstrates multiple child classes sharing a parent interface. Each workflow implements `Execute` differently; the caller iterates both through the same loop.

Parent class script:

```ssl
:CLASS Workflow;
:DECLARE sWorkflowName, sStatus;

:PROCEDURE Execute;
    :RETURN sStatus;
:ENDPROC;

:PROCEDURE GetStatus;
    :RETURN sStatus;
:ENDPROC;

:PROCEDURE GetName;
    :RETURN sWorkflowName;
:ENDPROC;

:PROCEDURE Constructor;
    sWorkflowName := "Base Workflow";
    sStatus := "Initialized";
:ENDPROC;
```

First derived class script:

```ssl
:CLASS ApprovalWorkflow;
:INHERIT Workflow;
:DECLARE aApprovers, nCurrentStep;

:PROCEDURE Execute;
    :DECLARE sApprover;

    :IF nCurrentStep <= ALen(aApprovers);
        sApprover := aApprovers[nCurrentStep];
        sStatus := "Awaiting " + sApprover;
        nCurrentStep += 1;
        :RETURN sStatus;
    :ENDIF;

    sStatus := "All approvals received";

    :RETURN sStatus;
:ENDPROC;

:PROCEDURE Constructor;
    sWorkflowName := "Approval Workflow";
    aApprovers := {"Supervisor", "Manager", "Director"};
    nCurrentStep := 1;
    sStatus := "Pending approval";
:ENDPROC;
```

Second derived class script:

```ssl
:CLASS NotificationWorkflow;
:INHERIT Workflow;
:DECLARE nSentCount;

:PROCEDURE Execute;
    nSentCount += 1;

    :IF nSentCount >= 3;
        sStatus := "All notifications sent";
        :RETURN sStatus;
    :ENDIF;

    sStatus := "Sending notification " + LimsString(nSentCount);

    :RETURN sStatus;
:ENDPROC;

:PROCEDURE Constructor;
    sWorkflowName := "Notification Workflow";
    nSentCount := 0;
    sStatus := "Pending notification";
:ENDPROC;
```

Usage:

```ssl
:PROCEDURE RunPolymorphicWorkflow;
    :DECLARE oWorkflow, aWorkflows, nOuter, nInner, sStatus;

    aWorkflows := {
        CreateUdObject("ApprovalWorkflow"),
        CreateUdObject("NotificationWorkflow")
    };

    :FOR nOuter := 1 :TO ALen(aWorkflows);
        oWorkflow := aWorkflows[nOuter];
        UsrMes("Running workflow: " + oWorkflow:GetName());
        /* Displays the current workflow name;

        :FOR nInner := 1 :TO 5;
            sStatus := oWorkflow:Execute();

            :IF sStatus == "All approvals received"
                .OR. sStatus == "All notifications sent";
                :EXITFOR;
            :ENDIF;
        :NEXT;

        UsrMes("Final status: " + oWorkflow:GetStatus());
        /* Displays the final workflow status;
    :NEXT;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("RunPolymorphicWorkflow");
```

## Related

- [`CLASS`](CLASS.md)
- [`Base:`](Base.md)
- [`Me:`](Me.md)
