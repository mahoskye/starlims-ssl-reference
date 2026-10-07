---
title: "PrmCount"
summary: "Returns how many arguments the caller passed to the current server script; only valid in script-level code."
id: ssl.function.prmcount
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# PrmCount

Returns how many arguments the caller passed to the current server script; only valid in script-level code.

`PrmCount()` reports how many arguments the caller supplied to the running server script, for example with [`ExecFunction`](ExecFunction.md)`("Category.Script", aArgs)`. Use it in a script whose [`:PARAMETERS`](../keywords/PARAMETERS.md) has optional trailing parameters, to tell an omitted argument from one that was passed.

`PrmCount()` works only in the script's top-level code. Inside a [`:PROCEDURE`](../keywords/PROCEDURE.md), including one reached with [`DoProc`](DoProc.md), and in code run with [`ExecUdf`](ExecUdf.md), it raises `Function PrmCount() is not available in procedures.`

## When to use

- When a server script accepts optional trailing arguments and needs to know how many the caller actually supplied.
- When a script called with [`ExecFunction`](ExecFunction.md) should reject calls that leave out a required argument.

## Syntax

```ssl
PrmCount()
```

## Parameters

This function takes no parameters.

## Returns

**[number](../types/number.md)** — The number of arguments the caller passed to the current server script.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| Called inside a `:PROCEDURE`, or in code run with `ExecUdf`. | `Function PrmCount() is not available in procedures.` |

## Best practices

!!! success "Do"
    - Call `PrmCount()` in a server script's top-level code, after its `:PARAMETERS` line.
    - Check the count before using parameters a caller may have left out.

!!! failure "Don't"
    - Call `PrmCount()` inside a `:PROCEDURE`. It raises an error there. Inside a procedure, test a parameter with [`Empty`](Empty.md) or [`LimsTypeEx`](LimsTypeEx.md) instead, or give it a default with [`:DEFAULT`](../keywords/DEFAULT.md).
    - Use `PrmCount()` in code run with `ExecUdf`, which raises the same error.

## Caveats

- The count is the number of arguments the caller passed, not the number of parameters the script declares: a script with two parameters called with one argument gets `1`.

## Examples

### Reject calls that omit a required argument

A server script `Orders.ShowOrderStatus` checks that its caller passed an order number before using it.

```ssl
:PARAMETERS sOrderNo;

:IF PrmCount() < 1;
	UsrMes("Order number is required");
	:RETURN .F.;
:ENDIF;

UsrMes("Looking up order " + sOrderNo);

:RETURN .T.;
```

Calling it from another script, first without and then with the argument:

```ssl
ExecFunction("Orders.ShowOrderStatus");
ExecFunction("Orders.ShowOrderStatus", {"ORD-1001"});
```

`UsrMes` logs, in order:

```text
Order number is required
Looking up order ORD-1001
```

### Apply defaults only to omitted trailing arguments

A server script `Labels.BuildLabel` counts the arguments it received and fills in only the optional values the caller left out.

```ssl
:PARAMETERS sText, sPrefix, sSuffix;
:DECLARE nArgs, sResult;

nArgs := PrmCount();

:IF nArgs < 1;
	sText := "Untitled";
:ENDIF;

:IF nArgs < 2;
	sPrefix := "[";
:ENDIF;

:IF nArgs < 3;
	sSuffix := "]";
:ENDIF;

sResult := sPrefix + sText + sSuffix;
UsrMes(sResult);

:RETURN sResult;
```

Calling it with one, two and three arguments:

```ssl
ExecFunction("Labels.BuildLabel", {"Report"});
ExecFunction("Labels.BuildLabel", {"Report", "("});
ExecFunction("Labels.BuildLabel", {"Report", "(", ")"});
```

`UsrMes` logs, in order:

```text
[Report]
(Report]
(Report)
```

## Related

- [`DoProc`](DoProc.md)
- [`ExecFunction`](ExecFunction.md)
- [`number`](../types/number.md)
