---
title: "ArrayToTVP"
summary: "Convert a one-dimensional array into a table-valued parameter object."
id: ssl.function.arraytotvp
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ArrayToTVP

Convert a one-dimensional array into a table-valued parameter object.

`ArrayToTVP` creates a TVP object from a flat SSL array so it can be passed to
database code that supports table-valued parameters. The function resolves the
target database from `sConnectionName` when that argument is a string. If
`sConnectionName` is omitted or is not a string, the default database is used.

The function accepts only one-dimensional arrays. If the array has at least one element and the first element is itself an array, the call fails. Empty arrays are allowed.

Runtime support is limited to string and integer TVPs:

- If `sDataType` is omitted or is not a string, the function infers the type
  from the array contents.
- `"INT"` selects integer TVP behavior.
- `"DOUBLE"` and `"DATE"` are recognized strings, but TVP creation still fails
  because the underlying TVP implementations support only integer and string
  payloads.
- Any other string value falls back to string TVP behavior.

All non-[`NIL`](../literals/nil.md) elements must match the chosen TVP type. Integer TVPs accept only whole-number values that fit the supported integer range. Mixed non-[`NIL`](../literals/nil.md) element types fail.

## When to use

- When you need to pass a list of values into database code without building
  the list into a SQL string.
- When the receiving database side expects a TVP-like parameter shape.
- When the same calling code may target either SQL Server or Oracle.

## Syntax

```ssl
ArrayToTVP(aValues, [sDataType], [sConnectionName])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aValues` | [array](../types/array.md) | yes | — | Source array. Must be one-dimensional. Empty arrays are allowed. |
| `sDataType` | [string](../types/string.md) | no | inferred | Optional TVP type hint. `"INT"` forces integer handling. `"DOUBLE"` and `"DATE"` are recognized but fail during TVP construction. Any other string falls back to string handling. Non-string values are treated the same as omission. |
| `sConnectionName` | [string](../types/string.md) | no | default database | Optional database connection name. Non-string values are treated the same as omission. |

## Returns

**[object](../types/object.md)** — TVP object created for the selected database platform.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aValues` is not an array. | `Argument 'aValues' must be an array` |
| `aValues` has at least one element and the first element is an array. | `Argument 'aValues' must be a one-dimensional array` |
| `sConnectionName` names an unknown database. | `The provider name: {sConnectionName} not found.` |
| Database resolution is not available. | `The internal database collection is null` |
| The resolved database platform is not `SQL` or `ORACLE`. | `Unsupported database: {dbType}` |
| `sDataType` or inferred content selects an unsupported TVP type. | `Unsupported data type: Double` or `Unsupported data type: Date` |
| Non-[`NIL`](../literals/nil.md) elements do not all match the chosen TVP type. | `Mixed values are not supported` |
| An integer TVP receives a non-integer numeric element. | `Only integer numbers are supported for TVP. Index: <N>` |

## Best practices

!!! success "Do"
    - Pass a flat array whose non-[`NIL`](../literals/nil.md) elements are all strings or all whole
      numbers.
    - Omit `sDataType` when the array contents already make the intended type
      obvious.
    - Pass `sConnectionName` explicitly when the TVP must target a non-default
      database.
    - Validate numeric input before calling `ArrayToTVP` if fractional values
      might be present.

!!! failure "Don't"
    - Pass nested arrays. `ArrayToTVP` is for one-dimensional input.
    - Assume `"DOUBLE"` or `"DATE"` are usable output types. They are
      recognized names, but TVP creation still fails.
    - Mix strings and numbers in one TVP array unless you expect the call
      to fail.
    - Assume every unknown `sDataType` string raises an error. Unknown
      strings fall back to string TVP behavior.

## Caveats

- Empty arrays are allowed. With omitted type information, an empty array
  defaults to string TVP behavior.
- [`NIL`](../literals/nil.md) elements are allowed as long as the non-[`NIL`](../literals/nil.md) elements still match the
  chosen TVP type.
- The one-dimensional check is explicit only for the first element. Other
  unsupported element shapes fail later through the normal mixed-type checks.
- This function only creates the TVP object. How that object is bound to a
  query or procedure depends on the database call that receives it.

## Examples

### Create an integer TVP

Builds an integer TVP by passing `"INT"` as the type hint, then checks that the result is non-empty before proceeding.

```ssl
:PROCEDURE BuildIntegerTVP;
	:DECLARE aOrderIds, oTVP;

	aOrderIds := {1001, 1002, 1003};
	oTVP := ArrayToTVP(aOrderIds, "INT");

	:IF Empty(oTVP);
		UsrMes("TVP was not created");
	:ELSE;
		UsrMes("Integer TVP created");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("BuildIntegerTVP");
```

### Let the function infer a string TVP

Omits the type hint so the function infers string behavior from the array contents. A [`NIL`](../literals/nil.md) element is accepted as long as the non-[`NIL`](../literals/nil.md) elements are all strings.

```ssl
:PROCEDURE BuildStringTVP;
	:DECLARE aSampleIds, oTVP;

	aSampleIds := {"SMP-0001", "SMP-0002", NIL, "SMP-0004"};
	oTVP := ArrayToTVP(aSampleIds);

	:IF Empty(oTVP);
		UsrMes("String TVP was not created");
	:ELSE;
		UsrMes("String TVP created for sample IDs");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("BuildStringTVP");
```

### Target a specific connection and catch errors

Passes a named connection to direct the TVP at a non-default database, and wraps the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to handle resolution failures.

```ssl
:PROCEDURE BuildRemoteTVP;
	:DECLARE aIds, oTVP, oErr;

	aIds := {2001, 2002, 2003};

	:TRY;
		oTVP := ArrayToTVP(aIds, "INT", "LABDATA");
		UsrMes("Remote TVP created");

	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("TVP creation failed: " + oErr:Description);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("BuildRemoteTVP");
```

On failure, [`ErrorMes`](ErrorMes.md) displays:

```
TVP creation failed: <error message>
```

## Related

- [`ArrayNew`](ArrayNew.md)
- [`BuildArray`](BuildArray.md)
- [`BuildArray2`](BuildArray2.md)
- [`SQLExecute`](SQLExecute.md)
- [`array`](../types/array.md)
- [`object`](../types/object.md)
