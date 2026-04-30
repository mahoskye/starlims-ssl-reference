---
title: "LimsTypeEx"
summary: "Returns the public SSL type name for a value."
id: ssl.function.limstypeex
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsTypeEx

Returns the public SSL type name for a value.

Use `LimsTypeEx` when you need a readable type label such as `STRING`, `NUMERIC`, or `ARRAY`. It accepts any SSL value, including [`NIL`](../literals/nil.md), and returns an uppercase string describing the value's runtime type.

## When to use

- When you need to branch logic based on the runtime type of a value.
- When you want to log or display a readable SSL type name.
- When you are validating dynamic input before applying type-specific logic.

## Syntax

```ssl
LimsTypeEx(vSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vSource` | any | yes | — | Value to inspect. |

## Returns

**[string](../types/string.md)** — An uppercase SSL type name.

`LimsTypeEx` returns one of these values:

| Input value | Return value |
|-------------|--------------|
| [`NIL`](../literals/nil.md) | [`NIL`](../literals/nil.md) |
| String | `STRING` |
| Number | `NUMERIC` |
| Boolean | `LOGIC` |
| Date | `DATE` |
| Array | `ARRAY` |
| Code block | `CODEBLOCK` |
| Object values exposed as SSL objects | `OBJECT` |
| Other unsupported or custom values | `SSLVALUE` |

For most application code, the standard values above are the ones you will use. If a value does not map to one of the documented SSL categories, `LimsTypeEx` may return `SSLVALUE`.

## Best practices

!!! success "Do"
    - Compare the return value against the documented uppercase names such as `STRING`, `NUMERIC`, and [`NIL`](../literals/nil.md).
    - Use `LimsTypeEx` before type-specific operations when input may vary at runtime.
    - Handle [`NIL`](../literals/nil.md) explicitly when blank or missing input is meaningful to your logic.

!!! failure "Don't"
    - Assume every incoming value is already the type you expect.
    - Infer a value's type from how it prints or from user-facing formatting.
    - Treat `LimsTypeEx` as a validator for business rules; it reports type, not whether the value is acceptable for your process.

## Examples

### Inspect the type of a single value

Use `LimsTypeEx` to report the type of a single value. The string `"Sample Text"` returns `"STRING"`.

```ssl
:PROCEDURE ShowValueType;
	:DECLARE sValue, sType;

	sValue := "Sample Text";
	sType := LimsTypeEx(sValue);

	UsrMes("Value type: " + sType);
:ENDPROC;

/* Usage;
DoProc("ShowValueType");
```

[`UsrMes`](UsrMes.md) displays:

```
Value type: STRING
```

### Handle mixed values by type

Loop through an array of mixed values and branch on the returned type name to build a summary array. No messaging is called — the result array can be inspected or passed to a reporting step.

```ssl
:PROCEDURE DescribeValues;
	:DECLARE aValues, aSummary, nIndex, sType;

	aValues := {"Batch-1001", 42.5, .T., Today(), NIL};
	aSummary := {};

	:FOR nIndex := 1 :TO ALen(aValues);
		sType := LimsTypeEx(aValues[nIndex]);

		:BEGINCASE;
		:CASE sType == "STRING";
			AAdd(aSummary, "Text value");
			:EXITCASE;
		:CASE sType == "NUMERIC";
			AAdd(aSummary, "Numeric value");
			:EXITCASE;
		:CASE sType == "LOGIC";
			AAdd(aSummary, "Boolean value");
			:EXITCASE;
		:CASE sType == "DATE";
			AAdd(aSummary, "Date value");
			:EXITCASE;
		:CASE sType == "NIL";
			AAdd(aSummary, "Missing value");
			:EXITCASE;
		:OTHERWISE;
			AAdd(aSummary, "Other type: " + sType);
			:EXITCASE;
		:ENDCASE;
	:NEXT;

	:RETURN aSummary;
:ENDPROC;

/* Usage;
DoProc("DescribeValues");
```

### Reject unexpected input types before numeric logic

Check each parameter's type before performing numeric addition. If either argument is not numeric, an error is shown and [`NIL`](../literals/nil.md) is returned.

```ssl
:PROCEDURE AddMeasuredValue;
	:PARAMETERS nCurrentTotal, nIncrement;
	:DECLARE sCurrentType, sIncrementType;

	sCurrentType := LimsTypeEx(nCurrentTotal);
	sIncrementType := LimsTypeEx(nIncrement);

	:IF !(sCurrentType == "NUMERIC");
		ErrorMes("Current total must be numeric.");
		:RETURN NIL;
	:ENDIF;

	:IF !(sIncrementType == "NUMERIC");
		ErrorMes("Increment must be numeric.");
		:RETURN NIL;
	:ENDIF;

	:RETURN nCurrentTotal + nIncrement;
:ENDPROC;

/* Usage;
DoProc("AddMeasuredValue", {10.5, 3.2});
```

## Related

- [`LimsType`](LimsType.md)
- [`string`](../types/string.md)
