---
title: "GetDataSetXMLFromArray"
summary: "Generates dataset XML from in-memory values, field definitions, and output flags."
id: ssl.function.getdatasetxmlfromarray
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDataSetXMLFromArray

Generates dataset XML from in-memory values, field definitions, and output flags.

`GetDataSetXMLFromArray` converts array data into an XML dataset string. You can control the table name, whether the XML output includes header information, and whether schema metadata is emitted. The function requires `aArrayOfValues`; when that argument is [`NIL`](../literals/nil.md), it raises an error before any XML is built.

Unlike [`GetDataSetFromArrayEx`](GetDataSetFromArrayEx.md), this function does not add the extra field-name normalization step before calling the XML generator. Use it when you want direct control over the XML-oriented form.

## When to use

- When another system needs dataset XML rather than an [`SSLDataset`](../classes/SSLDataset.md) object.
- When you need to control table name, header output, and schema output in one call.
- When you already have explicit field definitions and want to serialize rows
  directly.
- When you need a schema-only XML template with no data rows yet.

## Syntax

```ssl
GetDataSetXMLFromArray(aArrayOfValues, [aArrayFields], [sTableName], [bIncludeHeader], [bIncludeSchema])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `aArrayOfValues` | [array](../types/array.md) | yes | — | Values to serialize. In the common case, each element is a row array. If an element is a scalar value, the runtime wraps it as a single-column row. |
| `aArrayFields` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Field definitions for the output columns. Each element may be a field name string or a definition array such as `{"sample_id", "S", 20}` or `{"result_value", "N", 10, 2}`. |
| `sTableName` | [string](../types/string.md) | no | `Table` | Table name used when the argument is omitted or [`NIL`](../literals/nil.md). If you pass an empty string, the generated table name is normalized to `TABLE`. |
| `bIncludeHeader` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether to include header information in the generated XML. |
| `bIncludeSchema` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Whether to include schema metadata in the generated XML. |

## Returns

**[string](../types/string.md)** — XML produced from the supplied rows, fields, and output options.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aArrayOfValues` is [`NIL`](../literals/nil.md). | `The values array parameter is null` |
| Array preparation fails. | `Preparing the input arrays generated an error : {message}` |

## Best practices

!!! success "Do"
    - Pass rows as a two-dimensional array when you are exporting tabular data.
    - Supply explicit field definitions when column names or schema details must stay stable.
    - Turn on `bIncludeSchema` only when the receiving system actually needs schema metadata.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `aArrayOfValues` and expect an empty result. The function raises an error instead.
    - Assume this function will add the same field-name defaults as [`GetDataSetFromArrayEx`](GetDataSetFromArrayEx.md). If you need that convenience, use the wrapper.
    - Rely on the default table name when downstream consumers care about the table identifier.

## Caveats

- If `aArrayOfValues` is empty and `bIncludeSchema` is [`.F.`](../literals/false.md), the function returns an empty string.
- When schema output is disabled, generated columns are treated as string columns.
- When schema output is enabled, field definitions can carry type metadata: `"S"` for string, `"N"` for numeric, and `"D"` for date.
- If a field definition only supplies the field name, the runtime infers the column type from the first non-null value it finds in that column.
- If row width and field-definition count do not match, the generated output is trimmed to the smaller available column count.
- [`NIL`](../literals/nil.md) values and blank strings in row data are emitted as empty dataset values.

## Examples

### Export rows with explicit field names

Builds an XML dataset from three hard-coded rows with explicit column names, header enabled, and schema disabled.

```ssl
:PROCEDURE BuildSampleResultsXml;
	:DECLARE aRows, aFields, sXml;

	aRows := {
		{"LAB-001", "pH", 7.1},
		{"LAB-002", "pH", 6.9},
		{"LAB-003", "pH", 7.3}
	};

	aFields := {"sample_id", "test_code", "result_value"};

	sXml := GetDataSetXMLFromArray(aRows, aFields, "sample_results", .T., .F.);

	UsrMes(sXml);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("BuildSampleResultsXml");
```

[`UsrMes`](UsrMes.md) displays:

```text
<?xml version="1.0" standalone="yes" ?>
<DataSet><sample_results><sample_id>LAB-001</sample_id><test_code>pH</test_code><result_value>7.1</result_value></sample_results><sample_results><sample_id>LAB-002</sample_id><test_code>pH</test_code><result_value>6.9</result_value></sample_results><sample_results><sample_id>LAB-003</sample_id><test_code>pH</test_code><result_value>7.3</result_value></sample_results></DataSet>
```

### Include schema with typed field definitions

Passes typed field definitions and sets `bIncludeSchema` to [`.T.`](../literals/true.md) to embed column type metadata alongside the row data in the returned XML.

```ssl
:PROCEDURE BuildResultXmlWithSchema;
	:DECLARE aRows, aFields, sXml;

	aRows := {
		{"LAB-001", 7.12, CToD("04/18/2026")},
		{"LAB-002", 6.98, CToD("04/19/2026")}
	};

	aFields := {
		{"sample_id", "S", 20},
		{"result_value", "N", 10, 2},
		{"analysis_date", "D"}
	};

	sXml := GetDataSetXMLFromArray(aRows, aFields, "lab_results", .T., .T.);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("BuildResultXmlWithSchema");
```

### Build a schema-only XML template

Passes an empty row array with schema enabled to generate an XML dataset that contains only field definitions — useful as a typed import template.

```ssl
:PROCEDURE BuildImportTemplateXml;
	:DECLARE aRows, aFields, sXml;

	aRows := {};

	aFields := {
		{"sample_id", "S", 20},
		{"status", "S", 12},
		{"received_date", "D"}
	};

	sXml := GetDataSetXMLFromArray(aRows, aFields, "sample_import", .T., .T.);

	UsrMes(sXml);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("BuildImportTemplateXml");
```

[`UsrMes`](UsrMes.md) displays:

```text
<?xml version="1.0" standalone="yes" ?>
<DataSet><xs:schema id="DataSet" xmlns="" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:msdata="urn:schemas-microsoft-com:xml-msdata"><xs:element name="DataSet" msdata:IsDataSet="true"><xs:complexType><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="sample_import"><xs:complexType><xs:sequence><xs:element name="sample_id" type="xs:string" minOccurs="0"/><xs:element name="status" type="xs:string" minOccurs="0"/><xs:element name="received_date" type="xs:dateTime" minOccurs="0"/></xs:sequence></xs:complexType></xs:element></xs:choice></xs:complexType></xs:element></xs:schema></DataSet>
```

## Related

- [`GetDataSetFromArray`](GetDataSetFromArray.md)
- [`GetDataSetFromArrayEx`](GetDataSetFromArrayEx.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
