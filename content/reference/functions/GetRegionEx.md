---
title: "GetRegionEx"
summary: "Retrieves a named region string, optionally using a caller-supplied local region map before falling back to the current region scope."
id: ssl.function.getregionex
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetRegionEx

Retrieves a named region string, optionally using a caller-supplied local region map before falling back to the current region scope.

`GetRegionEx` behaves like [`GetRegion`](GetRegion.md), but it checks `oLocalRegions` first when that argument contains a compatible local region map. Region names are matched case-insensitively. If both `aSourceValues` and `aDestinationValues` are supplied, the function applies each replacement pair in order to the retrieved text and returns the updated string.

## When to use

- When you need the same behavior as [`GetRegion`](GetRegion.md), but want a caller-supplied local region map to take precedence.
- When stored region text contains placeholders that should be replaced after lookup.
- When a shared script receives region overrides from surrounding code and still needs a fallback to the current region scope.

## Syntax

```ssl
GetRegionEx(sRegionName, [aSourceValues], [aDestinationValues], [oLocalRegions])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sRegionName` | [string](../types/string.md) | yes | — | Region name to look up. Matching is case-insensitive. |
| `aSourceValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Source strings to replace in the retrieved region text. Replacements are only attempted when both `aSourceValues` and `aDestinationValues` are supplied. |
| `aDestinationValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Replacement strings corresponding to `aSourceValues`. Must contain the same number of elements as `aSourceValues`. |
| `oLocalRegions` | [object](../types/object.md) | no | [`NIL`](../literals/nil.md) | Compatible local region map to check before the current region scope. If this argument is omitted or not compatible, normal scope lookup is used. |

## Returns

**[string](../types/string.md)** — The matched region text. When both `aSourceValues` and `aDestinationValues` are supplied, token replacements are applied in order before returning. Returns an empty string when no global region storage has been initialized and no local override supplies the requested name.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sRegionName` is [`NIL`](../literals/nil.md). | `Argument cannot be null.` |
| `sRegionName` is not a string. | `Argument must be of type string.` |
| `aSourceValues` or `aDestinationValues` is not an array. | `Invalid arguments for GetRegion! Should be: string, array, array.` |
| `aSourceValues` and `aDestinationValues` have different lengths. | `Invalid arguments for GetRegion! Source array's length is not equal with destination array's length.` |
| The region name is not found in either the local override map or the current region scope. The value substituted for `<sRegionName>` is the lowercased region name. | `GetRegion: <sRegionName> not in scope.` |

## Best practices

!!! success "Do"
    - Use `GetRegionEx` only when you genuinely need local overrides. Prefer [`GetRegion`](GetRegion.md) for normal scope-based lookups.
    - Pass `aSourceValues` and `aDestinationValues` as parallel arrays of equal length when doing token replacement.
    - Wrap the call in `:TRY / :CATCH` when the region may be missing.

!!! failure "Don't"
    - Pass a non-string value as `sRegionName`. The function raises an error instead of converting it.
    - Pass only one replacement array and expect partial substitution. If either array is missing, no replacements are performed.
    - Assume a local override object will always be honored. If it is not compatible, the function falls back to the normal region scope.

## Caveats

- Replacements are applied in order, so overlapping source values can affect the final result.

## Examples

### Look up a region by name

Retrieves a named region without any token substitution, wrapping the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) so that a missing region name can be reported without halting the procedure.

```ssl
:PROCEDURE ShowRegionText;
	:DECLARE oErr, sResult;

	:TRY;
		sResult := GetRegionEx("InvoiceHeader");
		UsrMes(sResult);
		/* Displays the InvoiceHeader region text;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes(oErr:Description);
		/* Displays on error: missing region message;
		:RETURN "";
	:ENDTRY;

	:RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("ShowRegionText");
```

### Replace placeholder tokens after lookup

Retrieves a template region and replaces `{CUSTOMER}` and `{DATE}` placeholders in one call by passing parallel source and destination arrays. The exact output depends on what `InvoiceTemplate` contains in the region scope.

```ssl
:PROCEDURE BuildInvoiceHeader;
	:DECLARE aDst, aSrc, sHeader;

	aSrc := {"{CUSTOMER}", "{DATE}"};
	aDst := {"Acme Corp", DToC(Today())};

	sHeader := GetRegionEx("InvoiceTemplate", aSrc, aDst);

	UsrMes(sHeader);

	:RETURN sHeader;
:ENDPROC;

/* Usage;
DoProc("BuildInvoiceHeader");
```

[`UsrMes`](UsrMes.md) displays this output when `InvoiceTemplate` = `"Invoice for {CUSTOMER} dated {DATE}"`:

```text
Invoice for Acme Corp dated 23/04/2026
```

### Override region lookup with a local region map

Passes a caller-supplied local region map as `oLocalRegions` so that the local map is checked first; if the name is found there it overrides the global scope, otherwise the fallback lookup proceeds normally. The [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) guards against missing region names in both sources.

```ssl
:PROCEDURE ResolveImportRegion;
	:PARAMETERS oLocalRegions, sSampleID;
	:DECLARE aDst, aSrc, oErr, sRegionText;

	aSrc := {"{SAMPLE}"};
	aDst := {sSampleID};

	:TRY;
		sRegionText := GetRegionEx("ImportTemplate", aSrc, aDst, oLocalRegions);
		UsrMes(sRegionText);
		/* Displays the resolved import template text;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("ResolveImportRegion failed: " + oErr:Description);
		/* Displays on error: import lookup failed;
		:RETURN "";
	:ENDTRY;

	:RETURN sRegionText;
:ENDPROC;

/* Usage;
DoProc("ResolveImportRegion", {NIL, "LAB-001"});
```

## Related

- [`DeleteInlineCode`](DeleteInlineCode.md)
- [`GetInlineCode`](GetInlineCode.md)
- [`GetRegion`](GetRegion.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
