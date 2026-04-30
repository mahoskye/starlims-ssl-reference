---
title: "CLASS"
summary: "Defines a class in SSL. A class file can declare fields, methods, an optional base class, and a Constructor procedure for instance initialization."
id: ssl.keyword.class
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CLASS

Defines a class in SSL. A class file can declare fields, methods, an optional base class, and a `Constructor` procedure for instance initialization.

!!! info "One class per script"
    A file is either a class file or a script file. A `:CLASS` definition runs to end-of-file, so each class must live in its own script.

The `:CLASS` keyword starts a class definition. After `:CLASS`, you can add an optional [`:INHERIT`](INHERIT.md) line, one or more [`:DECLARE`](DECLARE.md) field declarations, regular methods defined with [`:PROCEDURE`](PROCEDURE.md), and an optional [`Constructor`](../special-forms/constructor.md) declared as `:PROCEDURE Constructor;`. If [`:INHERIT`](INHERIT.md) is omitted, the class inherits from the built-in base object automatically. If you omit the constructor, SSL creates an empty zero-argument constructor for you. There is no `:ENDCLASS` keyword; the class continues to the end of the file.

Use [`CreateUdObject`](../functions/CreateUdObject.md) to instantiate a user-defined class. Inside class methods, call sibling methods with [`Me:MethodName()`](../special-forms/me.md) and inherited methods with [`Base:MethodName()`](../special-forms/base.md).

## Behavior

`:CLASS` changes the file into class context. After the class declaration, SSL accepts an optional [`:INHERIT`](INHERIT.md), then field declarations and method definitions. The class body is not closed by another keyword; it ends only at end-of-file.

Class fields are declared with [`:DECLARE`](DECLARE.md) in the class body and are available to class methods. Methods are defined with [`:PROCEDURE`](PROCEDURE.md) ... [`:ENDPROC`](ENDPROC.md) just like script procedures, but inside a class they are invoked through the instance, for example `oSample:GetSummary()` or `Me:GetSummary()`.

Constructors use the reserved declaration name [`Constructor`](../special-forms/constructor.md). A constructor may take parameters, but it cannot return a value. If no constructor is declared, SSL generates an empty zero-argument constructor automatically.

## When to use

- When you need to keep related state and behavior together in one reusable type.
- When several operations should share the same fields across multiple methods.
- When you want to extend another SSL class with [`:INHERIT`](INHERIT.md).
- When object-style code is clearer than passing many separate values between procedures.

## Syntax

```ssl
:CLASS ClassName;
```

```ssl
:CLASS ClassName;
:INHERIT category.scriptname;
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ClassName` | Identifier | No | Name of the class. SSL permits `:CLASS;`, but reviewed code should provide an explicit class name. |

## Keyword group

**Group:** Procedures & Classes
**Role:** opener

## Best practices

!!! success "Do"
    - Put [`:INHERIT`](INHERIT.md) immediately after `:CLASS` when the class derives from
      another class.
    - Keep class fields in [`:DECLARE`](DECLARE.md) statements near the top of the file so
      the object shape is easy to read.
    - Place regular methods before [`Constructor`](../special-forms/constructor.md) and keep the constructor last for predictable structure.
    - Instantiate user-defined classes with [`CreateUdObject`](../functions/CreateUdObject.md) instead of built-in-class curly-brace syntax.
    - Use [`Me:`](../special-forms/me.md) for sibling method calls and [`Base:`](../special-forms/base.md) for inherited behavior inside class methods.

!!! failure "Don't"
    - Mix script logic and a class definition in the same file. `:CLASS` runs
      to end-of-file, so the file must stay class-only.
    - Use `ClassName{}` syntax for a user-defined class — that pattern targets
      built-in class construction rules.
    - Return a value from [`Constructor`](../special-forms/constructor.md). SSL treats that as a compile-time error.
    - Split related fields across method bodies. Declaring them in the class body makes the instance state clear and consistent.

## Caveats

- Members whose names start with `_` are excluded from reflection-based access.

## Examples

### Define a simple class and instantiate it

Create a class with fields, a regular method, and a constructor that receives initial values. `GetDescription` returns a formatted string built from the instance fields.

Class definition:

