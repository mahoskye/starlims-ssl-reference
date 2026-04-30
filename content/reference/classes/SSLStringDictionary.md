---
title: "SSLStringDictionary"
summary: "Stores values by string key."
id: ssl.class.sslstringdictionary
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLStringDictionary

Stores values by string key.

`SSLStringDictionary` is a dictionary class for lookups keyed by strings. Use it when your SSL code needs to map names, codes, or identifiers to stored values without scanning arrays manually.

It supports adding or replacing values, checking whether a key exists, retrieving a value with an optional fallback, removing entries, clearing the dictionary, and reading the current `Count`, `Keys`, and `Values`.

## When to use

- When your keys are names, codes, statuses, or other string identifiers.
- When you want dictionary-style lookup instead of repeated array searches.
- When you need either case-insensitive or case-sensitive string matching.
- When you need to tell the difference between a missing key and a stored value by using `TryGetValue()`.

## Constructors

### `SSLStringDictionary{}`

Creates an empty case-insensitive dictionary.

### `SSLStringDictionary{bCaseSensitive, nLength}`

Creates an empty dictionary with configurable case matching and an initial capacity hint.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `bCaseSensitive` | [boolean](../types/boolean.md) | yes | When true, key matching is case-sensitive. When false, matching is case-insensitive. |
| `nLength` | [number](../types/number.md) | yes | Integer-valued capacity hint for the initial dictionary size. |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `Count` | [number](../types/number.md) | read-only | Number of key-value pairs currently stored |
| `Keys` | [array](../types/array.md) | read-only | Array of the current string keys |
| `Values` | [array](../types/array.md) | read-only | Array of the current stored values |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `Clear()` | [boolean](../types/boolean.md) | Removes all entries and returns [`.T.`](../literals/true.md) |
| `AddValue(sKey, vValue)` | [boolean](../types/boolean.md) | Adds or replaces a value for a string key |
| `Contains(sKey)` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the key exists |
| `GetValue(sKey, vDefaultValue)` | any | Returns the stored value or the fallback |
| `Remove(sKey)` | [boolean](../types/boolean.md) | Removes a key and returns whether it was removed |
| `TryGetValue(sKey)` | [object](../types/object.md) | Returns an object with `Exists` and `Value` |

### `Clear`

Removes all key-value pairs from the dictionary.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the dictionary is cleared.

### `AddValue`

Adds or replaces a value for a string key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sKey` | [string](../types/string.md) | yes | Key to store |
| `vValue` | any | yes | Value to store |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when `sKey` is a string, [`.F.`](../literals/false.md) when the key is not a valid string key.

### `Contains`

Checks whether the dictionary contains the specified key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sKey` | [string](../types/string.md) | yes | Key to check |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the key exists, [`.F.`](../literals/false.md) when it does not.

**Raises:**
- `Argument 'sKey' must be a non-null string` when `sKey` is not a valid string key.

### `GetValue`

Returns the value stored for a key, or the fallback value when the key is missing or invalid.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sKey` | [string](../types/string.md) | yes | Key to look up |
| `vDefaultValue` | any | no | Value to return when the key is missing |

**Returns:** any — Stored value when found. Otherwise returns `vDefaultValue`. If you omit `vDefaultValue`, a missing key returns [`NIL`](../literals/nil.md).

### `Remove`

Removes the specified key from the dictionary.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sKey` | [string](../types/string.md) | yes | Key to remove |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the key was removed, [`.F.`](../literals/false.md) when the key was not present.

**Raises:**
- `Argument 'sKey' must be a non-null string` when `sKey` is not a valid string key.

### `TryGetValue`

