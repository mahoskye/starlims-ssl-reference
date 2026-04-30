---
title: "base"
summary: "Provides explicit access to members on a class's immediate parent type from within a class method."
id: ssl.special_form.base
element_type: special_form
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# base

## What it does

Provides explicit access to members on a class's immediate parent type from within a class method.

Use `Base:MemberName` when a derived class needs the parent implementation or the parent version of a member instead of the current class version. `Base` always targets the current class's base type, so `Base:MethodName()` calls the parent method directly and `Base:FieldName` or `Base:PropertyName` reads or writes the parent member rather than the derived one.

`Base` resolves the member lookup against the immediate parent class of the current class. For method calls, the parent method must exist or compilation fails. For field or property access, the compiler resolves the member against the parent type and warns if it cannot find a matching base member.

## When to use it

- When an overridden method needs to call the parent implementation.
- When derived code needs the parent version of a field or property.
- When a derived constructor must run parent initialization before its own setup.

## Syntax

```ssl
Base:FieldName;
Base:PropertyName;
Base:MethodName(args);
Base:Constructor(args);
```

## Context rules

`Base` is valid inside [`:CLASS`](../keywords/CLASS.md) method bodies. It is meaningful when the current class inherits from another class and you need that parent member explicitly. `Base` is not a standalone value; it must be followed by `:MemberName`.

!!! info "One class per script"
    SSL allows only one [`:CLASS`](../keywords/CLASS.md) definition per script file. Parent and child classes must live in separate scripts. The examples below show separate class blocks followed by a separate usage block.

## Notes for daily SSL work

!!! success "Do"
    - Use `Base:MethodName()` when you are extending inherited behavior rather than replacing it completely.
    - Call `Base:Constructor()` in a derived constructor when the parent class needs initialization.
    - Keep `Base` usage focused on places where the parent implementation is clearly part of the design.

!!! failure "Don't"
    - Use `Base` when [`Me`](me.md)`:MethodName()` is the intended polymorphic call path. `Base` skips the derived override.
    - Assume a derived member name automatically exists on the parent class too. `Base` only works with members available on the parent type.
    - Scatter `Base` calls through unrelated logic. Overuse makes inheritance behavior harder to follow.

## Errors and edge cases

- `Base` must be written as member access: `Base:MethodName()` or `Base:FieldName`.
  It cannot be used as a standalone expression.
- A missing base method is a compile-time error.
- Base field and property access is limited to members available on the parent type.
- `Base` outside a [`:CLASS`](../keywords/CLASS.md) method raises a compile-time error.

## Examples

### Calling the parent implementation from an override

A derived `Calculator` class overrides `Add` to track the last value before delegating to the parent implementation via `Base:Add(nValue)`. The constructor also chains to `Base:Constructor()` to ensure the parent initializes its state.

Parent class:

```ssl
:CLASS CalculatorBase;
:DECLARE nTotal;

:PROCEDURE Add;
	:PARAMETERS nValue;

	nTotal += nValue;
:ENDPROC;


:PROCEDURE GetTotal;
	:RETURN nTotal;
:ENDPROC;


:PROCEDURE Constructor;
	nTotal := 0;
:ENDPROC;
```

Derived class:

```ssl
:CLASS Calculator;
:INHERIT Lab:CalculatorBase;

:DECLARE nLastValue;

:PROCEDURE Add;
	:PARAMETERS nValue;

	nLastValue := nValue;
	Base:Add(nValue);

	UsrMes("Added " + LimsString(nValue));
:ENDPROC;


:PROCEDURE GetLastValue;
	:RETURN nLastValue;
:ENDPROC;


:PROCEDURE Constructor;
	Base:Constructor();
	nLastValue := 0;
:ENDPROC;
```

Usage:

```ssl
:DECLARE oCalc, nTotal;

oCalc := CreateUdObject("Calculator");
oCalc:Add(5);
oCalc:Add(3);

nTotal := oCalc:GetTotal();
UsrMes("Total: " + LimsString(nTotal));
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Added 5
Added 3
Total: 8
```

### Reading a parent field directly from derived code

`EmployeeRecord` extends `PersonBase`. The constructor chains to `Base:Constructor(sName)` to initialize the parent's `sLegalName` field. `ShowNames` then reads both `Me:sBadgeName` (the derived field) and `Base:sLegalName` (the parent field) to display both names.

Parent class:

```ssl
:CLASS PersonBase;
:DECLARE sLegalName;

:PROCEDURE GetLegalName;
	:RETURN sLegalName;
:ENDPROC;


:PROCEDURE Constructor;
	:PARAMETERS sName;

	sLegalName := sName;
:ENDPROC;
```

Derived class:

```ssl
:CLASS EmployeeRecord;
:INHERIT Lab:PersonBase;

:DECLARE sBadgeName, sRole;

:PROCEDURE ShowNames;
	:DECLARE sDerivedLabel, sBaseLabel;

	sDerivedLabel := "Badge name: " + Me:sBadgeName;
	sBaseLabel := "Legal name: " + Base:sLegalName;

	UsrMes(sDerivedLabel);
	UsrMes(sBaseLabel);

	:RETURN {sDerivedLabel, sBaseLabel};
:ENDPROC;


:PROCEDURE Constructor;
	:PARAMETERS sName, sBadge, sEmpRole;

	Base:Constructor(sName);

	sBadgeName := sBadge;
	sRole := sEmpRole;
:ENDPROC;
```

Usage:

```ssl
:DECLARE oEmployee;

oEmployee := CreateUdObject("EmployeeRecord", {"Alice Adams", "A. Adams", "Chemist"});
oEmployee:ShowNames();
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Badge name: A. Adams
Legal name: Alice Adams
```

## Related elements

- [`me`](me.md)
- [`constructor`](constructor.md)
- [`CLASS`](../keywords/CLASS.md)
- [`INHERIT`](../keywords/INHERIT.md)
