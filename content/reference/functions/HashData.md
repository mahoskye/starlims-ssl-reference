---
title: "HashData"
summary: "Computes a one-way hash string from input text."
id: ssl.function.hashdata
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# HashData

Computes a one-way hash string from input text.

`HashData` hashes `sInputData` and returns the result as a hexadecimal string. If `sAlgorithm` is omitted or passed as [`NIL`](../literals/nil.md), the function uses `"SH1"`. The only supported algorithm names are `"SH1"` and `"MD5"`. Passing [`NIL`](../literals/nil.md) for `sInputData` raises an error. Passing an unsupported algorithm raises an error.

Use `HashData` when you need a repeatable, non-reversible fingerprint of a string. For reversible protection, use [`EncryptData`](EncryptData.md) and [`DecryptData`](DecryptData.md) instead.

## When to use

- When you need to compare a current string value to a previously stored hash.
- When an existing STARLIMS workflow expects `SH1` or `MD5` hashes.
- When you need a one-way transformation rather than reversible encryption.

## Syntax

```ssl
HashData(sInputData, [sAlgorithm])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sInputData` | [string](../types/string.md) | yes | — | String value to hash. Passing [`NIL`](../literals/nil.md) raises an error. An empty string is allowed and hashes successfully. |
| `sAlgorithm` | [string](../types/string.md) | no | `SH1` | Hash algorithm name. Supported values are `SH1` and `MD5`. If omitted or [`NIL`](../literals/nil.md), `SH1` is used. |

## Returns

**[string](../types/string.md)** — An uppercase hexadecimal hash string for `sInputData`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sInputData` is [`NIL`](../literals/nil.md). | `HashData`. (Note: the runtime uses the function name as the exception message text — it is not descriptive.) |
| `sAlgorithm` is not `"SH1"` or `"MD5"`. | `Invalid Hashing Algorithm` |

## Best practices

!!! success "Do"
    - Standardize on one algorithm for a given workflow so stored hashes remain comparable.
    - Handle runtime errors when `sInputData` may be [`NIL`](../literals/nil.md) or `sAlgorithm` may come from external input.
    - Record which algorithm produced the hash when values may be shared across systems.

!!! failure "Don't"
    - Pass algorithm names such as `SHA1` or `SHA256`. `HashData` only accepts `SH1` and `MD5`.
    - Switch algorithms for existing stored hashes without a migration plan. The same input produces different hashes under different algorithms.
    - Use `HashData` when you need to recover the original value later. Use [`EncryptData`](EncryptData.md) for reversible storage.

## Caveats

- `sAlgorithm` is case-insensitive, but the accepted values are still limited to `SH1` and `MD5`.
- `HashData("")` is valid and returns the hash of the empty string.
- The same input hashed with `SH1` and `MD5` produces different results.

## Examples

### Hash a value with the default algorithm

Hash a string with the default `SH1` algorithm and compare it to a known hash.

```ssl
:PROCEDURE VerifySampleToken;
    :DECLARE sToken, sExpectedHash, sActualHash;

    sToken := "LAB-2026-0001";
    sExpectedHash := HashData("LAB-2026-0001");
    sActualHash := HashData(sToken);

    :IF sActualHash == sExpectedHash;
        UsrMes("Token hash matched");
        :RETURN .T.;
    :ENDIF;

    UsrMes("Token hash did not match");

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("VerifySampleToken");
```

### Use an explicit algorithm for an external interface

Specify `MD5` explicitly when an existing integration expects that algorithm.

```ssl
:PROCEDURE BuildLegacyHashRecord;
    :DECLARE sPayload, sHash, oRecord;

    sPayload := "sample=LAB-2026-0001|status=Logged|user=apiuser";
    sHash := HashData(sPayload, "MD5");

    oRecord := CreateUdObject();
    oRecord:payload := sPayload;
    oRecord:algorithm := "MD5";
    oRecord:hash := sHash;

    :RETURN oRecord;
:ENDPROC;

/* Usage;
DoProc("BuildLegacyHashRecord");
```

### Validate user-supplied algorithm input

Catch the runtime error when the requested algorithm is not supported.

```ssl
:PROCEDURE SafeHashWithRequestedAlgorithm;
    :PARAMETERS sInputData, sAlgorithm;
    :DECLARE sHash, oErr;

    :TRY;
        sHash := HashData(sInputData, sAlgorithm);

        :RETURN sHash;
    :CATCH;
        oErr := GetLastSSLError();
        UsrMes("Hashing failed: " + oErr:Description);
        /* Displays on failure: hashing failed with the runtime error;

        :RETURN "";
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("SafeHashWithRequestedAlgorithm", {"my-data", "SHA256"});
```

## Related

- [`DecryptData`](DecryptData.md)
- [`EncryptData`](EncryptData.md)
- [`string`](../types/string.md)
