---
title: "LimsNETConnect"
summary: "Loads a .NET assembly, resolves a type, and either returns a type handle or creates an instance for SSL interop."
id: ssl.function.limsnetconnect
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsNETConnect

Loads a .NET assembly, resolves a type, and either returns a type handle or creates an instance for SSL interop.

`LimsNETConnect` is the main entry point for .NET interop from SSL. You can use it to load an assembly by name or `.dll` path, resolve a type within that assembly, return the type itself for static access, or create a new instance with constructor arguments. If `sTypeName` is omitted, the function returns the loaded assembly object instead of resolving a type.

When constructor arguments are supplied, pass them as an SSL array. If a constructor updates by-reference or out values, the corresponding entries in that SSL array are updated after the call.

## When to use

- When you need to call .NET static members from SSL.
- When you need to create a .NET object with constructor arguments.
- When you need to load a specific assembly before resolving a type.
- When you need constructor by-reference or out values copied back into an SSL array.

## Syntax

```ssl
LimsNETConnect([sAssembly], [sTypeName], [aArgs], [bAsStatic])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sAssembly` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Assembly name or `.dll` path to load. If the value ends with `.dll`, the runtime first checks that path, then also checks the application's `Components` folder. When [`NIL`](../literals/nil.md), the runtime uses the default .NET assembly containing `System.String`. |
| `sTypeName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Fully qualified .NET type name to resolve from the loaded assembly. If omitted or empty, the function returns the assembly object. |
| `aArgs` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Constructor arguments for instance creation. |
| `bAsStatic` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Pass [`.T.`](../literals/true.md) to return the resolved type for static access instead of creating an instance. Values other than [`.T.`](../literals/true.md) behave like [`.F.`](../literals/false.md). |

## Returns

**any** — Return shape depends on how you call the function.

| Call pattern | Result |
| --- | --- |
| `sTypeName` omitted or empty | Loaded assembly object |
| `bAsStatic` is [`.T.`](../literals/true.md) | Resolved .NET type object |
| Resolved type is static-only or has no public constructors | Resolved .NET type object |
| Instance creation returns a value that maps cleanly to SSL | Corresponding SSL value |
| Instance creation returns a value that does not map cleanly to SSL | .NET interop object |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sAssembly` is not a string. | `Argument 'sAssembly' must be a string.` |
| `sTypeName` is not a string. | `Argument 'sTypeName' must be a string.` |
| `aArgs` is not an array. | `Argument 'aArgs' must be an array.` |
| A `.dll` path cannot be found. | `File: <path> doesn't exist.` |
| Assembly loading fails. | `Error loading the assembly: <assembly>.` |
| The requested type cannot be resolved. | `Type: <typeFullName> was not found.` |

## Best practices

!!! success "Do"
    - Pass `bAsStatic` as [`.T.`](../literals/true.md) only when you want the type itself for static member access.
    - Pass constructor arguments as an array, even for a single argument.
    - Use fully qualified type names so resolution is predictable.
    - Wrap calls in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the assembly, type, or constructor may fail at runtime.

!!! failure "Don't"
    - Pass non-string values for `sAssembly` or `sTypeName`, or a non-array value for `aArgs`.
    - Omit `sTypeName` unless you actually want the assembly object rather than a type or instance.
    - Pass a single constructor argument directly. Use `{value}` rather than `value`.
    - Assume a `.dll` name will resolve unless that file exists at the provided path or in the application's `Components` folder.

## Examples

### Access a static .NET member

Return a type handle and call a static member.

```ssl
:PROCEDURE AccessStaticMathMembers;
    :DECLARE oMathType, nAbsValue, nMaxValue;

    oMathType := LimsNETConnect(, "System.Math",, .T.);
    nAbsValue := oMathType:Abs(-42);
    nMaxValue := oMathType:Max(10, 20);

    UsrMes("Absolute value: " + LimsString(nAbsValue));
    UsrMes("Maximum value: " + LimsString(nMaxValue));
:ENDPROC;

/* Usage;
DoProc("AccessStaticMathMembers");
```

### Create an instance with constructor arguments

Create an object and call instance methods on it.

```ssl
:PROCEDURE BuildStringWithNET;
    :DECLARE oBuilder, sText;

    oBuilder := LimsNETConnect(, "System.Text.StringBuilder", {"Hello"});
    oBuilder:Append(" SSL");
    oBuilder:Append(" interop");

    sText := oBuilder:ToString();

    UsrMes(sText);
:ENDPROC;

/* Usage;
DoProc("BuildStringWithNET");
```

[`UsrMes`](UsrMes.md) displays:

```
Hello SSL interop
```

### Receive by-reference constructor updates

Pass a by-reference placeholder in the constructor argument array and then read the updated array entry after construction.

```ssl
:PROCEDURE CreateWithByRefOutput;
    :DECLARE sAssembly, sTypeName, aArgs, oObject;
    :DECLARE nInput, nOutput;

    sAssembly := "CustomInterop.dll";
    sTypeName := "CustomInterop.SampleProcessor";
    nInput := 42;
    nOutput := 0;

    aArgs := {nInput, LimsNETCast(nOutput, "byref")};

    :TRY;
        oObject := LimsNETConnect(sAssembly, sTypeName, aArgs);
        nOutput := aArgs[2];

        UsrMes("Object created successfully");
        UsrMes("Updated output value: " + LimsString(nOutput));
        /* Displays updated output value on success;
    :CATCH;
        ErrorMes(GetLastSSLError():Description);
        /* Displays failure details;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CreateWithByRefOutput");
```

## Related

- [`LimsNETCast`](LimsNETCast.md)
- [`LimsNETTypeOf`](LimsNETTypeOf.md)
- [`MakeNETObject`](MakeNETObject.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
