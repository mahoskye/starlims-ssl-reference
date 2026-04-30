---
title: "UrlEncode"
summary: "Converts a string into a format safe for inclusion in a URL by encoding unsafe characters."
id: ssl.function.urlencode
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# UrlEncode

Converts a string into a format safe for inclusion in a URL by encoding unsafe characters.

`UrlEncode` returns the encoded form of `sData` for use in URL values such as query parameters or path segments. If `sData` is [`NIL`](../literals/nil.md), the function returns [`NIL`](../literals/nil.md). If `sData` is not a [string](../types/string.md), the function raises an error. Use [`UrlDecode`](UrlDecode.md) when you need to reverse the operation.

## When to use

- When adding user-entered text to a query string.
- When building URL path segments from dynamic names or identifiers.
- When preparing redirect targets or download links that include spaces or reserved characters.

## Syntax

```ssl
UrlEncode(sData)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sData` | [string](../types/string.md) | yes | — | The string to encode. When [`NIL`](../literals/nil.md), the function returns [`NIL`](../literals/nil.md). |

## Returns

**[string](../types/string.md)** — The encoded string. Returns [`NIL`](../literals/nil.md) when `sData` is [`NIL`](../literals/nil.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sData` is not a string. | `Argument <sData> must be a string.` |

## Best practices

!!! success "Do"
    - Encode each dynamic URL value before concatenating it into the final URL.
    - Guard optional inputs when [`NIL`](../literals/nil.md) is a valid upstream value.
    - Pair `UrlEncode` with [`UrlDecode`](UrlDecode.md) when a workflow needs round-trip URL data handling.

!!! failure "Don't"
    - Pass numbers, arrays, or objects directly to `UrlEncode`. The function requires a string.
    - Encode an entire URL when only one value is dynamic. Encode the individual value, then assemble the URL.
    - Encode the same value repeatedly without confirming whether it was already encoded.

## Examples

### Add user input to a query string

Encode one dynamic value before appending it to a query string. Spaces become [`+`](../operators/plus.md) and special characters such as `'` and [`&`](../operators/and.md) become percent-encoded sequences.

```ssl
:PROCEDURE BuildSearchUrl;
	:DECLARE sCompanyName, sEncodedCompany, sBaseUrl, sUrl;

	sCompanyName := "O'Reilly & Associates";
	sBaseUrl := "https://example.com/api/search";

	sEncodedCompany := UrlEncode(sCompanyName);
	sUrl := sBaseUrl + "?company=" + sEncodedCompany;

	UsrMes(sUrl);

	:RETURN sUrl;
:ENDPROC;

/* Usage;
DoProc("BuildSearchUrl");
```

[`UsrMes`](UsrMes.md) displays:

```
https://example.com/api/search?company=O%27Reilly+%26+Associates
```

### Encode multiple query parameter values

Encode each user-supplied value separately before building the final URL. Encoding values one at a time prevents accidental double-encoding of the [`&`](../operators/and.md) separator.

```ssl
:PROCEDURE BuildOrderLookupUrl;
	:PARAMETERS sOrderNo, sStatus;
	:DECLARE sEncodedOrderNo, sEncodedStatus, sUrl;

	sEncodedOrderNo := UrlEncode(sOrderNo);
	sEncodedStatus := UrlEncode(sStatus);

	sUrl := "https://example.com/orders?ordno=" + sEncodedOrderNo
	+ "&status=" + sEncodedStatus;

	:RETURN sUrl;
:ENDPROC;

/* Usage;
DoProc("BuildOrderLookupUrl", {"ORD-2024-001", "PENDING REVIEW"});
```

### Encode optional filters and path segments

Combine required path segments with an optional query value while preserving [`NIL`](../literals/nil.md) behavior for the optional input. When `sFilter` is [`NIL`](../literals/nil.md), the URL omits the filter parameter entirely.

```ssl
:PROCEDURE BuildDownloadUrl;
	:PARAMETERS sFolderName, sFileName, sFilter;
	:DECLARE sFolderSegment, sFileSegment, sUrl, sEncodedFilter;

	sFolderSegment := UrlEncode(sFolderName);
	sFileSegment := UrlEncode(sFileName);

	sUrl := "https://example.com/files/" + sFolderSegment + "/" + sFileSegment;

	:IF !(sFilter == NIL);
		sEncodedFilter := UrlEncode(sFilter);
		sUrl += "?filter=" + sEncodedFilter;
	:ENDIF;

	:RETURN sUrl;
:ENDPROC;

/* Usage;
DoProc("BuildDownloadUrl", {"Reports", "annual summary.pdf", "2024"});
```

## Related

- [`UrlDecode`](UrlDecode.md)
- [`string`](../types/string.md)