Attempts to read a value and reports both whether the key exists and the stored value.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sKey` | [string](../types/string.md) | yes | Key to look up |

**Returns:** [object](../types/object.md) — An object with `Exists` and `Value` properties. `Exists` is [`.T.`](../literals/true.md) when the key was found and [`.F.`](../literals/false.md) when it was not. When the key is missing, `Value` is [`NIL`](../literals/nil.md).

**Raises:**
- `Argument 'sKey' must be a non-null string` when `sKey` is not a valid string key.

## Inheritance

**Base class:** [`SSLBaseDictionary`](SSLBaseDictionary.md)

Inherited members available on `SSLStringDictionary` include:

- `Count`
- `Keys`
- `Values`
- `Clear()`

## Best practices

!!! success "Do"
    - Use the default constructor when you want case-insensitive lookups for ordinary status names, setting names, or other user-facing keys.
    - Use `TryGetValue()` when you need to know whether a key exists instead of relying on a fallback value.
    - Pass a capacity hint only when you already expect a larger dictionary.

!!! failure "Don't"
    - Assume different casing creates separate entries in the default constructor, because `SSLStringDictionary{}` matches keys case-insensitively.
    - Use `GetValue()` by itself when a stored value could be the same as your fallback, because only `TryGetValue()` tells you whether the key was present.
    - Pass [`NIL`](../literals/nil.md), numbers, or other non-string values as keys, because invalid keys either fail silently with [`.F.`](../literals/false.md), return the fallback value, or raise an error, depending on the method you call.

## Caveats

- `Contains()`, `Remove()`, and `TryGetValue()` are stricter than `AddValue()` and `GetValue()` for invalid keys.
- In a case-sensitive dictionary, `"Spec"` and `"spec"` are different keys.
- The `nLength` argument is only a starting-size hint. It does not limit how many entries the dictionary can hold.

## Examples

### Store and retrieve values by string key

Creates a case-insensitive dictionary, adds two entries including a duplicate key that replaces the earlier value, then retrieves values with mixed-case keys to show that case is ignored in lookups.

```ssl
:PROCEDURE DemoStringDictionary;
	:DECLARE oSettings, sStatus, sReviewer;

	oSettings := SSLStringDictionary{};

	oSettings:AddValue("status", "Logged");
	oSettings:AddValue("reviewer", "jsmith");
	oSettings:AddValue("reviewer", "adoyle");

	sStatus := oSettings:GetValue("STATUS", "Unknown");
	sReviewer := oSettings:GetValue("Reviewer", "");

	UsrMes("Status: " + sStatus);

	UsrMes("Reviewer: " + sReviewer);

	UsrMes("Entry count: " + LimsString(oSettings:Count));
:ENDPROC;

/* Usage;
DoProc("DemoStringDictionary");
```

### Use case-sensitive keys and `TryGetValue()`

Creates a case-sensitive dictionary with a capacity hint, adds entries with different casings as separate keys, then uses `TryGetValue()` to confirm that `"ApprovedBy"` and `"approvedby"` are distinct, that an empty stored value still reports as present, and that `"APPROVEDBY"` is absent entirely.

```ssl
:PROCEDURE DemoStringDictionaryLookup;
	:DECLARE oReleaseInfo, oLookup, vMissing;

	oReleaseInfo := SSLStringDictionary{.T., 5};

	oReleaseInfo:AddValue("ApprovedBy", "QCLead");
	oReleaseInfo:AddValue("approvedby", "auto-release");
	oReleaseInfo:AddValue("Comment", "");

	oLookup := oReleaseInfo:TryGetValue("ApprovedBy");
	:IF oLookup:Exists;
		UsrMes("ApprovedBy: " + oLookup:Value);
	:ENDIF;

	oLookup := oReleaseInfo:TryGetValue("approvedby");
	:IF oLookup:Exists;
		UsrMes("approvedby: " + oLookup:Value);
	:ENDIF;

	oLookup := oReleaseInfo:TryGetValue("Comment");
	:IF oLookup:Exists;
		UsrMes("Comment exists even though the stored value is empty");
	:ENDIF;

	oLookup := oReleaseInfo:TryGetValue("APPROVEDBY");
	:IF .NOT. oLookup:Exists;
		UsrMes("APPROVEDBY was not found");
	:ENDIF;

	vMissing := oLookup:Value;

	UsrMes("Missing value is NIL: " + LimsString(vMissing == NIL));
:ENDPROC;

/* Usage;
DoProc("DemoStringDictionaryLookup");
```

## Related

- [`SSLBaseDictionary`](SSLBaseDictionary.md)
- [`SSLIntDictionary`](SSLIntDictionary.md)
- [`SSLExpando`](SSLExpando.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
