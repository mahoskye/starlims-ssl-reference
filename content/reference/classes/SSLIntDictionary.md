---
title: "SSLIntDictionary"
summary: "Stores values by whole-number keys."
id: ssl.class.sslintdictionary
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLIntDictionary

Stores values by whole-number keys.

`SSLIntDictionary` is a dictionary class for lookups keyed by integer-valued numbers. Use it when your SSL code needs to map numeric IDs, sequence values, or similar whole-number keys to any kind of stored value.

It supports adding or replacing values, checking whether a key exists, retrieving a value with an optional fallback, removing entries, clearing the dictionary, and reading the current `Count`, `Keys`, and `Values`.

## When to use

- When your keys are numeric IDs or other whole-number values.
- When you want dictionary-style lookup instead of scanning arrays manually.
- When you need to distinguish between a missing key and a stored value by using `TryGetValue()`.

## Constructors

### `SSLIntDictionary{}`

Creates an empty dictionary.

### `SSLIntDictionary{nLength}`

Creates an empty dictionary with an optional initial capacity hint.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nLength` | [number](../types/number.md) | no | Optional initial capacity hint. If you omit it, or pass a value that is not an integer-valued number, the dictionary uses its default starting size. |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `Count` | [number](../types/number.md) | read-only | Number of key-value pairs currently stored |
| `Keys` | [array](../types/array.md) | read-only | Array of the current keys |
| `Values` | [array](../types/array.md) | read-only | Array of the current values |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `Clear()` | [boolean](../types/boolean.md) | Removes all entries and returns [`.T.`](../literals/true.md) |
| `AddValue(nKey, vValue)` | [boolean](../types/boolean.md) | Adds or replaces a value for an integer-valued numeric key |
| `Contains(nKey)` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the key exists |
| `GetValue(nKey, vDefaultValue)` | any | Returns the stored value or the fallback |
| `Remove(nKey)` | [boolean](../types/boolean.md) | Removes a key and returns whether it was removed |
| `TryGetValue(nKey)` | [object](../types/object.md) | Returns an object with `Exists` and `Value` |

### `Clear`

Removes all key-value pairs from the dictionary.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the dictionary is cleared.

### `AddValue`

Adds or replaces a value for an integer-valued numeric key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nKey` | [number](../types/number.md) | yes | Integer-valued numeric key to store |
| `vValue` | any | yes | Value to store |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the key is a valid integer-valued number and the value is stored, [`.F.`](../literals/false.md) when the key is not a valid integer-valued number.

### `Contains`

Checks whether the dictionary contains the specified key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nKey` | [number](../types/number.md) | yes | Integer-valued numeric key to check |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the key exists, [`.F.`](../literals/false.md) when it does not.

**Raises:**
- **When `nKey` is not a number:** `Argument 'nKey' must be a number`

### `GetValue`

Returns the value stored for a key, or the fallback value when the key is missing or invalid.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nKey` | [number](../types/number.md) | yes | Integer-valued numeric key to look up |
| `vDefaultValue` | any | no | Value to return when the key is missing |

**Returns:** any — Stored value when found, otherwise `vDefaultValue`.

### `Remove`

Removes the specified key from the dictionary.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nKey` | [number](../types/number.md) | yes | Integer-valued numeric key to remove |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the key was removed, [`.F.`](../literals/false.md) when the key was not present.

**Raises:**
- **When `nKey` is not a number:** `Argument 'nKey' must be a number`

### `TryGetValue`

Attempts to read a value and reports both whether the key exists and the stored value.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nKey` | [number](../types/number.md) | yes | Integer-valued numeric key to look up |

**Returns:** [object](../types/object.md) — An object with `Exists` and `Value` properties. When the key is missing, `Exists` is [`.F.`](../literals/false.md) and `Value` is [`NIL`](../literals/nil.md).

**Raises:**
- **When `nKey` is not a number:** `Argument 'nKey' must be a number`

## Inheritance

**Base class:** [`SSLBaseDictionary`](SSLBaseDictionary.md)

Inherited members available on `SSLIntDictionary` include:

- `Count`
- `Keys`
- `Values`
- `Clear()`

## Best practices

!!! success "Do"
    - Use `SSLIntDictionary` when your keys are integer-valued numeric IDs such as sample, order, or task identifiers.
    - Use `TryGetValue()` when you need to know whether a key exists without relying on a fallback value.
    - Pass an initial capacity only when you already expect a larger dictionary.

!!! failure "Don't"
    - Pass text or fractional values as keys, because invalid keys either fail silently with [`.F.`](../literals/false.md), return the fallback value, or raise an error, depending on the method you call.
    - Use `GetValue()` by itself when you must tell the difference between a missing key and a stored value that could match your fallback.
    - Assume adding the same key creates a second entry, because `AddValue()` replaces the existing value for that key.

## Caveats

- `AddValue()` and `GetValue()` are forgiving with invalid keys, but `Contains()`, `Remove()`, and `TryGetValue()` are not.
- `GetValue()` uses the optional fallback only when no value is returned for the key.

## Examples

### Store and retrieve values by numeric ID

Adds two entries keyed by numeric ID, then retrieves a value with `GetValue`, checks existence with `Contains`, and reads the current `Count`.

```ssl
:PROCEDURE DemoIntDictionary;
	:DECLARE oStatusById, sStatus, bFound;

	oStatusById := SSLIntDictionary{};

	oStatusById:AddValue(1001, "Logged");
	oStatusById:AddValue(1002, "In Review");

sStatus := oStatusById:GetValue(1001, "Missing");
	UsrMes("Status for 1001: " + sStatus);
	/* Displays stored status for key 1001;

	bFound := oStatusById:Contains(1002);
	UsrMes("1002 exists: " + LimsString(bFound));
	/* Displays whether key 1002 exists;

	UsrMes("Entry count: " + LimsString(oStatusById:Count));
	/* Displays current entry count;
:ENDPROC;
```

### Use TryGetValue before reading the stored value

Creates a dictionary with an initial capacity hint, adds one result entry, then uses `TryGetValue` to check presence without relying on a fallback, once for a key that exists and once for a missing key.

```ssl
:PROCEDURE DemoIntDictionaryLookup;
	:DECLARE oResults, oLookup, sMessage;

	oResults := SSLIntDictionary{20};

	oResults:AddValue(5010, "Pass");

	oLookup := oResults:TryGetValue(5010);

	:IF oLookup:Exists;
		sMessage := "Result 5010: " + LimsString(oLookup:Value);
		UsrMes(sMessage);
		/* Displays stored result for key 5010;
	:ENDIF;

	oLookup := oResults:TryGetValue(9999);

	:IF .NOT. oLookup:Exists;
		UsrMes("Result 9999 was not found");
	:ENDIF;
:ENDPROC;
```

## Related

- [`SSLBaseDictionary`](SSLBaseDictionary.md)
- [`SSLStringDictionary`](SSLStringDictionary.md)
- [`SSLExpando`](SSLExpando.md)
- [`object`](../types/object.md)
- [`number`](../types/number.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
