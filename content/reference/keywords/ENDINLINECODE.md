---
title: "ENDINLINECODE"
summary: "Ends a named inline SSL code block opened by :BEGININLINECODE."
id: ssl.keyword.endinlinecode
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ENDINLINECODE

Ends a named inline SSL code block opened by [`:BEGININLINECODE`](BEGININLINECODE.md).

`:ENDINLINECODE;` closes the inline block started by [`:BEGININLINECODE`](BEGININLINECODE.md) `Name;` or `:BEGININLINECODE "Name";`. Everything between the opener and `:ENDINLINECODE;` is the inline block body. That body can later be retrieved with [`GetInlineCode`](../functions/GetInlineCode.md) `()`. After `:ENDINLINECODE;`, regular script statements continue normally. The keyword does not take arguments and must be written with its terminating semicolon.

## When to use

- When closing a block that was opened with [`:BEGININLINECODE`](BEGININLINECODE.md).
- When defining named inline SSL that you plan to retrieve later with [`GetInlineCode`](../functions/GetInlineCode.md)`()`.
- When you want the following statements in the script to continue after the inline block declaration.

## Syntax

```ssl
:ENDINLINECODE;
```

## Keyword group

**Group:** Organization
**Role:** closer

## Best practices

!!! success "Do"
    - Close every [`:BEGININLINECODE`](BEGININLINECODE.md) block explicitly with `:ENDINLINECODE;`.
    - Put `:ENDINLINECODE;` on its own line so the block boundary is obvious.
    - Keep the inline body valid SSL so the script compiles cleanly.

!!! failure "Don't"
    - Omit `:ENDINLINECODE;` — the inline block must be closed explicitly.
    - Use `:ENDINLINECODE;` without a matching [`:BEGININLINECODE`](BEGININLINECODE.md) — the script will not compile.
    - Treat `:ENDINLINECODE;` as an executable statement with arguments. It only closes the inline block.

## Caveats

- The block body before `:ENDINLINECODE;` must be valid SSL.
- Use [`REGION`](REGION.md) instead when you need stored text that is not validated as executable SSL.

## Examples

### Close an inline block before retrieving it

Defines a named inline block that calculates a price, closes it with `:ENDINLINECODE;`, then retrieves and executes the stored code. With `nUnitPrice` set to `25` and `nQuantity` to `4`, the inline block returns `100`.

```ssl
:PROCEDURE CalculateTotalPrice;
	:DECLARE sInlineCode, nTotal;

	:BEGININLINECODE "CalculateTotal";
		:DECLARE nUnitPrice, nQuantity;

		nUnitPrice := 25;
		nQuantity := 4;

		:RETURN nUnitPrice * nQuantity;
	:ENDINLINECODE;

	sInlineCode := GetInlineCode("CalculateTotal");
	nTotal := ExecUdf(sInlineCode,, .F.);

	DeleteInlineCode("CalculateTotal");

	UsrMes("Total price: " + LimsString(nTotal));

	:RETURN nTotal;
:ENDPROC;

/* Usage;
DoProc("CalculateTotalPrice");
```

`UsrMes` displays:

```
Total price: 100
```

## Related

- [`BEGININLINECODE`](BEGININLINECODE.md)
- [`GetInlineCode`](../functions/GetInlineCode.md)
- [`DeleteInlineCode`](../functions/DeleteInlineCode.md)
