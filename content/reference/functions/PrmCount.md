---
title: "PrmCount"
summary: "Returns how many arguments were passed to the currently executing procedure."
id: ssl.function.prmcount
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# PrmCount

Returns how many arguments were passed to the currently executing procedure.

`PrmCount()` reports the number of arguments supplied to the current procedure call. Use it inside a procedure when behavior depends on whether the caller passed zero, one, or more arguments. The function returns the count for the immediate current call only.

## When to use

- When a procedure supports optional trailing arguments and needs to detect how many were actually supplied.
- When a utility procedure changes behavior based on a flexible argument count.
- When you want to validate that a caller supplied the minimum number of arguments before using them.

## Syntax

```ssl
PrmCount()
```

## Parameters

This function takes no parameters.

## Returns

**[number](../types/number.md)** — The number of arguments passed to the current procedure call.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| Called outside a procedure context. | `Function PrmCount() is not available in procedures.` |

## Best practices

!!! success "Do"
    - Call `PrmCount()` inside a procedure body when the procedure accepts optional or flexible arguments.
    - Check the result before using arguments that may have been omitted by the caller.
    - Keep the count check close to the logic that depends on it so the procedure stays easy to follow.

!!! failure "Don't"
    - Call `PrmCount()` from top-level script code or any non-procedure context.
    - Assume every declared parameter was supplied by the caller; check `PrmCount()` first when omitted arguments matter.
    - Use `PrmCount()` as a substitute for clear procedure design when a fixed signature is enough.

## Examples

### Reject calls that omit a required argument

Use `PrmCount()` at the start of a procedure to verify that the caller supplied the minimum input you need.

```ssl
:PROCEDURE ShowOrderStatus;
	:PARAMETERS sOrderNo;

	:DECLARE nArgs;

	nArgs := PrmCount();

	:IF nArgs < 1;
		UsrMes("Order number is required");
		:RETURN .F.;
	:ENDIF;

	UsrMes("Looking up order " + sOrderNo);

	:RETURN .T.;
:ENDPROC;

DoProc("ShowOrderStatus");
DoProc("ShowOrderStatus", {"ORD-1001"});
```

`UsrMes` displays, in order:

```text
Order number is required
Looking up order ORD-1001
```

### Apply defaults only to omitted trailing arguments

Count the supplied arguments first, then fill in optional values only when the caller left them out.

```ssl
:PROCEDURE BuildLabel;
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
:ENDPROC;

DoProc("BuildLabel", {"Report"});
DoProc("BuildLabel", {"Report", "("});
DoProc("BuildLabel", {"Report", "(", ")"});
```

`UsrMes` displays, in order:

```text
[Report]
(Report]
(Report)
```

## Related

- [`DoProc`](DoProc.md)
- [`ExecFunction`](ExecFunction.md)
- [`number`](../types/number.md)
