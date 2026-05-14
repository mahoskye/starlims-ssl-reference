---
title: "INHERIT"
summary: "Specifies the parent class for an SSL class."
id: ssl.keyword.inherit
element_type: keyword
doc_status: published
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

`:INHERIT` modifies a [`:CLASS`](CLASS.md) definition. The inherited class becomes the parent for member lookup, so child methods can use [`Base:MethodName()`](../special-forms/base.md) to call inherited behavior and can read or write inherited fields with [`Base:fieldName`](../special-forms/base.md). Inside any class method, a bare identifier refers to a local or [`:PARAMETERS`](PARAMETERS.md) entry — class-level fields declared in the child must be qualified with [`Me:`](../special-forms/me.md), and fields declared on the parent must be qualified with [`Base:`](../special-forms/base.md).

The keyword does not stand alone and is not used in script code outside a class definition.

## When to use

- When a new class should reuse fields or methods from an existing parent class.
- When a child class needs to override behavior and still call the parent implementation with [`Base:MethodName()`](../special-forms/base.md).
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
    - Use [`Base:MethodName()`](../special-forms/base.md) in child methods when you want to extend, not replace, inherited behavior.

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

    Me:sFieldName := sName;
    Me:sValue := sVal;
:ENDPROC;

:PROCEDURE IsBlank;
    :RETURN Empty(Me:sValue);
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

    Me:SetField("SampleID", Me:sSampleId);
    bBlank := Me:IsBlank();

    :IF bBlank;
        :RETURN "SampleID is required";
    :ENDIF;

    :RETURN "";
:ENDPROC;

:PROCEDURE Constructor;
    Me:sSampleId := "";
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

Overrides a parent method and still calls the parent implementation via [`Base:`](../special-forms/base.md). The derived constructor sets the title and compliance values; `GetHeader` extends the base header with standard and limit details.

Base class script:

```ssl
:CLASS BaseReport;
:DECLARE sTitle;

:PROCEDURE GetHeader;
    :RETURN "Report: " + Me:sTitle;
:ENDPROC;

:PROCEDURE Constructor;
    Me:sTitle := "Generic Report";
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
    sHeader := sHeader + " | Standard: " + Me:sRegStandard;
    sHeader := sHeader + " | Limit: " + LimsString(Me:nContaminantLimit) + " ppm";

    :RETURN sHeader;
:ENDPROC;

:PROCEDURE Constructor;
    Me:sTitle := "Environmental Compliance";
    Me:nContaminantLimit := 50;
    Me:sRegStandard := "EPA-2018";
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
    :RETURN Me:sStatus;
:ENDPROC;

:PROCEDURE GetStatus;
    :RETURN Me:sStatus;
:ENDPROC;

:PROCEDURE GetName;
    :RETURN Me:sWorkflowName;
:ENDPROC;

:PROCEDURE Constructor;
    Me:sWorkflowName := "Base Workflow";
    Me:sStatus := "Initialized";
:ENDPROC;
```

First derived class script:

```ssl
:CLASS ApprovalWorkflow;
:INHERIT Workflow;
:DECLARE aApprovers, nCurrentStep;

:PROCEDURE Execute;
    :DECLARE sApprover;

    :IF Me:nCurrentStep <= ALen(Me:aApprovers);
        sApprover := Me:aApprovers[Me:nCurrentStep];
        Me:sStatus := "Awaiting " + sApprover;
        Me:nCurrentStep += 1;
        :RETURN Me:sStatus;
    :ENDIF;

    Me:sStatus := "All approvals received";

    :RETURN Me:sStatus;
:ENDPROC;

:PROCEDURE Constructor;
    Me:sWorkflowName := "Approval Workflow";
    Me:aApprovers := {"Supervisor", "Manager", "Director"};
    Me:nCurrentStep := 1;
    Me:sStatus := "Pending approval";
:ENDPROC;
```

Second derived class script:

```ssl
:CLASS NotificationWorkflow;
:INHERIT Workflow;
:DECLARE nSentCount;

:PROCEDURE Execute;
    Me:nSentCount += 1;

    :IF Me:nSentCount >= 3;
        Me:sStatus := "All notifications sent";
        :RETURN Me:sStatus;
    :ENDIF;

    Me:sStatus := "Sending notification " + LimsString(Me:nSentCount);

    :RETURN Me:sStatus;
:ENDPROC;

:PROCEDURE Constructor;
    Me:sWorkflowName := "Notification Workflow";
    Me:nSentCount := 0;
    Me:sStatus := "Pending notification";
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
- [`Base:`](../special-forms/base.md)
- [`Me:`](../special-forms/me.md)
