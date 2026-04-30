---
title: "SetDecimalSeparator"
summary: "Sets the current decimal separator and returns the previous setting."
id: ssl.function.setdecimalseparator
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SetDecimalSeparator

Sets the current decimal separator and returns the previous setting.

`SetDecimalSeparator` updates the current decimal separator to the supplied single-character string. The function returns the previous separator as a string, then stores the new value. If the current setting was empty before the call, the returned previous value is also empty.

## When to use

- When code must switch between `.` and `,` for locale-specific numeric text.
- When you need to save the current separator, apply a temporary one, then restore the original value.
- When existing logic needs the previous separator returned directly from the setter.

## Syntax

```ssl
SetDecimalSeparator(sDecimalSep)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDecimalSep` | [string](../types/string.md) | yes | — | New decimal separator. It must be exactly one character long. |

## Returns

**[string](../types/string.md)** — The previous decimal separator value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDecimalSep` is [`NIL`](../literals/nil.md). | `Argument: sDecimalSep cannot be null.` |
| `sDecimalSep` is empty or has more than one character. | `Wrong value for argument: sDecimalSep` |

## Best practices

!!! success "Do"
    - Save the returned value when you need to restore the previous separator later.
    - Pass a one-character string such as `"."` or `","`.
    - Use [`GetDecimalSeparator`](GetDecimalSeparator.md) when you need to check the current setting without changing it.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), `""`, or a multi-character string such as `".."`.
    - Change the separator temporarily without restoring the previous value afterward.
    - Use [`GetDecimalSep`](GetDecimalSep.md) when you need the separator as a string. That function returns a numeric character code, not the string value.

## Caveats

- This function changes a shared decimal separator setting.
- Unlike [`GetDecimalSep`](GetDecimalSep.md), this function does not provide a `.` fallback for an empty current setting before the change.

## Examples

### Set the separator and keep the previous value

Change the decimal separator to a comma and keep the old value so it can be restored later.

```ssl
:PROCEDURE UseCommaSeparator;
	:DECLARE sPreviousSep, sCurrentSep;

	sPreviousSep := SetDecimalSeparator(",");
	sCurrentSep := GetDecimalSeparator();

	UsrMes("Previous separator: " + sPreviousSep);  /* Displays previous separator value;
	UsrMes("Current separator: " + sCurrentSep);
:ENDPROC;

/* Usage;
DoProc("UseCommaSeparator");
```

### Restore the previous separator after temporary work

Switch the separator for a short operation, then restore the prior setting.

```ssl
:PROCEDURE FormatWithTemporarySeparator;
	:DECLARE sPreviousSep, sMessage;

	sPreviousSep := SetDecimalSeparator(",");

	sMessage := "Current separator while formatting: " + GetDecimalSeparator();
	UsrMes(sMessage);

	SetDecimalSeparator(sPreviousSep);
	UsrMes("Restored separator: " + GetDecimalSeparator());  /* Displays restored separator value;
:ENDPROC;

/* Usage;
DoProc("FormatWithTemporarySeparator");
```

### Restore the separator safely using TRY and FINALLY

Use [`:TRY`](../keywords/TRY.md) and [`:FINALLY`](../keywords/FINALLY.md) so the original separator is restored even if later work fails.

```ssl
:PROCEDURE ProcessWithDecimalSeparator;
	:PARAMETERS sNewSep;
	:DECLARE sPreviousSep, oErr;

	sPreviousSep := SetDecimalSeparator(sNewSep);

	:TRY;
		UsrMes("Processing with separator: " + GetDecimalSeparator());
		/* Displays current separator value during processing;
	:CATCH;
		oErr := GetLastSSLError();
		UsrMes("Processing failed: " + oErr:Description);
		/* Displays on failure: processing failed;
	:FINALLY;
		SetDecimalSeparator(sPreviousSep);
	:ENDTRY;

	UsrMes("Restored separator: " + GetDecimalSeparator());
	/* Displays restored separator value;
:ENDPROC;

/* Usage;
DoProc("ProcessWithDecimalSeparator", {","});
```

## Related

- [`GetDecimalSep`](GetDecimalSep.md)
- [`GetDecimalSeparator`](GetDecimalSeparator.md)
- [`string`](../types/string.md)
