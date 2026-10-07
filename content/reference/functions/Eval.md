---
title: "Eval"
summary: "Invokes a code block with the supplied arguments and returns the block's result."
id: ssl.function.eval
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# Eval

Invokes a code block with the supplied arguments and returns the block's result.

Eval is SSL's direct call form for code block values. It does one thing: it takes a code block value, runs the block's stored expression with the supplied arguments, and returns whatever that expression evaluates to.

Eval does not parse or compile SSL source text. If you have SSL source in a string, use a dynamic-code mechanism such as [`ExecUdf`](ExecUdf.md); Eval is only for code block values such as `{|nValue| nValue * 2}` or code blocks returned from other routines. Because Eval simply forwards the arguments to the block, the result can be any SSL value, including another code block.

## When to use

- When a routine receives a code block (a callback, predicate, or strategy) and needs to call it.
- When choosing one of several code blocks at runtime, for example from a dispatch table.
- When you want to pass arguments to a code block value and use its result.
- To run SSL source text stored in a string, use [`ExecUdf`](ExecUdf.md) instead.

## Syntax

```ssl
Eval(fnCode, [vArg1], [vArg2], ...)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `fnCode` | [codeblock](../types/codeblock.md) | yes | — | Code block to invoke. |
| `vArg1` | any | no | [`NIL`](../literals/nil.md) | Optional value passed to the code block. Additional arguments are allowed after `vArg1`. |

## Returns

**any** — Returns whatever value the code block produces.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `fnCode` is not a code block. | `Run-time error: the operator/method: eval is not implemented on type: <type>. Operand: <operand>` |

## Best practices

!!! success "Do"
    - Pass a code block value (from a `{|params| expr}` literal or a function that returns one) as the first argument.
    - Reserve use of Eval for calling code block values that are chosen or passed in at runtime.
    - Handle errors that may arise from evaluated code blocks.

!!! failure "Don't"
    - Pass an SSL source string to Eval. Strings are not code blocks, so the runtime rejects them when `eval` is invoked on that value type. Use [`ExecUdf`](ExecUdf.md) when you need to execute source text.
    - Use Eval in place of ordinary static routines or built-in functions. Standard routines are more performant and easier to debug.
    - Assume all evaluated code will succeed without handling errors. Error handling prevents runtime failures and unexpected halts.

## Caveats

- Errors raised inside the invoked block propagate to the Eval call site; wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the block may fail.
- Eval passes the supplied arguments to the code block in order; it does not compile source text, rename parameters, or add its own defaults.

## Examples

### Invoke a code block literal with arguments

Call a simple arithmetic code block defined with `{|n1, n2| n1 + n2}` and get the result.

```ssl
:PROCEDURE EvalCodeBlock;
	:DECLARE fnAdd, nValue1, nValue2, nResult;

	nValue1 := 25;
	nValue2 := 17;

	fnAdd := {|nLeft, nRight| nLeft + nRight};

	nResult := Eval(fnAdd, nValue1, nValue2);

	UsrMes(
		"Adding " + LimsString(nValue1)
		+ " + " + LimsString(nValue2)
		+ " = " + LimsString(nResult)
	);

	:RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("EvalCodeBlock");
```

[`UsrMes`](UsrMes.md) logs:

```text
Adding 25 + 17 = 42
```

### Strategy pattern — apply a tier's chain of pricing rules

Choose a list of pricing rule code blocks based on a customer tier and apply them in order to a running total. The VIP tier applies the VIP discount and then the clearance rule.

```ssl
:PROCEDURE ApplyDiscountRules;
	:DECLARE fnStandardDiscount, fnVipDiscount, fnClearance;
	:DECLARE aRuleBlocks, fnRule, nIndex, nCount;
	:DECLARE nUnitPrice, nQty, nFinalPrice, sCustomerTier;

	nUnitPrice := 100;
	nQty := 5;
	sCustomerTier := "VIP";

	fnStandardDiscount := {|nPrice, nUnits| nPrice * nUnits * 0.95};
	fnVipDiscount := {|nPrice, nUnits| nPrice * nUnits * 0.85};
	fnClearance := {|nPrice, nUnits| nPrice * nUnits * 0.50};

	:IF sCustomerTier == "VIP";
		aRuleBlocks := {fnVipDiscount, fnClearance};
	:ELSE;
		aRuleBlocks := {fnStandardDiscount};
	:ENDIF;

	nCount := ALen(aRuleBlocks);
	nFinalPrice := nUnitPrice * nQty;

	:FOR nIndex := 1 :TO nCount;
		fnRule := aRuleBlocks[nIndex];
		nFinalPrice := Eval(fnRule, nFinalPrice / nQty, nQty);
	:NEXT;

	UsrMes("Final price for " + sCustomerTier + ": " + LimsString(nFinalPrice));

	:RETURN nFinalPrice;
:ENDPROC;

/* Usage;
DoProc("ApplyDiscountRules");
```

[`UsrMes`](UsrMes.md) logs:

```text
Final price for VIP: 212.5
```

### Dispatch-table validation per sample type

Register one validator code block per sample type in an object and invoke the right validator based on the sample being processed.

```ssl
:PROCEDURE RunSampleValidation;
	:DECLARE oValidators, fnValidator;
	:DECLARE sSampleType, nResult, dDueDate, dToday;
	:DECLARE bValid;

	dToday := Today();

	sSampleType := "BLOOD";
	nResult := 245;
	dDueDate := dToday + 2;

	oValidators := CreateUdObject();
	SetInternal(
		oValidators,
		"BLOOD",
		{|nValue, dCheckDate| nValue > 0 .AND. nValue < 500 .AND. dCheckDate >= dToday}
	);
	SetInternal(
		oValidators,
		"URINE",
		{|nValue, dCheckDate| nValue >= 0 .AND. nValue < 1000 .AND. dCheckDate >= dToday}
	);
	SetInternal(oValidators, "CLEARANCE", {|nValue, dCheckDate| nValue > 0});

	:IF !HasProperty(oValidators, sSampleType);
		ErrorMes("No validator registered for sample type " + sSampleType);
		:RETURN .F.;
	:ENDIF;

	fnValidator := GetInternal(oValidators, sSampleType);

	bValid := Eval(fnValidator, nResult, dDueDate);

	:IF bValid;
		UsrMes("Sample passed " + sSampleType + " validation");
	:ELSE;
		ErrorMes("Sample failed " + sSampleType + " validation");
	:ENDIF;

	:RETURN bValid;
:ENDPROC;

/* Usage;
DoProc("RunSampleValidation");
```

## Related

- [`ExecFunction`](ExecFunction.md)
- [`ExecUdf`](ExecUdf.md)
- [`codeblock`](../types/codeblock.md)
