---
title: "RunDS"
summary: "Executes a data source by name or GUID and returns the result in the requested format."
id: ssl.function.runds
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RunDS

Executes a data source by name or GUID and returns the result in the requested format.

`RunDS` validates that the data source name is a string, optionally accepts an [array](../types/array.md) of arguments for the target data source, and can convert [`SSLDataset`](../classes/SSLDataset.md) results to an [array](../types/array.md), XML string, dataset handle, or [`SSLDataset`](../classes/SSLDataset.md) object. If the data source returns some other value type, `RunDS` returns that value unchanged.

## When to use

- When you need to execute a published data source from SSL instead of embedding the query directly in your script.
- When you want the same data source result as a plain [array](../types/array.md), XML string, dataset handle, or [`SSLDataset`](../classes/SSLDataset.md).
- When you need to call a data source by GUID instead of by its category-qualified name.

## Syntax

```ssl
RunDS(sDataSourceName, [aParameters], [vReturnType])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDataSourceName` | [string](../types/string.md) | yes | — | The data source to execute. A regular name is passed through as written. A GUID string is resolved to a data source name before execution. |
| `aParameters` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Optional array of argument values for the target data source. If supplied, it must be an array. |
| `vReturnType` | [boolean](../types/boolean.md) or [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Controls how an [`SSLDataset`](../classes/SSLDataset.md) result is returned. [`.T.`](../literals/true.md) maps to XML, [`.F.`](../literals/false.md) maps to array, and strings are matched case-insensitively after trimming. Omitting the argument returns an array. |

## Returns

**any** — The data source result. When the result is an [`SSLDataset`](../classes/SSLDataset.md), the value is converted based on `vReturnType` as shown below; otherwise the value is returned as-is.

| `vReturnType` value | Returned value |
|--------------------|----------------|
| omitted | [array](../types/array.md) |
| [`.F.`](../literals/false.md) | [array](../types/array.md) |
| [`.T.`](../literals/true.md) | [string](../types/string.md) containing XML |
| `"array"` | [array](../types/array.md) |
| `"xml"` | [string](../types/string.md) containing XML |
| `"dataset"` | dataset handle |
| `"ssldataset"` | [`SSLDataset`](../classes/SSLDataset.md) |
| any other string | [array](../types/array.md) |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDataSourceName` is not a string. | `Argument 'sDataSourceName' must be a string` |
| `aParameters` is supplied but is not an array. | `Argument 'aParameters' must be NIL or an array` |
| `sDataSourceName` is a GUID that does not resolve to a stored data source. | `Data source with id: {dataSourceId} doesn't exist in the database.` |

## Best practices

!!! success "Do"
    - Pass a string data source name or GUID and validate external input before calling `RunDS`.
    - Pass arguments as an [array](../types/array.md) when the data source expects parameters.
    - Specify `vReturnType` explicitly when callers depend on XML, a dataset handle, or an [`SSLDataset`](../classes/SSLDataset.md).
    - Use [`GetDSParameters`](GetDSParameters.md) when you need to inspect the published parameter list before building the argument array.

!!! failure "Don't"
    - Pass a scalar, object, or other non-array value as `aParameters`. `RunDS` rejects it immediately.
    - Assume every data source result is converted. Conversion rules only apply when the data source returned an [`SSLDataset`](../classes/SSLDataset.md).
    - Rely on unknown `vReturnType` strings to preserve the original result format. For [`SSLDataset`](../classes/SSLDataset.md) results, unrecognized strings fall back to an array.

## Caveats

- `RunDS` trims the incoming data source name before execution.
- String `vReturnType` values are lowercased and trimmed before matching.

## Examples

### Return the default array result

Call a data source with no arguments and iterate over the returned array to display each row's first column.

```ssl
:PROCEDURE LoadActiveStatuses;
    :DECLARE aStatuses, nIndex;

    aStatuses := RunDS("Administration.ActiveStatusList");

    :FOR nIndex := 1 :TO ALen(aStatuses);
        UsrMes("Status: " + LimsString(aStatuses[nIndex, 1]));
        /* Displays: Status: <value>;
    :NEXT;

    :RETURN aStatuses;
:ENDPROC;

/*
Example call
;
DoProc("LoadActiveStatuses");
```

### Pass arguments and keep the result as SSLDataset

Execute a data source with a filter parameter, keep the result as an [`SSLDataset`](../classes/SSLDataset.md) for further processing, and report the row count.

```ssl
:PROCEDURE LoadSamplesByStatus;
    :PARAMETERS sStatus;
    :DEFAULT sStatus, "Logged";
    :DECLARE oDataset, aRows;

    oDataset := RunDS("Laboratory.SampleSearch", {sStatus}, "ssldataset");
    aRows := oDataset:ToArray();

    :IF ALen(aRows) == 0;
        UsrMes("No samples returned");
        :RETURN oDataset;
    :ENDIF;

    UsrMes("Loaded " + LimsString(ALen(aRows)) + " sample rows");
    /* Displays: Loaded <n> sample rows;

    :RETURN oDataset;
:ENDPROC;

/*
Example call
;
DoProc("LoadSamplesByStatus", {"Logged"});
```

### Request XML output from a GUID-identified data source

Pass a GUID string as the data source name and request XML output. The GUID is resolved to a stored data source name before execution.

```ssl
:PROCEDURE ExportAuditDataXml;
    :PARAMETERS sDataSourceId;
    :DECLARE sXml, oErr;

    :TRY;
        sXml := RunDS(sDataSourceId,, .T.);

        :IF Empty(sXml);
            UsrMes("The data source returned no XML payload");
            :RETURN "";
        :ENDIF;

        :RETURN sXml;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes(oErr:Description);
        /* Displays on failure: error description;
        :RETURN "";
    :ENDTRY;
:ENDPROC;

/*
Example call
;
DoProc("ExportAuditDataXml", {"a1b2c3d4-e5f6-7890-abcd-ef1234567890"});
```

## Related

- [`GetDSParameters`](GetDSParameters.md)
- [`GetSSLDataset`](GetSSLDataset.md)
- [`SSLDataset`](../classes/SSLDataset.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
