---
title: "constructor"
summary: "Runs one-time class initialization code when a user-defined class instance is created."
id: ssl.special_form.constructor
element_type: special_form
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# constructor

## What it does

Runs one-time class initialization code when a user-defined class instance is created.

Use `Constructor` to set initial field values, validate incoming arguments, and prepare an object before any other instance method runs. It is a reserved constructor declaration name inside [`:CLASS`](../keywords/CLASS.md), not a normal method name. If a class does not declare a constructor, SSL generates a default parameterless constructor.

When `CreateUdObject("ClassName")` or `CreateUdObject("ClassName", {args})` creates a user-defined class instance, SSL runs that class's constructor automatically. Before the constructor body runs, SSL also emits a call to the base class's parameterless constructor. Constructors cannot return values.

Because `Constructor` is a special declaration form, it cannot be called as a
normal method from SSL code.

## When to use it

- When every new instance must start with a known valid state.
- When constructor arguments need validation before the object is used.
- When setup logic belongs with the class instead of being repeated at each call site.

!!! info "One class per script"
    SSL allows only one [`:CLASS`](../keywords/CLASS.md) definition per script file. If your design requires multiple related classes, each class must live in its own script.

## Syntax

Declare the constructor as `:PROCEDURE Constructor;` inside a [`:CLASS`](../keywords/CLASS.md) block. If it accepts arguments, declare them with [`:PARAMETERS`](../keywords/PARAMETERS.md) inside the body.

```ssl
:CLASS MyClass;

:PROCEDURE Constructor;
    /* Initialization code;
:ENDPROC;
```

```ssl
:CLASS MyClass;

:PROCEDURE Constructor;
    :PARAMETERS sName, nValue;

    /* Initialization code using sName and nValue;
:ENDPROC;
```

Create user-defined class instances with [`CreateUdObject`](../functions/CreateUdObject.md), not curly-brace construction:

```ssl
oItem := CreateUdObject("MyClass");
oItem := CreateUdObject("MyClass", {"Sample-001", 42});
```

## Context rules

`Constructor` can only be declared inside a [`:CLASS`](../keywords/CLASS.md) block. Using it outside a class does not produce a valid procedure declaration. Inside a constructor, `:RETURN;` is allowed as an early exit, but `:RETURN value;` is a compile-time error.

SSL automatically emits a call to the base class's parameterless constructor before the constructor body executes. You do not need to call `Base:Constructor()` when the base constructor takes no arguments. If you need to invoke a base constructor that takes parameters, call `Base:Constructor(args)` explicitly. The explicit call passes the arguments that the auto-call cannot.

## Notes for daily SSL work

!!! success "Do"
    - Keep constructor work focused on initialization and input validation.
    - Initialize fields that later methods depend on.
    - Fail early when required constructor arguments are missing or invalid.

!!! failure "Don't"
    - Instantiate a user-defined class with `MyClass{}`. That brace form is for built-in classes, not [`:CLASS`](../keywords/CLASS.md) files.
    - Call `Base:Constructor()` when the base constructor is parameterless. SSL already emits that call automatically.
    - Return a value from a constructor. `:RETURN value;` is a compile-time error.

## Errors and edge cases

- `Constructor` is meaningful only as the fixed constructor declaration name inside [`:CLASS`](../keywords/CLASS.md).
- `:RETURN value;` inside a constructor causes a compile-time error.
- Constructors run during object creation; they are not invoked like ordinary
  methods.
- If no constructor is declared, SSL provides an implicit parameterless one.

## Examples

### Basic property initialization

Sets `nCount` to zero in the constructor so every new `SampleCounter` instance starts from a known state. Calling `Increment()` twice and then `GetCount()` returns 2.

Class script:

```ssl
:CLASS SampleCounter;

:DECLARE nCount;

:PROCEDURE Constructor;
    nCount := 0;
:ENDPROC;

:PROCEDURE Increment;
    nCount += 1;
:ENDPROC;

:PROCEDURE GetCount;
    :RETURN nCount;
:ENDPROC;
```

Usage:

```ssl
:DECLARE oCounter, sMessage;

oCounter := CreateUdObject("SampleCounter");
oCounter:Increment();
oCounter:Increment();

sMessage := "Count: " + LimsString(oCounter:GetCount());
UsrMes(sMessage);
```

`UsrMes` displays:

```text
Count: 2
```

### Constructor with parameters and validation

Accepts `sId` and `sInitialStatus`. If `sId` is empty the constructor raises an error. If `sInitialStatus` is empty it defaults to `"PENDING"`.

Class script:

```ssl
:CLASS Sample;

:DECLARE sSampleId, sStatus;

:PROCEDURE Constructor;
    :PARAMETERS sId, sInitialStatus;

    :IF Empty(sId);
        RaiseError("Sample ID is required");
    :ENDIF;

    sSampleId := sId;

    :IF Empty(sInitialStatus);
        sStatus := "PENDING";
    :ELSE;
        sStatus := sInitialStatus;
    :ENDIF;
:ENDPROC;

:PROCEDURE GetSummary;
    :RETURN sSampleId + " (" + sStatus + ")";
:ENDPROC;
```

Usage:

```ssl
:DECLARE oSample;

oSample := CreateUdObject("Sample", {"S-001", "ACTIVE"});
UsrMes(oSample:GetSummary());

oSample := CreateUdObject("Sample", {"S-002"});
UsrMes(oSample:GetSummary());
```

`UsrMes` displays:

```text
S-001 (ACTIVE)
S-002 (PENDING)
```

### Derived constructor with automatic base initialization

`AuditCounter` inherits from `CounterBase`. SSL automatically calls the base parameterless constructor, which sets `nCount := 10`, before the derived constructor body runs. The derived constructor only needs to set its own field `sLabel`.

Parent class script:

```ssl
:CLASS CounterBase;

:DECLARE nCount;

:PROCEDURE Constructor;
    nCount := 10;
:ENDPROC;

:PROCEDURE GetCount;
    :RETURN nCount;
:ENDPROC;
```

Derived class script:

```ssl
:CLASS AuditCounter;
:INHERIT Lab:CounterBase;

:DECLARE sLabel;

:PROCEDURE Constructor;
    :PARAMETERS sValue;

    sLabel := sValue;
:ENDPROC;

:PROCEDURE GetSummary;
    :RETURN sLabel + ": " + LimsString(Me:GetCount());
:ENDPROC;
```

Usage:

```ssl
:DECLARE oCounter;

oCounter := CreateUdObject("AuditCounter", {"Batch A"});
UsrMes(oCounter:GetSummary());
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Batch A: 10
```

## Related elements

- [`CreateUdObject`](../functions/CreateUdObject.md)
- [`me`](me.md)
- [`base`](base.md)
- [`CLASS`](../keywords/CLASS.md)
- [`INHERIT`](../keywords/INHERIT.md)
