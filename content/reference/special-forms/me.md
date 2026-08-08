---
title: "Me:"
summary: "Provides a reference to the current class instance inside :CLASS methods."
id: ssl.special_form.me
element_type: special_form
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Me:

## What it does

Provides a reference to the current class instance inside [`:CLASS`](../keywords/CLASS.md) methods.

Use `Me` when code in a class method needs to read or write the current instance's fields, or call another method on the same object. `Me:MemberName` resolves against the current class first. If a field is not found there, member lookup falls back to inherited members. For method calls, the target method must exist or compilation fails.

!!! warning "`Me:` is required for class-field access"
    A bare identifier inside a class method always refers to a local variable or [`:PARAMETERS`](../keywords/PARAMETERS.md) entry, never to a class-level [`:DECLARE`](../keywords/DECLARE.md) field. To read or write an instance field — including inside `Constructor` — you must write `Me:fieldName`. Use [`Base:fieldName`](base.md) for a field declared on the parent class. Compound assignments (`+=`, `-=`, etc.) need the same qualification.

`Me` evaluates to the current instance of the class where the code is running. `Me:FieldName` resolves against the current class first, then falls back to inherited members when needed. `Me:MethodName()` calls a method on the same instance, which is the normal way to invoke sibling methods from inside class code. `Me` is case-insensitive, but examples and new code should use the canonical `Me` form.

## When to use it

- When you need to access or modify a field of the current object from within a class method.
- When invoking another method on the same instance, especially if polymorphic or overridden behavior is expected.
- When you need to disambiguate between a local variable and an instance field that share the same name.

## Syntax

```ssl
Me;
Me:FieldName;
Me:MethodName(args)
```

## Context rules

`Me` is valid only inside methods that belong to a [`:CLASS`](../keywords/CLASS.md) definition, including `Constructor`. It is not a standalone special form for ordinary scripts or standalone procedures.

!!! info "One class per script"
    SSL allows only one [`:CLASS`](../keywords/CLASS.md) definition per script file. If your design requires multiple related classes, each must live in its own script.

## Notes for daily SSL work

!!! success "Do"
    - Use `Me` to access fields and methods within class method bodies.
    - Use `Me:Method(args)` to call other methods on the same instance.
    - Use `Me` to disambiguate when a parameter or local variable shadows an instance field.

!!! failure "Don't"
    - Use `Me` in standalone procedures, global scope, or outside a class. It produces a compile-time error.
    - Use `DoProc("MethodName")` from inside a class method. Call sibling methods with `Me:MethodName()` instead.
    - Assume `Me:MethodName()` will succeed for a missing method. Invalid method calls fail at compile time.

## Errors and edge cases

- Using `Me` outside a class method body results in a compile-time error.
- `Me` is case-insensitive, but `Me` is the canonical spelling in documentation and examples.
- Fields referenced through `Me` can resolve from the current class or an ancestor class.
- A missing `Me:MethodName()` target is a compile-time error.

## Examples

### Accessing instance fields

Sets `nQuantity` and `nUnitPrice` via `Me` in the constructor, then reads them in `CalculateTotal`. With `{5, 12}` as arguments, the result is 60.

Class script:

```ssl
:CLASS OrderCalculator;
:DECLARE nQuantity, nUnitPrice;

:PROCEDURE CalculateTotal;
	:DECLARE nTotal;

	nTotal := Me:nQuantity * Me:nUnitPrice;
	UsrMes("Total: " + LimsString(nTotal));

	:RETURN nTotal;
:ENDPROC;


:PROCEDURE Constructor;
	:PARAMETERS nQty, nPrice;

	Me:nQuantity := nQty;
	Me:nUnitPrice := nPrice;
:ENDPROC;
```

Usage:

```ssl
:DECLARE oCalc;

oCalc := CreateUdObject("OrderCalculator", {5, 12});
oCalc:CalculateTotal();
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
Total: 60
```

### Calling methods on the same instance

`Process` calls `Me:IsValid()` to check state before updating status. When the sample ID is non-empty, the status changes to `"PROCESSED"`.

Class script:

```ssl
:CLASS SampleProcessor;
:DECLARE sSampleId, sStatus;

:PROCEDURE Process;
	:IF Me:IsValid();
		Me:sStatus := "PROCESSED";
		UsrMes(Me:sSampleId + " processed successfully");
		/* Logs the success message for the sample ID;
	:ELSE;
		Me:sStatus := "FAILED";
		UsrMes(Me:sSampleId + " failed validation");
		/* Logs the failure message for the sample ID;
	:ENDIF;
:ENDPROC;

:PROCEDURE IsValid;
	:RETURN !Empty(Me:sSampleId);
:ENDPROC;

:PROCEDURE GetStatus;
	:RETURN Me:sStatus;
:ENDPROC;


:PROCEDURE Constructor;
	:PARAMETERS sId;

	Me:sSampleId := sId;
	Me:sStatus := "PENDING";
:ENDPROC;
```

Usage:

```ssl
:DECLARE oSample;

oSample := CreateUdObject("SampleProcessor", {"S-001"});
oSample:Process();

UsrMes("Status: " + oSample:GetStatus());
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
Status: PROCESSED
```

### Disambiguating parameters from instance fields

`Constructor` takes `sKey` and `sValue` as parameters with the same names as the class fields. `Me:sKey` and `Me:sValue` write to the instance fields while the bare names refer to the local parameters.

Class script:

```ssl
:CLASS ConfigEntry;
:DECLARE sKey, sValue;

:PROCEDURE UpdateValue;
	:PARAMETERS sValue;

	Me:sValue := sValue;
:ENDPROC;

:PROCEDURE GetDisplay;
	:RETURN Me:sKey + " = " + Me:sValue;
:ENDPROC;


:PROCEDURE Constructor;
	:PARAMETERS sKey, sValue;

	Me:sKey := sKey;
	Me:sValue := sValue;
:ENDPROC;
```

Usage:

```ssl
:DECLARE oEntry;

oEntry := CreateUdObject("ConfigEntry", {"MaxRetries", "3"});
oEntry:UpdateValue("5");
UsrMes(oEntry:GetDisplay());
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
MaxRetries = 5
```

## Related elements

- [`Base:`](base.md)
- [`Constructor`](constructor.md)
- [`CLASS`](../keywords/CLASS.md)
