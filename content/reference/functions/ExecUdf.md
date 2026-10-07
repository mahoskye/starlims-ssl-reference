---
title: "ExecUdf"
summary: "Executes SSL source supplied as a string and returns the result."
id: ssl.function.execudf
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# ExecUdf

Executes SSL source supplied as a string and returns the result.

`ExecUdf` runs SSL code built at runtime. If `sCode` is a single expression with no trailing semicolon, `ExecUdf` returns its value. If `sCode` is just the name of a local variable, `ExecUdf` returns that variable's current value. When supplied, `aArgs` must be an array, and `bCacheCode` enables reuse of compiled code for repeated execution of the same source text.

## When to use

- When you need to execute SSL source assembled at runtime.
- When a template or generated script must return a value.
- When the same dynamic code will be executed repeatedly and cached compilation is useful.
- When [`Eval`](Eval.md) is not appropriate because you have source text rather than a code block value.

## Syntax

```ssl
ExecUdf(sCode, [aArgs], [bCacheCode])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCode` | [string](../types/string.md) | yes | — | SSL source to execute. If it is [`NIL`](../literals/nil.md), it is treated as an empty string. |
| `aArgs` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Optional argument array for the dynamic call. When supplied, it must be an array. The dynamic code receives the elements, in order, through its own [`:PARAMETERS`](../keywords/PARAMETERS.md) statement: `ExecUdf(":PARAMETERS a, b; :RETURN a + b;", {2, 3})` returns `5`. |
| `bCacheCode` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Reuses compiled code for repeated execution of the same source text. |

## Returns

**any** — Returns whatever the dynamic code evaluates or returns.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aArgs` is provided but is not an array. | `Expected an array but actual type was: {type}` |
| `sCode` has a syntax error such as an unexpected token. Other compile failures raise the compiler's own message. | `unexpected token: ["{token}",<{tokenType}>,line={line},col={column}]` |

## Best practices

!!! success "Do"
    - Pass a complete expression or a complete SSL snippet with an explicit [`:RETURN`](../keywords/RETURN.md) when the result matters.
    - Skip `aArgs` with adjacent commas when you only want to set the cache flag, for example `ExecUdf(sCode,, .T.)`.
    - Use caching only for stable source text that will be executed repeatedly.
    - Wrap dynamic execution in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the source may fail to compile or run.

!!! failure "Don't"
    - Pass a string, number, or object as the second argument. `aArgs` must be an array when present.
    - Use `ExecUdf` when [`Eval`](Eval.md) or [`DoProc`](DoProc.md) already fits the job better. [`Eval`](Eval.md) is for code blocks, and [`DoProc`](DoProc.md) is for known procedures.
    - Assume generated code is safe just because it comes from your own script. Validate or constrain dynamic source before executing it.
    - Enable `bCacheCode` for one-off or constantly changing code strings where reuse provides no benefit.

## Caveats

- Omitting `aArgs` is valid. To set `bCacheCode` without arguments, skip the second parameter with adjacent commas: `ExecUdf(sCode,, .T.)`.

## Examples

### Evaluate a simple expression string

Passes an arithmetic expression as a string to `ExecUdf` and logs the numeric result. Because the string is a single expression with no trailing `;`, `ExecUdf` returns its value, `14`.

```ssl
:PROCEDURE RunDynamicExpression;
    :DECLARE sCode, nResult;

    sCode := "2 + 3 * 4";
    nResult := ExecUdf(sCode);

    UsrMes("Calculated value: " + LimsString(nResult));
    :RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("RunDynamicExpression");
```

[`UsrMes`](UsrMes.md) logs:

```text
Calculated value: 14
```

### Return a local variable by name

Passes a bare identifier string to `ExecUdf`. Because `"sStatus"` matches an existing local variable and does not end with `;`, `ExecUdf` returns that variable's current value.

```ssl
:PROCEDURE ReturnLocalValue;
    :DECLARE sCode, sStatus, sResult;

    sStatus := "Logged";
    sCode := "sStatus";

    sResult := ExecUdf(sCode);

    UsrMes("Returned value: " + sResult);
    :RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("ReturnLocalValue");
```

[`UsrMes`](UsrMes.md) logs:

```text
Returned value: Logged
```

### Reuse compiled dynamic code with caching

Runs the same dynamic code block five times without caching, then five times with caching. Both totals should be equal. The difference is that cached execution skips compilation on the second and later calls.

```ssl
:PROCEDURE CompareCachedExecution;
    :DECLARE sCode, nIterations, nIndex, nUncachedTotal, nCachedTotal;

    nIterations := 5;
    sCode := "
        :DECLARE nSum, nInner;
        nSum := 0;

        :FOR nInner := 1 :TO 100;
            nSum += nInner;
        :NEXT;

        :RETURN nSum;
    ";

    nUncachedTotal := 0;
    :FOR nIndex := 1 :TO nIterations;
        nUncachedTotal += ExecUdf(sCode,, .F.);
    :NEXT;

    nCachedTotal := 0;
    :FOR nIndex := 1 :TO nIterations;
        nCachedTotal += ExecUdf(sCode,, .T.);
    :NEXT;

    UsrMes(
        "Uncached total: " + LimsString(nUncachedTotal)
        + " | Cached total: " + LimsString(nCachedTotal)
    );

    :RETURN nCachedTotal;
:ENDPROC;

/* Usage;
DoProc("CompareCachedExecution");
```

[`UsrMes`](UsrMes.md) logs:

```text
Uncached total: 25250 | Cached total: 25250
```

## Related

- [`DoProc`](DoProc.md)
- [`Eval`](Eval.md)
- [`ExecFunction`](ExecFunction.md)
- [`ExecInternal`](ExecInternal.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
