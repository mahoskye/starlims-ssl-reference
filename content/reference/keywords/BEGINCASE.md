---
title: "BEGINCASE"
summary: "Starts a :BEGINCASE block for evaluating one or more boolean :CASE conditions, with an optional :OTHERWISE branch and a required :ENDCASE."
id: ssl.keyword.begincase
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# BEGINCASE

Starts a `:BEGINCASE` block for evaluating one or more boolean [`:CASE`](CASE.md) conditions, with an optional [`:OTHERWISE`](OTHERWISE.md) branch and a required [`:ENDCASE`](ENDCASE.md).

`BEGINCASE` opens SSL's case-block form. Each [`:CASE`](CASE.md) contains a full boolean expression, not a simple value label. The runtime evaluates the [`:CASE`](CASE.md) expressions in order. When a [`:CASE`](CASE.md) expression is true, that case body runs. If the body does not end with [`:EXITCASE;`](EXITCASE.md), execution continues and later [`:CASE`](CASE.md) expressions are still evaluated. An [`:OTHERWISE`](OTHERWISE.md) block runs only when no earlier [`:CASE`](CASE.md) body has executed.

## Behavior

`BEGINCASE` must be followed by at least one [`:CASE`](CASE.md) block and closed with [`:ENDCASE;`](ENDCASE.md). Each [`:CASE`](CASE.md) expression is evaluated as a boolean condition.

Without [`:EXITCASE;`](EXITCASE.md), a matched branch does not automatically stop the block. Later [`:CASE`](CASE.md) expressions are still checked, and additional matching case bodies may run. This is why [`:EXITCASE;`](EXITCASE.md) is the normal pattern when you want the block to behave like an either-or decision structure.

[`:OTHERWISE;`](OTHERWISE.md) is optional but recommended. It runs only if no earlier [`:CASE`](CASE.md) body executed. Once any [`:CASE`](CASE.md) body has run, [`:OTHERWISE;`](OTHERWISE.md) is skipped.

## When to use

- When you need to evaluate several boolean conditions in a clearer structure than a long [`:IF`](IF.md) chain.
- When the logic benefits from named branches and an explicit default path.
- When you intentionally want either single-branch behavior with [`:EXITCASE;`](EXITCASE.md) or controlled multi-match behavior by omitting it.

## Syntax

```ssl
:BEGINCASE;
:CASE <condition>;
    /* statements;
    :EXITCASE;
:CASE <condition>;
    /* statements;
    :EXITCASE;
:OTHERWISE;
    /* statements;
    :EXITCASE;
:ENDCASE;
```

`BEGINCASE` itself does not take parameters.

## Keyword group

**Group:** Control Flow
**Role:** opener

## Best practices

!!! success "Do"
    - End each [`:CASE`](CASE.md) and [`:OTHERWISE`](OTHERWISE.md) branch with [`:EXITCASE;`](EXITCASE.md) unless you intentionally want multi-match behavior.
    - Add an [`:OTHERWISE;`](OTHERWISE.md) branch when the logic needs a clear default path.
    - Use `:BEGINCASE;` when several boolean conditions are easier to read as branches than as a long [`:IF`](IF.md) chain.

!!! failure "Don't"
    - Assume `:BEGINCASE;` stops after the first true branch. Without [`:EXITCASE;`](EXITCASE.md), later [`:CASE`](CASE.md) expressions are still evaluated and more than one body can run.
    - Omit [`:OTHERWISE;`](OTHERWISE.md) when the block needs explicit default handling.
    - Use `:BEGINCASE;` for trivial two-way branching where [`:IF`](IF.md) and [`:ELSE`](ELSE.md) would be clearer.

## Caveats

- SSL keywords are case-sensitive. Write `:BEGINCASE`, [`:CASE`](CASE.md), [`:OTHERWISE`](OTHERWISE.md), [`:EXITCASE`](EXITCASE.md), and [`:ENDCASE`](ENDCASE.md) in uppercase.

## Examples

### Condition-based notification

Choose one notification path by ending each branch with [`:EXITCASE;`](EXITCASE.md). With `nResultValue` set to `85`, the warning branch matches and the notification message is displayed.

