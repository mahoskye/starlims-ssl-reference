---
title: "codeblock"
summary: "Represents a callable expression value that you can store, pass, and evaluate."
id: ssl.type.codeblock
element_type: type
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# codeblock

## What it is

Represents a callable expression value that you can store, pass, and evaluate.

A code block is a first-class callable value written with SSL's code-block literal syntax, such as `{|nValue| nValue * 2}`. The literal requires at least one parameter, and its body is a single expression. Use code blocks when you need inline logic that can be passed to functions such as [`Eval`](../functions/Eval.md) or higher-order array helpers.
[`LimsTypeEx`](../functions/LimsTypeEx.md) reports this type as `CODEBLOCK`.

## Creating values

Code block values use inline literal syntax with pipe-delimited parameters and a single expression body.

```ssl
fnDouble := {|nValue| nValue * 2};
fnAdd := {|nA, nB| nA + nB};
```

- **Runtime type:** `CODEBLOCK`
- **Literal syntax:** `{|param| expression}`, `{|param1, param2| expression}`

## Operators

Equality is not supported for code blocks. Comparing them raises a runtime error instead of returning a value.

| Operator | Symbol | Returns | Behavior |
|----------|--------|---------|----------|
| [`equals`](../operators/equals.md) | [`=`](../operators/equals.md) | error | Raises a runtime error. |
| [`strict-equals`](../operators/strict-equals.md) | [`==`](../operators/strict-equals.md) | error | Raises a runtime error. |
| [`not-equals`](../operators/not-equals.md) | [`!=`](../operators/not-equals.md) | error | Raises a runtime error. |

## Members

| Member | Kind | Returns | Description |
|--------|------|---------|-------------|
| `eval` | Method | `any` | Evaluates the code block with the arguments you provide. |
| `IsEmpty()` | Method | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the code block is uninitialized, otherwise [`.F.`](../literals/false.md). |
| `ToString()` | Method | [`string`](string.md) | Always returns the fixed text `Code block`. Does not expose the parameter list or expression body. |
| `clone()` | Method | `code block` | Creates another code block value that reuses the same callable logic. |

## Indexing

- **Supported:** false
- **Behavior:** `[]` indexing and indexed assignment are not supported for code blocks and raise a runtime error.

## Notes for daily SSL work

!!! success "Do"
    - Use a code block when you need a small reusable expression that fits naturally inline.
    - Keep code blocks expression-based and move multi-step logic into a procedure.
    - Check `IsEmpty()` before evaluation when a code block may not have been initialized.

!!! failure "Don't"
    - Compare code blocks with [`=`](../operators/equals.md), [`==`](../operators/strict-equals.md), or [`!=`](../operators/not-equals.md). Code blocks do not support equality checks and the comparison raises a runtime error.
    - Use code blocks for multi-statement workflows. SSL code blocks are single-expression values, not miniature procedures.
    - Treat a code block like an array or string. `[]` access and indexed assignment are not supported.

## Errors and edge cases

- `clone()` copies the code block value, but it does not create a separate procedure.

## Examples

### Evaluating a simple code block

Defines a multiplication code block and runs it with [`Eval`](../functions/Eval.md) for the values 3 and 7.

```ssl
:PROCEDURE DemoCodeBlock;
	:DECLARE fnMultiply, nResult, sMessage;

	fnMultiply := {|nLeft, nRight| nLeft * nRight};
	nResult := Eval(fnMultiply, 3, 7);
	sMessage := "3 x 7 = " + LimsString(nResult);
	UsrMes(sMessage);

	:RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("DemoCodeBlock");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
3 x 7 = 21
```

### Reusing a predicate code block in a loop

Defines a threshold predicate once and reuses it to filter values from an array. Values above 100 are collected into `aMatches`.

```ssl
:PROCEDURE FilterHighValues;
	:DECLARE aValues, aMatches, fnAboveLimit, nIndex, nLimit, nValue;

	aValues := {50, 120, 75, 200, 150};
	aMatches := {};
	nLimit := 100;
	fnAboveLimit := {|nItem| nItem > nLimit};

	:FOR nIndex := 1 :TO ALen(aValues);
		nValue := aValues[nIndex];

		:IF Eval(fnAboveLimit, nValue);
			AAdd(aMatches, nValue);
		:ENDIF;
	:NEXT;

	:RETURN aMatches;
:ENDPROC;

/* Usage;
DoProc("FilterHighValues");
```

### Passing a code block to an array helper

Passes a predicate code block to [`AScan`](../functions/AScan.md) to find the first row where pH exceeds 8.0. The array has S2 at index 2 with pH 8.6, so [`AScan`](../functions/AScan.md) returns `2`.

```ssl
:PROCEDURE FindFirstOutOfSpec;
	:DECLARE aResults, fnIsOutOfSpec, nIndex;

	aResults := {
		{"S1", "pH", 7.1},
		{"S2", "pH", 8.6},
		{"S3", "pH", 7.4}
	};

	fnIsOutOfSpec := {|aRow| aRow[3] > 8.0};
	nIndex := AScan(aResults, fnIsOutOfSpec);

	:RETURN nIndex;
:ENDPROC;

/* Usage;
DoProc("FindFirstOutOfSpec");
```

## Related elements

- [`Eval`](../functions/Eval.md)
- [`code-block`](../special-forms/code-block.md)
- [`LimsTypeEx`](../functions/LimsTypeEx.md)
- [`object`](object.md)
