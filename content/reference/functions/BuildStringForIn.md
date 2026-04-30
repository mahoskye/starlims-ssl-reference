---
title: "BuildStringForIn"
summary: "Builds a quoted string list for a SQL IN clause from an array."
id: ssl.function.buildstringforin
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# BuildStringForIn

Builds a quoted string list for a SQL `IN` clause from an array.

`BuildStringForIn` converts each array element to text, trims surrounding spaces, escapes embedded single quotes by doubling them, joins the values with `','`, and wraps the result as `('value1','value2')`.

If `aTarget` is [`NIL`](../literals/nil.md) or empty, the function returns the fixed sentinel list `('C7082BA7C83D38CAE98421BE494753931F8B52A8')`. This keeps the generated `IN (...)` clause syntactically valid while making a real match unlikely.

The function always returns literal SQL text. It does not produce positional parameter arrays for database calls such as [`RunSQL`](RunSQL.md), [`LSearch`](LSearch.md), [`LSelect`](LSelect.md), [`LSelect1`](LSelect1.md), [`LSelectC`](LSelectC.md), or [`GetDataSet`](GetDataSet.md).

## When to use

- When you must embed a literal `IN (...)` list into dynamically assembled SQL.
- When array values may contain apostrophes that need SQL string escaping.
- When you want empty input to produce a non-matching sentinel value instead of an empty `IN ()` clause.

## Syntax

```ssl
BuildStringForIn(aTarget)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Array whose values will be converted into one quoted string list for a SQL `IN` clause. |

## Returns

**[string](../types/string.md)** — A parenthesized list of single-quoted values in the format `('value1','value2',...)`, ready to append to a dynamic SQL `IN` clause. Returns the sentinel `('C7082BA7C83D38CAE98421BE494753931F8B52A8')` when `aTarget` is [`NIL`](../literals/nil.md) or empty.

## Best practices

!!! success "Do"
    - Use `BuildStringForIn` only when you intentionally need a literal SQL `IN` list.
    - Expect apostrophes inside values to be doubled in the output.
    - Check for the sentinel result when empty input should follow a different code path.
    - Prefer parameter arrays with `?` placeholders for functions such as [`RunSQL`](RunSQL.md), [`LSearch`](LSearch.md), and [`LSelect1`](LSelect1.md) when you do not need literal SQL text.

!!! failure "Don't"
    - Add another pair of parentheses around the returned value. The function already returns them.
    - Treat this as a general-purpose SQL safety layer for arbitrary query building.
    - Use it as a substitute for positional parameter arrays in database functions that support `?` placeholders.
    - Assume an empty array returns an empty string. It returns the sentinel list instead.

## Caveats

- Each value is converted to text before quoting, and surrounding spaces are trimmed.
- [`NIL`](../literals/nil.md) array elements become the literal text [`NIL`](../literals/nil.md) before quoting, so they appear as `'NIL'` in the result.
- The function always quotes every item as text.
- Empty input returns the sentinel list, not `()` and not an empty string.

## Examples

### Build a literal `IN` list from selected IDs

Converts a small array of sample IDs into one quoted list ready to append to a SQL `IN` clause.

```ssl
:PROCEDURE ShowSampleFilter;
	:DECLARE aSampleIDs, sInClause;

	aSampleIDs := {"SAM-2024-001", "SAM-2024-002", "SAM-2024-003"};
	sInClause := BuildStringForIn(aSampleIDs);

	UsrMes(sInClause);

	:RETURN sInClause;
:ENDPROC;

/* Usage;
DoProc("ShowSampleFilter");
```

[`UsrMes`](UsrMes.md) displays:

```
('SAM-2024-001','SAM-2024-002','SAM-2024-003')
```

### Filter a query on names that contain apostrophes

Passes names that include apostrophes to `BuildStringForIn` and embeds the result directly in a SQL `WHERE` clause. The apostrophe in `"Bob O'Brien"` is doubled automatically.

```ssl
:PROCEDURE FetchSamplesBySampler;
	:DECLARE aSamplerNames, sSQL, aResults;

	aSamplerNames := {"Alice Johnson", "Bob O'Brien", "Carol White"};

	sSQL := "
	    SELECT sampleid, samplename, sampler
	    FROM sample
	    WHERE sampler IN
	" + BuildStringForIn(aSamplerNames);

	aResults := LSelect1(sSQL);

	:RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("FetchSamplesBySampler");
```

## Related

- [`AddNameDelimiters`](AddNameDelimiters.md)
- [`BuildArray`](BuildArray.md)
- [`BuildString`](BuildString.md)
- [`BuildString2`](BuildString2.md)
- [`PrepareArrayForIn`](PrepareArrayForIn.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