```ssl
:PROCEDURE NotifyAnalysisStatus;
	:DECLARE sSampleID, sNotifyMessage, oEmail, nResultValue;

	sSampleID := "LAB-2024-0042";
	nResultValue := 85;
	oEmail := Email{};

	:BEGINCASE;
	:CASE nResultValue >= 100;
		sNotifyMessage := "CRITICAL: " + sSampleID
			+ " exceeded the safe threshold";
		oEmail:Subject := "Critical Alert - Sample " + sSampleID;
		:EXITCASE;
	:CASE nResultValue >= 75;
		sNotifyMessage := "WARNING: " + sSampleID
			+ " is approaching the threshold limit";
		oEmail:Subject := "Warning Alert - Sample " + sSampleID;
		:EXITCASE;
	:CASE nResultValue >= 50;
		sNotifyMessage := "NOTICE: " + sSampleID
			+ " is within the acceptable range";
		oEmail:Subject := "Normal Status - Sample " + sSampleID;
		:EXITCASE;
	:OTHERWISE;
		sNotifyMessage := "INFO: " + sSampleID
			+ " is below the typical range";
		oEmail:Subject := "Information - Sample " + sSampleID;
		:EXITCASE;
	:ENDCASE;

	oEmail:Body := sNotifyMessage;
	oEmail:To := {"labmanager@example.com"};

	InfoMes(sNotifyMessage);

	:RETURN sNotifyMessage;
:ENDPROC;

/* Usage;
DoProc("NotifyAnalysisStatus");
```

[`InfoMes`](../functions/InfoMes.md) displays:

```text
WARNING: LAB-2024-0042 is approaching the threshold limit
```

### Dynamic pricing configuration

Ordered conditions ensure the first matching business rule wins. With `nBasePrice` of `100`, a contract order of `1500` units triggers the contract volume discount.

```ssl
:PROCEDURE CalculateDynamicPrice;
	:PARAMETERS nBasePrice, sCustomerType, nOrderVolume, bHasContract;
	:DEFAULT sCustomerType, "RETAIL";
	:DEFAULT nOrderVolume, 0;
	:DEFAULT bHasContract, .F.;
	:DECLARE nFinalPrice, sFormulaUsed, sMessage;

	nFinalPrice := nBasePrice;
	sFormulaUsed := "Base Price";

	:BEGINCASE;
	:CASE bHasContract .AND. nOrderVolume > 1000;
		nFinalPrice := nBasePrice * 0.70;
		sFormulaUsed := "Contract Volume Discount";
		:EXITCASE;
	:CASE sCustomerType == "WHOLESALE";
		nFinalPrice := nBasePrice * 0.80;
		sFormulaUsed := "Wholesale Rate";
		:EXITCASE;
	:CASE sCustomerType == "DISTRIBUTOR" .AND. nOrderVolume > 500;
		nFinalPrice := nBasePrice * 0.85;
		sFormulaUsed := "Distributor Volume Rate";
		:EXITCASE;
	:CASE nOrderVolume > 2000;
		nFinalPrice := nBasePrice * 0.90;
		sFormulaUsed := "High Volume Discount";
		:EXITCASE;
	:OTHERWISE;
		sFormulaUsed := "Standard Pricing";
		:EXITCASE;
	:ENDCASE;

	sMessage := "Price: " + LimsString(nBasePrice)
				+ " -> " + LimsString(nFinalPrice);
	sMessage += " via " + sFormulaUsed;

	UsrMes(sMessage);

	:RETURN nFinalPrice;
:ENDPROC;

/* Usage;
DoProc("CalculateDynamicPrice", {100, "RETAIL", 1500, .T.});
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Price: 100 -> 70 via Contract Volume Discount
```

### Single-branch shipment processing

Show the normal single-branch behavior by ending each branch with [`:EXITCASE;`](EXITCASE.md). Passing `bRushOrder` and `bColdChain` as [`.T.`](../literals/true.md) causes the first matching case body to execute.

```ssl
:PROCEDURE BuildShipmentActions;
	:PARAMETERS bRushOrder, bColdChain, bInternational;
	:DEFAULT bRushOrder, .F.;
	:DEFAULT bColdChain, .F.;
	:DEFAULT bInternational, .F.;
	:DECLARE aActions;

	aActions := {};

	:BEGINCASE;
	:CASE bRushOrder;
		AAdd(aActions, "Print priority label");
		:EXITCASE;
	:CASE bColdChain;
		AAdd(aActions, "Pack with temperature control");
		:EXITCASE;
	:CASE bInternational;
		AAdd(aActions, "Attach customs paperwork");
		:EXITCASE;
	:OTHERWISE;
		AAdd(aActions, "Standard packaging only");
		:EXITCASE;
	:ENDCASE;

	:RETURN aActions;
:ENDPROC;

/* Usage;
DoProc("BuildShipmentActions", {.T., .T., .F.});
```

In this example, a shipment that is both rush and cold-chain adds only the priority-label action because the first matching branch exits the block. If any [`:CASE`](CASE.md) body runs, [`:OTHERWISE;`](OTHERWISE.md) is skipped.

## Related

- [`CASE`](CASE.md)
- [`OTHERWISE`](OTHERWISE.md)
- [`ENDCASE`](ENDCASE.md)
- [`EXITCASE`](EXITCASE.md)
- [`IIf`](../functions/IIf.md)
