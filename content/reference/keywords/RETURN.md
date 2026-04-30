---
title: "RETURN"
summary: "Ends the current script, procedure, or method immediately and can optionally return a value."
id: ssl.keyword.return
element_type: keyword
category: control-flow
tags:
  - procedure
  - script
  - method
  - control-flow
  - return-value
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RETURN

Ends the current script, procedure, or method immediately and can optionally return a value.

`:RETURN` stops execution of the current executable body and skips every later statement in that body. When you include an expression, its value becomes the result returned to the caller. When you omit the expression in a normal script, procedure, or method, SSL returns an empty string.

Two important placement rules also apply. `:RETURN` cannot appear inside [`:FINALLY`](FINALLY.md), and constructors may only use the bare form `:RETURN;` to exit early.

## Behavior

Use `:RETURN` anywhere you need an immediate exit from the current executable body. That includes top-level script code, ordinary procedures, and class methods.

When `:RETURN` runs inside [`:TRY`](TRY.md) or [`:CATCH`](CATCH.md), the enclosing [`:FINALLY`](FINALLY.md) cleanup still runs before execution leaves the block. `:RETURN` itself must stay outside the [`:FINALLY`](FINALLY.md) section.

In constructors, `:RETURN;` is valid as an early exit, but `:RETURN value;` is not.

## When to use

- When you need to leave a script, procedure, or method as soon as a result is ready.
- When guard checks should stop execution early on missing or invalid input.
- When different success and failure paths should return different results.

## Syntax

```ssl
:RETURN;
:RETURN expression;
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `expression` | Any | no | omitted | Value returned to the caller. In ordinary scripts, procedures, and methods, omitting it returns an empty string. In constructors, an expression is not allowed. |

## Keyword group

**Group:** Procedures & Classes
**Role:** statement

## Best practices

!!! success "Do"
    - Use `:RETURN` for clear guard clauses when validation fails early.
    - Return explicit values when callers depend on a result.
    - Keep cleanup in [`:FINALLY`](FINALLY.md) and place `:RETURN` in the [`:TRY`](TRY.md) or [`:CATCH`](CATCH.md) body instead.

!!! failure "Don't"
    - Put `:RETURN` inside [`:FINALLY`](FINALLY.md). It is invalid there.
    - Use `:RETURN value;` inside a constructor. Constructors may only use the bare form.
    - Leave dead statements after a `:RETURN` and expect them to run.

## Caveats

- Keywords are case-sensitive and must be written in uppercase.
- Placing `:RETURN` inside [`:FINALLY`](FINALLY.md) is a compile error: `Cannot have :RETURN inside :FINALLY.`
- Using `:RETURN value;` in a constructor is a compile error: `Cannot return values from a constructor.`

## Examples

### Return a calculated value from a procedure

Uses `:RETURN` to send a computed result back to the caller. With `nUnitPrice` set to `25` and `nQuantity` set to `4`, the subtotal is `100` and the total with 8% tax is `108`.

```ssl
:PROCEDURE CalculateTotalWithTax;
	:PARAMETERS nUnitPrice, nQuantity;
	:DECLARE nSubtotal, nTaxRate, nTotal;

	nSubtotal := nUnitPrice * nQuantity;
	nTaxRate := 0.08;
	nTotal := nSubtotal + (nSubtotal * nTaxRate);

	:RETURN nTotal;
:ENDPROC;

/* Usage;
:DECLARE nResult;
nResult := DoProc("CalculateTotalWithTax", {25, 4});
UsrMes(LimsString(nResult));
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
108
```

### Return early from top-level script code

Uses guard clauses in script entry-point code to stop processing once a failure is detected. With `sBatchID` set to `"B-1001"` and matching samples found, the script reaches the final `:RETURN` with a loaded-count message.

```ssl
:DECLARE sBatchID, aSamples;

sBatchID := "B-1001";

:IF Empty(sBatchID);
	:RETURN "Batch ID is required";
:ENDIF;

aSamples := SQLExecute("
    SELECT sample_id
    FROM sample
    WHERE batch_id = ?sBatchID?
");

:IF ALen(aSamples) == 0;
	:RETURN "No samples found for batch " + sBatchID;
:ENDIF;

:RETURN "Loaded " + LimsString(ALen(aSamples)) + " sample(s)";
```

### Return from TRY or CATCH while FINALLY still cleans up

Demonstrates that [`:FINALLY`](FINALLY.md) always runs even when `:RETURN` exits from [`:TRY`](TRY.md) or [`:CATCH`](CATCH.md). Regardless of which branch returns, the cleanup message displays.

```ssl
:PROCEDURE LoadBatchStatus;
	:PARAMETERS sBatchID;
	:DECLARE bCleanupNeeded, oErr, sStatus;

	bCleanupNeeded := .F.;
	sStatus := "";

	:TRY;
		bCleanupNeeded := .T.;
		sStatus := LSearch("
		    SELECT status
		    FROM batch
		    WHERE batch_id = ?
		", "",, {sBatchID});

		:IF Empty(sStatus);
			:RETURN "Batch was not found";
		:ENDIF;

		:RETURN sStatus;

	:CATCH;
		oErr := GetLastSSLError();
		:RETURN "Status lookup failed: " + oErr:Description;

	:FINALLY;
		:IF bCleanupNeeded;
			bCleanupNeeded := .F.;
			UsrMes("Batch status lookup finished");
		:ENDIF;

	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("LoadBatchStatus", {"B-1001"});
```

[`UsrMes`](../functions/UsrMes.md) displays before the procedure returns:

```text
Batch status lookup finished
```

## Related

- [`PROCEDURE`](PROCEDURE.md)
- [`ENDPROC`](ENDPROC.md)
- [`FINALLY`](FINALLY.md)
