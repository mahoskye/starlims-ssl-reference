---
title: "XmlDomToUdObject"
summary: "Converts an XML string into a dynamic object tree."
id: ssl.function.xmldomtoudobject
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# XmlDomToUdObject

Converts an XML string into a dynamic object tree.

`XmlDomToUdObject` loads a non-empty XML string and returns an [`SSLExpando`](../types/object.md) that represents the document's root element. Each returned object records the element name in `XmlType`, exposes attributes as properties, stores leaf text in `Value`, and exposes child elements both as a singular property and as a `<name>Collection` array.

## When to use

- When you need to traverse XML with normal object-property access in SSL.
- When you need both element attributes and child elements preserved in one dynamic object tree.
- When you want repeated sibling elements grouped into a predictable collection property.

## Syntax

```ssl
XmlDomToUdObject(sXml, [bPreserveWhitespace])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sXml` | [string](../types/string.md) | yes | — | XML text to parse. It must be a non-empty string. |
| `bPreserveWhitespace` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), whitespace-only text nodes are preserved while loading the XML. |

## Returns

**[object](../types/object.md)** — An [`SSLExpando`](../classes/SSLExpando.md) for the XML root element.

Returned objects follow these rules:

- `XmlType` contains the current element name.
- Attributes become properties on the same object.
- A leaf element gets a `Value` property containing its text, or `""` when the element has no children.
- Each child element name is exposed twice:
  - `<name>` holds the first child object with that name.
  - `<name>Collection` holds an array of all child objects with that name.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sXml` is [`NIL`](../literals/nil.md), empty, or not a string. | `Argument 'sXml' cannot be empty.` |
| `sXml` is malformed XML. | A runtime error from the XML loader. |

## Best practices

!!! success "Do"
    - Wrap calls in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the XML comes from an external or user-controlled source.
    - Use the `<name>Collection` property when an element may appear more than once.
    - Set `bPreserveWhitespace` to [`.T.`](../literals/true.md) only when whitespace-only text content is part of the data you need to keep.

!!! failure "Don't"
    - Assume repeated sibling elements are returned as a scalar value. The singular property keeps only the first matching child.
    - Assume an attribute named `value` will appear as `Value`. The function prefixes that attribute name to avoid colliding with the generated text-value property.
    - Pass [`NIL`](../literals/nil.md), `""`, or a non-string value for `sXml`. Those inputs raise the documented argument error.

## Caveats

- Attribute names that contain `:` are surfaced with `_` instead.
- When an attribute name is `value`, the function renames it with an `Attr` prefix to avoid colliding with the generated `Value` property.
- `bPreserveWhitespace` only changes what the XML loader keeps. Whitespace nodes between nested elements are still not exposed as child properties in the returned object tree.
- Non-boolean `bPreserveWhitespace` values behave like the argument was omitted,
  so whitespace preservation stays off.

## Examples

### Read attributes from the root's child element

Parse a simple XML document and read attribute values from the first child.

```ssl
:PROCEDURE ReadConfigXml;
	:DECLARE sXml, oConfig, sAppName, sVersion, sMessage;

	sXml := "<config><application name='SampleApp' version='2.5'/></config>";
	oConfig := XmlDomToUdObject(sXml);

	sAppName := oConfig:application:name;
	sVersion := oConfig:application:version;
	sMessage := oConfig:XmlType + ": " + sAppName + " v" + sVersion;

	UsrMes(sMessage);

	:RETURN oConfig;
:ENDPROC;

/* Usage;
DoProc("ReadConfigXml");
```

[`UsrMes`](UsrMes.md) displays:

```
config: SampleApp v2.5
```

### Handle repeated child elements with `Collection`

Use the generated `testCollection` array to process every repeated `<test>`
element.

```ssl
:PROCEDURE ReadTestResults;
	:DECLARE sXml, oOrder, aTests, oTest, sSummary, nIndex;

	sXml :=
		"
<order>
    <tests>
        <test code='pH'>7.1</test>
        <test code='Cond'>320</test>
    </tests>
</order>
";
	oOrder := XmlDomToUdObject(sXml);
	aTests := oOrder:tests:testCollection;
	sSummary := "";

	:FOR nIndex := 1 :TO ALen(aTests);
		oTest := aTests[nIndex];

		:IF !Empty(sSummary);
			sSummary := sSummary + ", ";
		:ENDIF;

		sSummary := sSummary + oTest:code + "=" + oTest:Value;
	:NEXT;

	UsrMes(sSummary);

	:RETURN oOrder;
:ENDPROC;

/* Usage;
DoProc("ReadTestResults");
```

[`UsrMes`](UsrMes.md) displays:

```
pH=7.1, Cond=320
```

### Preserve whitespace-only text when it matters

Compare the default behavior with `bPreserveWhitespace` enabled for an element whose content is only spaces.

```ssl
:PROCEDURE PreservePadding;
	:DECLARE sXml, oDefault, oExact, nDefaultLen, nExactLen;

	sXml := "<token><padding>   </padding><value>ABC</value></token>";

	oDefault := XmlDomToUdObject(sXml);
	oExact := XmlDomToUdObject(sXml, .T.);

	nDefaultLen := Len(oDefault:padding:Value);
	nExactLen := Len(oExact:padding:Value);

	UsrMes("Default padding length: " + LimsString(nDefaultLen));
	UsrMes("Preserved padding length: " + LimsString(nExactLen));

	:RETURN oExact;
:ENDPROC;

/* Usage;
DoProc("PreservePadding");
```

[`UsrMes`](UsrMes.md) displays:

```text
Default padding length: 0
Preserved padding length: 3
```

## Related

- [`FromXml`](FromXml.md)
- [`ToXml`](ToXml.md)
- [`boolean`](../types/boolean.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
