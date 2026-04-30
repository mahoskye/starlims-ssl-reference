---
title: "GetDSParameters"
summary: "Returns an array of parameter key strings for the named data source."
id: ssl.function.getdsparameters
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDSParameters

Returns an array of parameter key strings for the named data source.

The name is trimmed automatically and may be a GUID or a qualified `category.ds_name` string. If `sDsName` is [`NIL`](../literals/nil.md) or cannot be resolved to a known data source, the function raises an error. If the data source exists but has no parameters, it returns an empty array.

## When to use

- When you need to programmatically discover what input parameters are expected by an existing data source, prior to execution.
- When building dynamic forms or integrations that must adapt to different data sources in real-time.
- When validating user or external configurations to ensure all required parameters for the dataset will be supplied.
- When troubleshooting failures in dataset execution, such as missing or unexpected input parameters.

## Syntax

```ssl
GetDSParameters(sDsName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDsName` | [string](../types/string.md) | yes | — | The name or GUID identifier of the data source whose parameters are to be retrieved. |

## Returns

**[array](../types/array.md)** — An array of parameter key strings for the specified data source.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDsName` is [`NIL`](../literals/nil.md). | `Argument cannot be null.` |
| `sDsName` cannot be resolved to a known data source. | `There is no info for data source: {sDsName}` |
| `sDsName` is not a GUID and does not contain a `.` separating category and data source name. | `Data Source name should be: categ_name.ds_name` |

## Best practices

!!! success "Do"
    - Validate data source names before calling.
    - Wrap calls in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the name comes from configuration or user input.
    - Use this function during setup, validation, or configuration-building phases.

!!! failure "Don't"
    - Pass unvalidated raw user input as the data source name.
    - Assume all data source names will resolve to parameters.
    - Call in tight loops — each call performs a database lookup.

## Examples

### List parameter keys for a data source

Retrieves the parameter array for a data source and builds a comma-separated list for display, showing `(none defined)` when the data source has no parameters.

```ssl
:PROCEDURE ListDataSourceParams;
	:DECLARE sDsName, aParams, nCount, nIndex, sParamList;

	sDsName := "Analysis.SampleResults";
	aParams := GetDSParameters(sDsName);
	nCount := ALen(aParams);
	sParamList := "Parameters for " + sDsName + ": ";

	:IF nCount > 0;
		:FOR nIndex := 1 :TO nCount;
			sParamList := sParamList + aParams[nIndex];
			:IF nIndex < nCount;
				sParamList := sParamList + ", ";
			:ENDIF;
		:NEXT;
	:ELSE;
		sParamList := sParamList + "(none defined)";
	:ENDIF;

	UsrMes(sParamList);
	:RETURN aParams;
:ENDPROC;

/* Usage;
DoProc("ListDataSourceParams");
```

[`UsrMes`](UsrMes.md) displays:

```text
Parameters for Analysis.SampleResults: SampleId, StartDate, EndDate
```

### Validate user-supplied parameters before running a data source

Compares the caller-supplied parameter keys against the expected parameters for the data source and reports the first set of unknown keys before running the data source.

```ssl
:PROCEDURE ValidateAndRunSampleDS;
	:PARAMETERS sDataSource, aUserParams;
	:DEFAULT sDataSource, "";
	:DEFAULT aUserParams, {};
	:DECLARE aExpectedParams, sParamKey, bParamValid, nIndex, sErrorMsg, oResult;

	aExpectedParams := GetDSParameters(sDataSource);
	bParamValid := .T.;
	sErrorMsg := "";

	:IF ALen(aUserParams) > 0;
		:FOR nIndex := 1 :TO ALen(aUserParams);
			sParamKey := aUserParams[nIndex, 1];
			:IF AScan(aExpectedParams, sParamKey) == 0;
				bParamValid := .F.;
				sErrorMsg := sErrorMsg + "Invalid parameter: " + sParamKey + ". ";
			:ENDIF;
		:NEXT;
	:ENDIF;

	:IF ! bParamValid;
		/* Displays on failure: validation errors;
		ErrorMes("Parameter validation failed. " + sErrorMsg);
		:RETURN NIL;
	:ENDIF;

	oResult := RunDS(sDataSource);
	:RETURN oResult;
:ENDPROC;

/* Usage;
DoProc("ValidateAndRunSampleDS", {"Analysis.SampleResults", {{"SampleId", "S001"}, {"StartDate", "2024-01-01"}}});
```

## Related

- [`RunDS`](RunDS.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