```ssl
:CLASS SampleAnalyzer;

:DECLARE sSampleName, nResultValue;

:PROCEDURE GetDescription;
    :DECLARE sDescription;

    sDescription := "Sample " + sSampleName + ": "
			        + LimsString(nResultValue);

    :RETURN sDescription;
:ENDPROC;

:PROCEDURE Constructor;
    :PARAMETERS sName, nValue;

    sSampleName := sName;
    nResultValue := nValue;
:ENDPROC;
```

Usage:

```ssl
:DECLARE oAnalyzer, sSummary;

oAnalyzer := CreateUdObject("SampleAnalyzer", {"SAM-001", 42});
sSummary := oAnalyzer:GetDescription();

UsrMes(sSummary);
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Sample SAM-001: 42
```

### Inherit from a base class and extend its behavior

Use [`:INHERIT`](INHERIT.md) in the derived class and call the parent implementation with `Base:`. The derived `GetSummary` appends a result value to the base summary.

Base class script:

```ssl
:CLASS LabSample;

:DECLARE sSampleId, sStatus;

:PROCEDURE GetSummary;
    :RETURN "Sample " + sSampleId + " is " + sStatus;
:ENDPROC;

:PROCEDURE Constructor;
    :PARAMETERS sId, sState;

    sSampleId := sId;
    sStatus := sState;
:ENDPROC;
```

Derived class script:

```ssl
:CLASS QcSample;
:INHERIT LabSample;

:DECLARE nResultValue;

:PROCEDURE GetSummary;
    :DECLARE sSummary;

    sSummary := Base:GetSummary();
    sSummary := sSummary + ", result " + LimsString(nResultValue);

    :RETURN sSummary;
:ENDPROC;

:PROCEDURE Constructor;
    :PARAMETERS sId, sState, nResult;

    sSampleId := sId;
    sStatus := sState;
    nResultValue := nResult;
:ENDPROC;
```

Usage:

```ssl
:DECLARE oSample;

oSample := CreateUdObject("QcSample", {"SAM-002", "Logged", 98.6});
UsrMes(oSample:GetSummary());
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Sample SAM-002 is Logged, result 98.6
```

### Coordinate several class methods through [`Me:`](../special-forms/me.md)

Use a class to manage state across multiple operations instead of passing many separate values between procedures. `LoadAndReport` delegates to `AddResult` via [`Me:`](../special-forms/me.md) and returns the accumulated summary.

Class definition:

```ssl
:CLASS ResultTracker;

:DECLARE aValues, nPassCount, nFailCount;

:PROCEDURE AddResult;
    :PARAMETERS nValue, nLimit;

    AAdd(aValues, nValue);

    :IF nValue >= nLimit;
        nPassCount += 1;
    :ELSE;
        nFailCount += 1;
    :ENDIF;
:ENDPROC;

:PROCEDURE GetSummary;
    :DECLARE sSummary;

    sSummary := "Runs: " + LimsString(ALen(aValues));
    sSummary := sSummary + ", pass: " + LimsString(nPassCount);
    sSummary := sSummary + ", fail: " + LimsString(nFailCount);

    :RETURN sSummary;
:ENDPROC;

:PROCEDURE LoadAndReport;
    :PARAMETERS aInputValues, nLimit;
    :DECLARE nIndex;

    :FOR nIndex := 1 :TO ALen(aInputValues);
        Me:AddResult(aInputValues[nIndex], nLimit);
    :NEXT;

    :RETURN Me:GetSummary();
:ENDPROC;

:PROCEDURE Constructor;
    aValues := {};
    nPassCount := 0;
    nFailCount := 0;
:ENDPROC;
```

Usage:

```ssl
:DECLARE oTracker, sReport;

oTracker := CreateUdObject("ResultTracker");
sReport := oTracker:LoadAndReport({95, 102, 88, 110}, 90);

UsrMes(sReport);
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Runs: 4, pass: 3, fail: 1
```

## Related

- [`INHERIT`](INHERIT.md)
- [`Me:`](../special-forms/me.md)
- [`Base:`](../special-forms/base.md)
- [`DECLARE`](DECLARE.md)
- [`PROCEDURE`](PROCEDURE.md)
- [`constructor`](../special-forms/constructor.md)
