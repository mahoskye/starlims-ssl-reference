---
title: "UrlDecode"
summary: "Decodes a URL-encoded string."
id: ssl.function.urldecode
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# UrlDecode

Decodes a URL-encoded string.

`UrlDecode` takes a [string](../types/string.md) value and returns its decoded form. If `sData` is [`NIL`](../literals/nil.md), the function returns [`NIL`](../literals/nil.md). If `sData` is not a [string](../types/string.md), the function raises an error. Use it when you receive URL-encoded text and need the readable value in SSL.

## When to use

- When you need to interpret query strings or form data submitted in URLs.
- When processing percent-encoded values returned from web requests or redirects.
- When transforming encoded parameters, such as file names or IDs, back into readable text.
- When reversing values that were previously encoded with [`UrlEncode`](UrlEncode.md).

## Syntax

```ssl
UrlDecode(sData)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sData` | [string](../types/string.md) | yes | — | The URL-encoded string to decode. If `sData` is [`NIL`](../literals/nil.md), the function returns [`NIL`](../literals/nil.md). |

## Returns

**[string](../types/string.md)** — The decoded string. Returns [`NIL`](../literals/nil.md) when `sData` is [`NIL`](../literals/nil.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sData` is not a string. | `Argument <sData> must be a string.` |

## Best practices

!!! success "Do"
    - Decode values at the point where you need the readable text.
    - Guard optional inputs when [`NIL`](../literals/nil.md) is a valid upstream value.
    - Pair `UrlDecode` with [`UrlEncode`](UrlEncode.md) for round-trip URL data handling.

!!! failure "Don't"
    - Pass numbers, arrays, or objects directly to `UrlDecode`. The function requires a string argument.
    - Decode the same value repeatedly without confirming that it was encoded more than once.
    - Assume [`NIL`](../literals/nil.md) becomes an empty string. [`NIL`](../literals/nil.md) stays [`NIL`](../literals/nil.md).

## Examples

### Display readable user input from a web form

Decode a single URL-encoded value before displaying it.

```ssl
:PROCEDURE DecodeWebFormInput;
    :DECLARE sEncodedForm, sDecodedForm;

    sEncodedForm := "John%20Doe%20%26%20Co";
    sDecodedForm := UrlDecode(sEncodedForm);

    UsrMes(sDecodedForm);

    :RETURN sDecodedForm;
:ENDPROC;

/* Usage;
DoProc("DecodeWebFormInput");
```

[`UsrMes`](UsrMes.md) displays:

```
John Doe & Co
```

### Extract a file name from an encoded query parameter

Extract an encoded query parameter from a full URL, guard against a missing input, and then decode the value. The [`NIL`](../literals/nil.md) check prevents an error when no URL was passed.

```ssl
:PROCEDURE ExtractFileNameFromUrl;
    :PARAMETERS sDownloadUrl;
    :DECLARE sQueryString, sFileName, sDecodedName, nParamStart, nAmpersand;

    :IF sDownloadUrl == NIL;
        :RETURN NIL;
    :ENDIF;

    nParamStart := At("filename=", sDownloadUrl);
    :IF nParamStart = 0;
        :RETURN "";
    :ENDIF;

    sQueryString := SubStr(sDownloadUrl, nParamStart + 9);

    nAmpersand := At("&", sQueryString);
    :IF nAmpersand > 0;
        sFileName := Left(sQueryString, nAmpersand - 1);
    :ELSE;
        sFileName := sQueryString;
    :ENDIF;

    sDecodedName := UrlDecode(sFileName);

    UsrMes("Decoded file name: " + sDecodedName);

    :RETURN sDecodedName;
:ENDPROC;

/* Usage;
DoProc("ExtractFileNameFromUrl", {"https://example.com/files?filename=quarterly%20report.pdf"});
```

[`UsrMes`](UsrMes.md) displays:

```
Decoded file name: quarterly report.pdf
```

## Related

- [`UrlEncode`](UrlEncode.md)
- [`string`](../types/string.md)
