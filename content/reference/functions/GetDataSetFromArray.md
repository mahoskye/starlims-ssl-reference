---
title: "GetDataSetFromArray"
summary: "Builds a dataset XML string from an array of values and an optional array of field names."
id: ssl.function.getdatasetfromarray
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDataSetFromArray

Builds a dataset XML string from an array of values and an optional array of field names.

`GetDataSetFromArray` is the simple wrapper around [`GetDataSetFromArrayEx`](GetDataSetFromArrayEx.md). It always uses the table name `TABLE`, includes the dataset header, and does not include schema metadata. Pass a two-dimensional array when each inner array represents one row. If `aArrayFields` is omitted or empty, the function generates default column names such as `Field1`, `Field2`, and so on.

If `aArrayOfValues` is [`NIL`](../literals/nil.md), the function raises an error before any dataset is built. If `aArrayOfValues` is empty, or if the effective field list is empty, the function returns an empty string.

## When to use

- When you need a quick dataset XML string from in-memory rows.
- When a consumer expects the default `TABLE` dataset name with a header.
- When field names can be supplied explicitly or safely auto-generated.

## Syntax

```ssl
GetDataSetFromArray(aArrayOfValues, [aArrayFields])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `aArrayOfValues` | [array](../types/array.md) | yes | — | Values to convert into dataset rows. In the common case, each element is a row array. |
| `aArrayFields` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Optional field names. When omitted, [`NIL`](../literals/nil.md), or empty, the function generates `Field1`, `Field2`, and so on. |

## Returns

**[string](../types/string.md)** — An XML dataset string generated with header output enabled and schema output disabled.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aArrayOfValues` is [`NIL`](../literals/nil.md). | `The values array parameter is null` |

## Best practices

!!! success "Do"
    - Pass a two-dimensional array so each inner array cleanly maps to one dataset row.
    - Provide explicit field names when column meaning matters to downstream consumers.
    - Use [`GetDataSetFromArrayEx`](GetDataSetFromArrayEx.md) instead when you need control over table name, header, or schema output.

!!! failure "Don't"
    - Pass a [`NIL`](../literals/nil.md) values array and expect an empty result. The function raises an error instead.
    - Rely on auto-generated field names when the dataset will be shared or imported elsewhere. Generic names are harder to interpret.
    - Use this wrapper when you need schema metadata or a custom table name. Those options are fixed here.

## Caveats

- If the field count does not match the row width, the output is trimmed to the available columns rather than raising a dedicated mismatch error.
- Empty strings in row values are emitted as empty database values in the generated dataset.

## Examples

### Convert tabular rows with explicit field names

Builds an XML dataset from three hard-coded lab result rows, passing explicit column names to control the field names in the output.

```ssl
:PROCEDURE BuildResultDataset;
    :DECLARE aRows, aFields, sDataset;

    aRows := {
        {"LAB-001", "pH", 7.1},
        {"LAB-002", "pH", 6.9},
        {"LAB-003", "pH", 7.3}
    };

    aFields := {"sample_id", "test_code", "result_value"};

    sDataset := GetDataSetFromArray(aRows, aFields);

    UsrMes(sDataset);
    :RETURN sDataset;
:ENDPROC;

/* Usage;
DoProc("BuildResultDataset");
```

[`UsrMes`](UsrMes.md) displays:

```text
<?xml version="1.0"?><DATASET><TABLE><sample_id>LAB-001</sample_id><test_code>pH</test_code><result_value>7.1</result_value></TABLE><TABLE><sample_id>LAB-002</sample_id><test_code>pH</test_code><result_value>6.9</result_value></TABLE><TABLE><sample_id>LAB-003</sample_id><test_code>pH</test_code><result_value>7.3</result_value></TABLE></DATASET>
```

### Let the function generate field names

Omits `aArrayFields` so the function generates `Field1`, `Field2`, `Field3` automatically, then parses the returned XML string into a dataset to report the row count.

```ssl
:PROCEDURE BuildAnonymousDataset;
    :DECLARE aRows, sDataset, oDataset;

    aRows := {
        {"A100", "Released", "2026-04-18"},
        {"A101", "Pending", "2026-04-19"}
    };

    sDataset := GetDataSetFromArray(aRows);
    oDataset := SSLDataset{sDataset, .T.};

    UsrMes("Generated " + LimsString(oDataset:RecordCount) + " rows");
    :RETURN sDataset;
:ENDPROC;

/* Usage;
DoProc("BuildAnonymousDataset");
```

[`UsrMes`](UsrMes.md) displays:

```text
Generated 2 rows
```

### Build a dataset from query results

Runs a parameterized query via [`LSelect1`](LSelect1.md), then converts the result array into a dataset XML string with named columns.

```ssl
:PROCEDURE BuildPendingOrderDataset;
    :DECLARE aRows, aFields, sDataset;

    aRows := LSelect1("
        SELECT ordno, testcode, status
        FROM ordtask
        WHERE status = ?
        ORDER BY ordno
    ",, {"Pending"});

    aFields := {"ordno", "testcode", "status"};
    sDataset := GetDataSetFromArray(aRows, aFields);

    :RETURN sDataset;
:ENDPROC;

/* Usage;
DoProc("BuildPendingOrderDataset");
```

## Related

- [`GetDataSetFromArrayEx`](GetDataSetFromArrayEx.md)
- [`GetDataSetXMLFromArray`](GetDataSetXMLFromArray.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
