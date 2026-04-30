---
title: "SSLBaseDictionary"
summary: "Provides the shared dictionary surface used by SSL dictionary classes such as SSLStringDictionary{} and SSLIntDictionary{}."
id: ssl.class.sslbasedictionary
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLBaseDictionary

Provides the shared dictionary surface used by SSL dictionary classes such as [`SSLStringDictionary{}`](SSLStringDictionary.md) and [`SSLIntDictionary{}`](SSLIntDictionary.md).

`SSLBaseDictionary` defines the members shared by SSL dictionary objects: `Count`, `Keys`, `Values`, `Clear`, `AddValue`, `GetValue`, `Contains`, `Remove`, `TryGetValue`, and `Invoke`. You do not create `SSLBaseDictionary{}` directly. Instead, create a concrete dictionary class that matches your key type and use these inherited members on that instance.

The shared behavior is small and consistent. `Count` returns the current number of entries. `Keys` and `Values` return arrays built from the dictionary's current contents. `Clear()` removes all entries and returns [`.T.`](../literals/true.md).

Key validation depends on the concrete dictionary class. That difference matters because the methods do not all react the same way to an invalid key:

- `AddValue(vKey, vValue)` returns [`.F.`](../literals/false.md) when the key is not valid for the concrete dictionary.
- `GetValue(vKey, vDefaultValue)` returns `vDefaultValue` when the key is invalid or not present.
- `Contains(vKey)`, `Remove(vKey)`, and `TryGetValue(vKey)` raise an error when the key is not valid for the concrete dictionary.

## When to use

- When you need to understand the members shared by SSL dictionary classes.
- When you are working with code that receives a dictionary object and only uses the common dictionary surface.
- When you want a reference for `Count`, `Keys`, `Values`, `Clear`, and the standard dictionary methods before choosing a concrete dictionary class.

## Constructors

`SSLBaseDictionary` does not expose a direct SSL constructor. Create a concrete subclass such as [`SSLStringDictionary`](SSLStringDictionary.md) or [`SSLIntDictionary`](SSLIntDictionary.md) instead.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `Count` | [number](../types/number.md) | read-only | Number of key-value pairs currently stored |
| `Keys` | [array](../types/array.md) | read-only | Array containing the current keys |
| `Values` | [array](../types/array.md) | read-only | Array containing the current values |

## Methods

### `Clear`

Removes all key-value pairs from the dictionary.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the dictionary is cleared.

### `AddValue`

Adds or updates a value for the specified key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vKey` | any | yes | Key to add or update. Valid key type depends on the concrete dictionary class. |
| `vValue` | any | yes | Value to store for the key |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the key is accepted and the value is stored, [`.F.`](../literals/false.md) when the key is not valid for the concrete dictionary.

### `GetValue`

Returns the value for a key, or the supplied fallback when the key is not found or is not valid for that dictionary.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vKey` | any | yes | Key to look up |
| `vDefaultValue` | any | no | Value to return when the key is not found or not valid |

**Returns:** any — Stored value, or `vDefaultValue` when no value is returned.

### `Contains`

Checks whether the dictionary contains the specified key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vKey` | any | yes | Key to check |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the key exists, [`.F.`](../literals/false.md) when it does not.

**Raises:**
- **When the key is not valid for the concrete dictionary class:** raises an error instead of returning [`.F.`](../literals/false.md).

### `Remove`

Removes the specified key from the dictionary.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vKey` | any | yes | Key to remove |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the key was removed, [`.F.`](../literals/false.md) when it was not present.

**Raises:**
- **When the key is not valid for the concrete dictionary class:** raises an error instead of returning [`.F.`](../literals/false.md).

### `TryGetValue`

Attempts to read a value without relying on a fallback argument.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vKey` | any | yes | Key to look up |

**Returns:** [object](../types/object.md) — An object with `Exists` and `Value` properties. `Exists` is [`.T.`](../literals/true.md) when the key was found. `Value` contains the stored value when present.

**Raises:**
- **When the key is not valid for the concrete dictionary class:** raises an error.

### `Invoke`

Invokes a dictionary method by name.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sMethodName` | [string](../types/string.md) | yes | Method name such as `AddValue`, `GetValue`, `Contains`, `Remove`, `TryGetValue`, or `Clear` |
| `vArg1`, `vArg2`, ... | any | no | Arguments to pass to the named method |

