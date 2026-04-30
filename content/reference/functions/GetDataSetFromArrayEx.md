---
title: "GetDataSetFromArrayEx"
summary: "Generates a dataset XML string from array values, with control over field definitions, table name, header output, and schema output."
id: ssl.function.getdatasetfromarrayex
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDataSetFromArrayEx

Generates a dataset XML string from array values, with control over field definitions, table name, header output, and schema output.

`GetDataSetFromArrayEx` is the configurable form of [`GetDataSetFromArray`](GetDataSetFromArray.md). It accepts the row values, optional field definitions, a table name, and flags that control whether the XML declaration/header and dataset schema are included.

If `aArrayFields` is omitted, [`NIL`](../literals/nil.md), or empty, the function generates default field names such as `Field1`, `Field2`, and so on. When `bIncludeSchema` is enabled, field definitions can also carry type metadata. If `aArrayOfValues` contains scalar elements instead of row arrays, each scalar is treated as a single-column row during dataset construction.

## When to use

- When you need dataset XML from in-memory values but cannot use the fixed defaults of [`GetDataSetFromArray`](GetDataSetFromArray.md).
- When the consumer needs a specific table name.
- When you need schema output in addition to the dataset XML.
- When you want to supply explicit field definitions instead of relying on generated `FieldN` names.

## Syntax

```ssl
GetDataSetFromArrayEx(aArrayOfValues, [aArrayFields], [sTableName], [bIncludeHeader], [bIncludeSchema])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aArrayOfValues` | [array](../types/array.md) | yes | — | Values to convert into dataset rows. In the common case, each element is a row array. Scalar elements are treated as single-column rows. |
| `aArrayFields` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Optional field definitions. Each element may be a field name string or an array definition such as `{"field_name", "S", 50}`. When omitted, [`NIL`](../literals/nil.md), or empty, the function generates `Field1`, `Field2`, and so on. |
| `sTableName` | [string](../types/string.md) | no | `Table` | Table name used in the generated dataset when the argument is omitted or [`NIL`](../literals/nil.md). If an empty string is passed, the runtime normalizes it to `TABLE`. |
| `bIncludeHeader` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether to include the XML header/declaration in the output. |
| `bIncludeSchema` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Whether to include schema metadata in the output. Field type metadata only matters when schema output is enabled. |

## Returns

**[string](../types/string.md)** — An XML dataset string built from the supplied values and output options.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aArrayOfValues` is [`NIL`](../literals/nil.md). | `The values array parameter is null` |
| Array preparation fails. | `Preparing the input arrays generated an error : {message}` |

## Best practices

!!! success "Do"
    - Pass a two-dimensional array when each inner array represents one row.
    - Provide explicit field definitions when downstream consumers depend on stable column names or schema metadata.
    - Enable `bIncludeSchema` only when the receiving system actually needs schema information.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `aArrayOfValues` and expect an empty result. The function raises an error instead.
    - Assume mismatched field counts will be rejected with a dedicated validation error. Extra field names or extra row values are trimmed to the smaller available column count.
    - Use this function when the fixed defaults from [`GetDataSetFromArray`](GetDataSetFromArray.md) already match your needs. The wrapper is simpler for that case.

## Caveats

- If `aArrayOfValues` is empty and `bIncludeSchema` is [`.F.`](../literals/false.md), the function returns an empty string.
- When the row width and field-definition count differ, the generated dataset uses the smaller column count.
- Omitting `sTableName` and passing `""` are not treated the same way: omitted or [`NIL`](../literals/nil.md) uses `Table`, while an empty string is normalized to `TABLE`.

## Examples

### Export rows with explicit field names

Passes a named table, explicit field definitions, header enabled, and schema disabled to produce a minimal XML dataset string.

```ssl
:PROCEDURE BuildUserDatasetXml;
	:DECLARE aRows, aFields, sXml;

	aRows := {
		{"USR001", "Alice Johnson", "alice.johnson@example.com"},
		{"USR002", "Bob Smith", "bob.smith@example.com"}
	};

	aFields := {"user_id", "user_name", "email"};

	sXml := GetDataSetFromArrayEx(aRows, aFields, "users", .T., .F.);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("BuildUserDatasetXml");
```

### Include schema with typed field definitions

Uses array-form field definitions to supply type metadata alongside column names, enabling schema output for a dataset with numeric and date columns.

```ssl
:PROCEDURE BuildResultDatasetWithSchema;
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

	sXml := GetDataSetFromArrayEx(aRows, aFields, "lab_results", .T., .T.);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("BuildResultDatasetWithSchema");
```

### Build a schema-only dataset template

Passes an empty row array with schema enabled to produce an XML dataset that contains only the field definitions — useful as an import template structure.

```ssl
:PROCEDURE BuildImportTemplateXml;
	:DECLARE aRows, aFields, sXml;

	aRows := {};

	aFields := {
		{"sample_id", "S", 20},
		{"status", "S", 12},
		{"received_date", "D"}
	};

	sXml := GetDataSetFromArrayEx(aRows, aFields, "sample_import", .T., .T.);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("BuildImportTemplateXml");
```

## Related

- [`GetDataSetFromArray`](GetDataSetFromArray.md)
- [`GetDataSetXMLFromArray`](GetDataSetXMLFromArray.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
