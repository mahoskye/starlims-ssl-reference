---
title: "FromXml"
summary: "Parses a type-tagged XML string and converts it to the corresponding SSL value."
id: ssl.function.fromxml
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# FromXml

Parses a type-tagged XML string and converts it to the corresponding SSL value.

`FromXml` is the symmetric counterpart to [`ToXml`](ToXml.md). It reads the root element tag to determine the SSL type and converts the content accordingly. Supported root tags are `<bool>`, `<byte>`, `<short>`, `<int>`, `<long>`, `<decimal>`, `<ushort>`, `<uint>`, `<ulong>`, `<float>`, `<double>`, `<string>`, `<date>`, `<complextype>`, `<dto>`, `<null>`, `<dbnull>`, and `<error>`. Any other tag raises an error. Empty or whitespace-only input returns [`NIL`](../literals/nil.md).

## When to use

- When restoring SSL values from XML produced by [`ToXml`](ToXml.md).
- When converting XML containing typed arrays, DTOs, or primitive values back into SSL types.
- When handling integration or import scenarios where XML is in the STARLIMS type-tagged format.

## Syntax

```ssl
FromXml(sXml)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sXml` | [string](../types/string.md) | yes | — | A type-tagged XML string, typically produced by [`ToXml`](ToXml.md). |

## Returns

**any** — The return type depends on the root element tag in `sXml`:

- **[boolean](../types/boolean.md)** — when the root element is `<bool>`.
- **[number](../types/number.md)** — when the root element is `<byte>`, `<short>`, `<int>`, `<long>`, `<decimal>`, `<ushort>`, `<uint>`, `<ulong>`, `<float>`, or `<double>`.
- **[string](../types/string.md)** — when the root element is `<string>`.
- **[date](../types/date.md)** — when the root element is `<date>` with a valid date value.
- **[array](../types/array.md)** — when the root element is `<complextype>`.
- **[object](../types/object.md)** ([`SSLExpando`](../classes/SSLExpando.md)) — when the root element is `<dto>`.
- **NIL** — when `sXml` is empty or whitespace, or when the root element is `<null>`, `<dbnull>`, or `<date>00/00/0000</date>`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sXml` is [`NIL`](../literals/nil.md). | `Argument sXml cannot be null.` |
| The string cannot be parsed as valid XML. | `Error unpacking XML` |
| An element inside `<complextype>` does not match the declared element type. | `Incorrect element type {element} found in array of type {typeName}` |
| The `<complextype>` contents cannot be converted to the target array type. | `Can't convert to array` |
| The root element is `<error>`. | `Error sent from outside: {message}` |
| An element's text cannot be converted to its declared type. | `Tag {element} contains an invalid value!` |
| The root element is not one of the recognized type tags. | `Unknown tag <{tagName}> in XML structure!` |

## Best practices

!!! success "Do"
    - Use [`ToXml`](ToXml.md) to produce the XML string and `FromXml` to restore it — this guarantees the tag format is correct.
    - Handle exceptions when parsing XML from external sources in case the format is invalid or unexpected.
    - Check for [`NIL`](../literals/nil.md) on return to distinguish empty, null, and zero-date inputs.

!!! failure "Don't"
    - Pass hand-authored XML with arbitrary tag names. Only the recognized type tags produce a result; all others raise an error.
    - Assume the return type without checking — the tag determines the type and multiple valid inputs can return [`NIL`](../literals/nil.md).

## Caveats

- `<dto>` elements are restored via [`SSLExpando`](../classes/SSLExpando.md) deserialization and may not implement all methods of a hand-built object.
- A `<date>` element whose text is `00/00/0000` returns [`NIL`](../literals/nil.md), not a zero date.

## Examples

### Parse a typed primitive from XML

Pass a type-tagged XML string directly to recover the original SSL value.

```ssl
:PROCEDURE ParseXmlInteger;
	:DECLARE sXml, nValue;

	sXml := "<int>42</int>";
	nValue := FromXml(sXml);

	UsrMes("Parsed value: " + LimsString(nValue));
	:RETURN nValue;
:ENDPROC;

/* Usage;
DoProc("ParseXmlInteger");
```

[`UsrMes`](UsrMes.md) displays:

```text
Parsed value: 42
```

### Round-trip an array through XML

Use [`ToXml`](ToXml.md) to serialize an array and `FromXml` to restore it, verifying that both values match after the round-trip.

```ssl
:PROCEDURE RoundTripArray;
	:DECLARE aOriginal, sXml, aRestored, nIndex;

	aOriginal := {10, 20, 30};
	sXml := ToXml(aOriginal);
	aRestored := FromXml(sXml);

	:FOR nIndex := 1 :TO ALen(aRestored);
		UsrMes(LimsString(aRestored[nIndex]));
	:NEXT;

	:RETURN aRestored;
:ENDPROC;

/* Usage;
DoProc("RoundTripArray");
```

[`UsrMes`](UsrMes.md) displays:

```text
10
20
30
```

### Handle an invalid or unrecognized XML tag

Catch and report the error when the XML contains an unrecognized tag name.

```ssl
:PROCEDURE ParseXmlWithErrorHandling;
	:DECLARE sXml, vResult, oErr;

	sXml := "<person>John</person>";

	:TRY;
		vResult := FromXml(sXml);
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("Parse failed: " + oErr:Description);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ParseXmlWithErrorHandling");
```

[`ErrorMes`](ErrorMes.md) displays:

```text
Parse failed: Unknown tag <person> in XML structure!
```

## Related

- [`ToXml`](ToXml.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`SSLExpando`](../classes/SSLExpando.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
- [`boolean`](../types/boolean.md)
- [`date`](../types/date.md)
