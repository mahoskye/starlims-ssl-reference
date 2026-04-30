---
title: "LimsNETCast"
summary: "Prepares a value for a requested interop type such as an enum, by-reference value, numeric type, or typed array."
id: ssl.function.limsnetcast
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsNETCast

Prepares a value for a requested interop type such as an enum, by-reference value, numeric type, or typed array.

`LimsNETCast` uses the `sNewType` string to decide how to treat `vVal`. When `sNewType` starts with `enum:`, the function accepts a string or number and prepares an enum value. When `sNewType` is `byref`, it returns a by-reference wrapper around the original value. When `vVal` is numeric, the function can apply a numeric target type. When `vVal` is an array, it can apply an array target type. If none of those cases apply, the original value is returned unchanged.

## When to use

- When a .NET interop call expects a specific enum or numeric type.
- When you need a by-reference wrapper for an interop scenario.
- When you need to prepare an SSL array as a typed array for interop.
- When you want to keep interop type intent explicit instead of relying on implicit conversion.

## Syntax

```ssl
LimsNETCast(vVal, sNewType)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vVal` | any | yes | — | Value to prepare for the requested target type. [`NIL`](../literals/nil.md) is allowed and is returned unchanged. |
| `sNewType` | [string](../types/string.md) | yes | — | Target type instruction such as `enum:Namespace.Type`, `byref`, a numeric type name, or an array type name. |

## Returns

**any** — A value prepared according to `sNewType`, or the original value when no cast path applies.

Common outcomes:

| Condition | Result |
|-----------|--------|
| `vVal` is [`NIL`](../literals/nil.md) | Returns [`NIL`](../literals/nil.md) |
| `sNewType` starts with `enum:` | Returns an enum-ready value based on the supplied string or number |
| `sNewType` is `byref` | Returns a by-reference wrapper around `vVal` |
| `vVal` is numeric | Returns a numeric value tagged with the requested numeric type |
| `vVal` is an array | Returns an array value tagged with the requested array type |
| Any other case | Returns `vVal` unchanged |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sNewType` is [`NIL`](../literals/nil.md) or empty. | `Argument sNewType cannot be empty.` |
| `sNewType` starts with `enum:` and `vVal` is not a string or number. | `Argument vVal must be a number or a string.` |
| `vVal` is numeric and `sNewType` is not a valid numeric target type. | `Invalid type for cast: <sNewType>` |

## Best practices

!!! success "Do"
    - Validate `sNewType` before calling so the cast path is explicit.
    - Use `enum:` only with a string or numeric source value.
    - Use specific numeric and array target types when an interop API expects them.

!!! failure "Don't"
    - Pass unchecked user input directly into `sNewType` — invalid type strings fail at runtime.
    - Use enum casts with arrays, objects, or other unsupported source types.
    - Assume every type name forces a conversion; unsupported combinations return the original value unchanged.

## Caveats

- `byref` is matched case-insensitively.
- If `vVal` is neither an enum candidate, a numeric value, nor an array, the function returns the original value unless `sNewType` is `byref`.
- Array casts may still fail later if the array contents do not fit the requested target array type.

## Examples

### Cast a string to an enum target

Prepare a string value for a .NET enum parameter.

```ssl
:DECLARE sStatus, vEnumValue;

sStatus := "Active";
vEnumValue := LimsNETCast(sStatus, "enum:MyCompany.SampleStatus");
```

### Cast a number to a specific numeric type

Prepare a numeric value for an interop call that expects a specific numeric type.

```ssl
:DECLARE nCount, vTypedCount;

nCount := 25;
vTypedCount := LimsNETCast(nCount, "System.Int32");
```

### Cast an SSL array to a typed array

Prepare an array of numeric values for an interop call that expects an integer array.

```ssl
:DECLARE aSampleIds, vTypedIds;

aSampleIds := {1001, 1002, 1003};
vTypedIds := LimsNETCast(aSampleIds, "System.Int32[]");
```

## Related

- [`LimsNETConnect`](LimsNETConnect.md)
- [`LimsNETTypeOf`](LimsNETTypeOf.md)
- [`MakeNETObject`](MakeNETObject.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