**Returns:** any — Result of the invoked method.

**Raises:**
- **When a required method argument is missing:** The method: `<name>` requires at least one parameter

`Invoke` matches these method names without case sensitivity.

## Inheritance

**Base class:** [`object`](../types/object.md)

Concrete classes that inherit from `SSLBaseDictionary` include:

- [`SSLStringDictionary`](SSLStringDictionary.md)
- [`SSLIntDictionary`](SSLIntDictionary.md)

## Best practices

!!! success "Do"
    - Create a concrete dictionary class that matches your key type, then use the inherited `SSLBaseDictionary` members on that instance.
    - Use `AddValue(vKey, vValue)` when you want invalid keys to fail with a boolean result instead of an exception.
    - Use `GetValue(vKey, vDefaultValue)` when you want a simple fallback value for missing keys.
    - Use `TryGetValue(vKey)` when you need to know both whether a key exists and what value was stored.
    - Read `Keys`, `Values`, and `Count` after updates when you need the current dictionary state.

!!! failure "Don't"
    - Document or write examples as if `SSLBaseDictionary{}` can be instantiated directly, because this page describes an abstract base class.
    - Assume all dictionary classes accept the same key types, because the concrete class decides what is valid.
    - Expect all invalid-key operations to fail the same way, because `AddValue` and `GetValue` handle invalid keys differently from `Contains`, `Remove`, and `TryGetValue`.
    - Treat `TryGetValue` as returning the value by itself, because it returns an object with `Exists` and `Value`.
    - Pass empty placeholder values just to fill optional arguments, because SSL lets you omit trailing optional arguments.

## Caveats

- `Invoke("Clear")` works without arguments, but methods such as `AddValue`, `GetValue`, `Contains`, `Remove`, and `TryGetValue` raise an error when called through `Invoke` without the required key argument.

## Examples

### Use shared dictionary members on a concrete dictionary

Creates an [`SSLStringDictionary`](SSLStringDictionary.md), adds two entries, then exercises the inherited `SSLBaseDictionary` surface: reading `Count` and `Keys`, looking up values with `GetValue` and `TryGetValue`, and calling `Clear`.

```ssl
:PROCEDURE DictionaryBaseMembers;
	:DECLARE oSettings, oLookup, aKeys, sMessage;

	oSettings := SSLStringDictionary{};

	oSettings:AddValue("instrument", "HPLC-01");
	oSettings:AddValue("status", "Ready");

	sMessage := "Entries: " + LimsString(oSettings:Count);
	UsrMes(sMessage);

	aKeys := oSettings:Keys;
	sMessage := "Keys returned: " + LimsString(ALen(aKeys));
	UsrMes(sMessage);

	sMessage := "Status: " + LimsString(oSettings:GetValue("status", "Unknown"));
	UsrMes(sMessage);

	oLookup := oSettings:TryGetValue("instrument");

	:IF oLookup:Exists;
		sMessage := "Instrument: " + LimsString(oLookup:Value);
		UsrMes(sMessage);
	:ENDIF;

	oSettings:Clear();

	UsrMes("Entries after Clear: " + LimsString(oSettings:Count));
:ENDPROC;

/* Usage;
DoProc("DictionaryBaseMembers");
```

### Call dictionary methods dynamically with Invoke

Uses `Invoke` to call `AddValue`, `Contains`, and `GetValue` by name on an [`SSLIntDictionary`](SSLIntDictionary.md). This pattern is useful when the method to call is determined at runtime.

```ssl
:PROCEDURE DictionaryInvokeExample;
	:DECLARE oDict, vResult, sMethod;

	oDict := SSLIntDictionary{};

	sMethod := "AddValue";
	vResult := oDict:Invoke(sMethod, 1001, "Queued");
	UsrMes("AddValue success: " + LimsString(vResult));

	vResult := oDict:Invoke("Contains", 1001);
	UsrMes("Contains 1001: " + LimsString(vResult));

	vResult := oDict:Invoke("GetValue", 1001, "Missing");
	UsrMes("Value 1001: " + LimsString(vResult));
:ENDPROC;

/* Usage;
DoProc("DictionaryInvokeExample");
```

## Related

- [`SSLStringDictionary`](SSLStringDictionary.md)
- [`SSLIntDictionary`](SSLIntDictionary.md)
- [`object`](../types/object.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
