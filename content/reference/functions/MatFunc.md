---
title: "MatFunc"
summary: "Calculates a mathematical operation on a given number based on the specified function name."
id: ssl.function.matfunc
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# MatFunc

Calculates a mathematical operation on a given number based on the specified function name.

Use `MatFunc` when the mathematical operation is chosen at runtime instead of being hardcoded in the script. The function accepts one supported operation name and one numeric argument, then returns the computed numeric result.

Supported operation names are `ABS`, `ACOT`, `ATAN`, `COS`, `COT`, `EXP`, `FACT`, `FRAC`, `LOG`, `LOG10`, `PI`, `RAND`, `SIN`, `SQRT`, and `TAN`. The name must match one of these values exactly.

## When to use

- When you need to choose the math operation from configuration, user input, or other runtime state.
- When one workflow needs to support several math operations through the same call site.
- When you are mapping operation names such as `ABS`, `LOG`, or `SQRT` to executable behavior.

## Syntax

```ssl
MatFunc(sFunctionName, nNumber)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFunctionName` | [string](../types/string.md) | yes | — | Mathematical operation name. Supported values are `ABS`, `ACOT`, `ATAN`, `COS`, `COT`, `EXP`, `FACT`, `FRAC`, `LOG`, `LOG10`, `PI`, `RAND`, `SIN`, `SQRT`, and `TAN`. |
| `nNumber` | [number](../types/number.md) | yes | — | Numeric input value. `PI` and `RAND` still require this argument even though the underlying calculation does not use it. |

## Returns

**[number](../types/number.md)** — Result of the selected mathematical operation.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFunctionName` is [`NIL`](../literals/nil.md). | `sFunctionName cannot be null.` |
| `nNumber` is [`NIL`](../literals/nil.md). | `nNumber cannot be null.` |
| `sFunctionName` is not a supported operation name. | `Invalid Mathematical function call <sFunctionName>` |

## Best practices

!!! success "Do"
    - Use `MatFunc` when the operation name is chosen dynamically at runtime.
    - Validate or normalize operation names before calling so only supported values reach the function.
    - Prefer direct functions such as [`Abs`](Abs.md) or [`Sqrt`](Sqrt.md) when the operation is fixed in advance.

!!! failure "Don't"
    - Pass unchecked user or configuration input directly as `sFunctionName`.
    - Assume lowercase or mixed-case names are accepted.
    - Use `MatFunc` just to wrap one known operation throughout the script.

## Caveats

- `PI` and `RAND` still require the `nNumber` argument even though the calculation ignores it.
- Numeric domain validation is not performed. Operations such as `LOG`, `LOG10`, `SQRT`, and `COT` can return special numeric results such as `NaN` or infinity for some inputs.
- `FACT` does not validate its input. The factorial loop terminates when the value reaches `1`, so `0`, negative numbers, and non-integers are not safe inputs.

## Examples

### Select one operation by name

Use `MatFunc` when the operation name is already known in a variable.

```ssl
:PROCEDURE ShowAbsoluteValue;
    :DECLARE sFunctionName, nInputValue, nResult;

    sFunctionName := "ABS";
    nInputValue := -42;
    nResult := MatFunc(sFunctionName, nInputValue);

    UsrMes(
        "ABS(" + LimsString(nInputValue) + ") = " + LimsString(nResult)
    );
:ENDPROC;

/* Usage;
DoProc("ShowAbsoluteValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
ABS(-42) = 42
```

### Validate a configurable operation name

Check the requested name before calling `MatFunc` so unsupported values are rejected cleanly.

```ssl
:PROCEDURE EvaluateConfiguredMath;
    :PARAMETERS sRequestedFunc, nInputValue;
    :DECLARE aSupportedFuncs, nResult;

    aSupportedFuncs := {
        "ABS", "ACOT", "ATAN", "COS", "COT", "EXP", "FACT", "FRAC",
        "LOG", "LOG10", "PI", "RAND", "SIN", "SQRT", "TAN"
    };

    :IF AScan(aSupportedFuncs, sRequestedFunc) = 0;
        UsrMes("Unsupported operation: " + sRequestedFunc);
        /* Displays unsupported operation message;
        :RETURN;
    :ENDIF;

    nResult := MatFunc(sRequestedFunc, nInputValue);

    UsrMes(
        sRequestedFunc + "(" + LimsString(nInputValue) + ") = "
        + LimsString(nResult)
    );
    /* Displays selected operation result;
:ENDPROC;

/* Usage;
DoProc("EvaluateConfiguredMath", {"SIN", 0.0});
```

### Process a batch of math jobs safely

Handle multiple requested operations, keep successful results, and record failures without stopping the whole batch.

```ssl
:PROCEDURE ProcessMathJobs;
    :PARAMETERS aJobs;
    :DECLARE aResults, oJob, oResult, oErr, nIndex;
    :DECLARE sFunctionName, sSummary;
    :DECLARE nInputValue, nResultValue;

    aResults := {};

    :FOR nIndex := 1 :TO ALen(aJobs);
        oJob := aJobs[nIndex];
        sFunctionName := oJob:functionName;
        nInputValue := oJob:inputValue;

        :TRY;
            nResultValue := MatFunc(sFunctionName, nInputValue);

            oResult := CreateUdObject({
                {"functionName", sFunctionName},
                {"inputValue", nInputValue},
                {"success", .T.},
                {"resultValue", nResultValue},
                {"message", ""}
            });
        :CATCH;
            oErr := GetLastSSLError();

            oResult := CreateUdObject({
                {"functionName", sFunctionName},
                {"inputValue", nInputValue},
                {"success", .F.},
                {"resultValue", 0},
                {"message", oErr:Description}
            });
        :ENDTRY;

        AAdd(aResults, oResult);
    :NEXT;

    sSummary := "Processed " + LimsString(ALen(aResults)) + " math job(s)";
    UsrMes(sSummary);
    /* Displays batch summary;

    :RETURN aResults;
:ENDPROC;
```

Usage:

```ssl
:DECLARE aJobs, aResults;

aJobs := {
    CreateUdObject({{"functionName", "ABS"}, {"inputValue", (0 - 42.5)}}),
    CreateUdObject({{"functionName", "SIN"}, {"inputValue", 0.0}}),
    CreateUdObject({{"functionName", "BAD"}, {"inputValue", 5.0}})
};

aResults := DoProc("ProcessMathJobs", {aJobs});
```

## Related

- [`Abs`](Abs.md)
- [`Sqrt`](Sqrt.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
