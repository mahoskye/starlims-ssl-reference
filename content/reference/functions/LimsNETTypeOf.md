---
title: "LimsNETTypeOf"
summary: "Resolves a .NET type name string to a .NET Type object."
id: ssl.function.limsnettypeof
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsNETTypeOf

Resolves a .NET type name string to a .NET `Type` object.

Use `LimsNETTypeOf` when you need a runtime type handle for .NET interop. It accepts a non-empty string, trims surrounding whitespace, and returns a .NET type object for the resolved name. The resolver recognizes common aliases such as [`string`](../types/string.md), `int`, `bool`, `double`, `decimal`, `datetime`, and [`object`](../types/object.md), and it also accepts fully qualified type names.

## When to use

- When another .NET interop step needs a resolved type object rather than a raw type name string.
- When you want to accept a type name from configuration or user input and resolve it at runtime.
- When you need alias support such as [`string`](../types/string.md) or `int` instead of writing the full `System.*` name.

## Syntax

```ssl
LimsNETTypeOf(sTypeName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sTypeName` | [string](../types/string.md) | yes | — | Type name to resolve. Leading and trailing whitespace is ignored. Built-in aliases such as [`string`](../types/string.md), `int`, `bool`, `datetime`, and [`object`](../types/object.md) are supported, as are fully qualified type names. |

## Returns

**[object](../types/object.md)** — A .NET `Type` object for the resolved type name.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sTypeName` is [`NIL`](../literals/nil.md). | `Value cannot be null. (Parameter 'sTypeName')` |
| `sTypeName` is not a string or trims to an empty value. | `Argument must be a non-empty string.` |
| The type name cannot be resolved. | `Type: <typeFullName> was not found.` |

## Best practices

!!! success "Do"
    - Validate dynamic input before calling the function.
    - Use fully qualified names for custom types or when alias resolution is not enough.
    - Wrap user-driven or configuration-driven lookups in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md).

!!! failure "Don't"
    - Pass numbers, objects, or arrays and expect implicit conversion to a type name.
    - Assume every short name will resolve outside the built-in aliases.
    - Continue as if lookup always succeeds when the type name comes from external input.

## Caveats

- A whitespace-only string is invalid.
- The not-found message uses the resolved full name when an alias expands first, such as `System.Int32` for `int`.

## Examples

### Resolve a built-in alias

Use one of the built-in aliases and inspect the resolved full name. The alias `"string"` expands to `System.String`.

```ssl
:DECLARE sTypeName, oType;

sTypeName := "string";
oType := LimsNETTypeOf(sTypeName);

UsrMes("Resolved type: " + LimsString(oType:FullName));
```

[`UsrMes`](UsrMes.md) displays:

```text
Resolved type: System.String
```

### Resolve a fully qualified type name

Use the full name when you want an exact type instead of relying on an alias. `"System.Text.StringBuilder"` resolves to a type with short name `StringBuilder`.

```ssl
:DECLARE sTypeName, oType, sTypeLabel;

sTypeName := "System.Text.StringBuilder";
oType := LimsNETTypeOf(sTypeName);
sTypeLabel := LimsString(oType:Name);

UsrMes("Resolved type name: " + sTypeLabel);
UsrMes("Full name: " + LimsString(oType:FullName));
```

[`UsrMes`](UsrMes.md) displays:

```text
Resolved type name: StringBuilder
Full name: System.Text.StringBuilder
```

### Validate dynamic input before lookup

Guard user-supplied input, then catch lookup failures so the script can report a useful message. Because `"CustomLib.Models.FooBar"` is a non-empty string but an unknown type, the [`:TRY`](../keywords/TRY.md) fires and the [`:CATCH`](../keywords/CATCH.md) branch reports the error.

```ssl
:DECLARE sTypeName, oType, oErr;

sTypeName := "CustomLib.Models.FooBar";

:IF LimsTypeEx(sTypeName) != "STRING" .OR. Empty(AllTrim(sTypeName));
	UsrMes("Type name must be a non-empty string.");
:ELSE;
	:TRY;
		oType := LimsNETTypeOf(sTypeName);
		UsrMes("Resolved type: " + LimsString(oType:FullName));
	:CATCH;
		oErr := GetLastSSLError();
		UsrMes("Could not resolve type: " + oErr:Description);
	:ENDTRY;
:ENDIF;
```

## Related

- [`LimsNETCast`](LimsNETCast.md)
- [`LimsNETConnect`](LimsNETConnect.md)
- [`MakeNETObject`](MakeNETObject.md)
- [`string`](../types/string.md)
