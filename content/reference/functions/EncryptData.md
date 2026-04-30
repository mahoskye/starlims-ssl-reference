---
title: "EncryptData"
summary: "Encrypts a string with a password by using the legacy built-in RC2, DES, or 3DES algorithms."
id: ssl.function.encryptdata
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# EncryptData

Encrypts a string with a password by using the legacy built-in `RC2`, `DES`, or `3DES` algorithms.

`EncryptData` returns an empty string when `sInputData` or `sPassword` is empty. When values are supplied, it encrypts the text and returns a STARLIMS-formatted encrypted string that includes the information needed by [`DecryptData`](DecryptData.md) to choose the algorithm and key size during decryption. If `sAlgorithm` is omitted, the function uses `3DES`. If `sKey` is omitted, it uses `128`. If `sRetType` is omitted, it defaults to `BASE64`.

This function is best suited to legacy interoperability or existing reversible encryption flows. For one-way hashing, use [`HashData`](HashData.md).

## When to use

- When you need to produce a value that [`DecryptData`](DecryptData.md) can later reverse.
- When you must match an existing STARLIMS encryption flow that already uses `RC2`, `DES`, or `3DES`.
- When you need to encrypt a non-empty string before storing or transmitting it within an established legacy integration.

## Syntax

```ssl
EncryptData(sInputData, sPassword, [sAlgorithm], [sKey], [sRetType])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sInputData` | [string](../types/string.md) | yes | — | Plaintext to encrypt. If empty, the function returns `""`. |
| `sPassword` | [string](../types/string.md) | yes | — | Password used to derive the encryption key. If empty, the function returns `""`. |
| `sAlgorithm` | [string](../types/string.md) | no | `3DES` | Encryption algorithm. Supported values are `RC2`, `DES`, and `3DES`. |
| `sKey` | [string](../types/string.md) | no | `128` | Requested key length in bits as a string, or `MAX`. |
| `sRetType` | [string](../types/string.md) | no | `BASE64` | Optional return-type argument retained by the public signature. |

## Returns

**[string](../types/string.md)** — The encrypted value. Successful results begin with a STARLIMS encryption header, followed by the encoded encrypted payload. If `sInputData` or `sPassword` is empty, the function returns `""`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sAlgorithm` is not `RC2`, `DES`, or `3DES`. | `Invalid Encryption Algorithm` |
| `sKey` is neither a valid integer string nor `MAX`. | `Invalid Key Length` |
| The numeric key size is outside the range supported by the selected algorithm. | `Invalid key size: {key}. Min size: {min}, Max size: {max}, Skip size: {skip}` |

## Best practices

!!! success "Do"
    - Use the same password for both `EncryptData` and [`DecryptData`](DecryptData.md).
    - Validate that `sInputData` and `sPassword` are not empty before treating the result as a usable encrypted value.
    - Standardize the algorithm and key length across the systems that produce and consume the encrypted value.

!!! failure "Don't"
    - Use this function for one-way password hashing. Use [`HashData`](HashData.md) when the value should not be decrypted later.
    - Assume an empty return value means encryption succeeded with an empty payload. It also means `sInputData` or `sPassword` was empty.
    - Pass arbitrary algorithm or key values from user input without validation. Invalid values raise runtime errors.

## Caveats

- `sKey` is a key length setting such as `128` or `MAX`, not the password text itself.
- The public signature includes `sRetType`, but the return format is always the STARLIMS-formatted encrypted string expected by [`DecryptData`](DecryptData.md).

## Examples

### Encrypt a value with defaults

Use the required arguments only and let the function apply its default algorithm and key length.

```ssl
:PROCEDURE EncryptSampleID;
    :DECLARE sInputData, sPassword, sEncrypted;

    sInputData := "LAB-2026-0001";
    sPassword := "LabSharedSecret";

    sEncrypted := EncryptData(sInputData, sPassword);

    :IF Empty(sEncrypted);
        ErrorMes("Encryption failed because required input was empty");
        :RETURN "";
    :ENDIF;

    UsrMes("Encrypted value created");
    /* Displays: Encrypted value created;

    :RETURN sEncrypted;
:ENDPROC;

/* Usage;
DoProc("EncryptSampleID");
```

### Specify algorithm and key length

Pass an explicit algorithm and key length when an existing integration expects fixed settings.

```ssl
:PROCEDURE EncryptInterfacePayload;
    :DECLARE sInputData, sPassword, sAlgorithm, sKey, sEncrypted;

    sInputData := '{"sample":"LAB-2026-0001","status":"Logged"}';
    sPassword := "InterfaceSecret";
    sAlgorithm := "3DES";
    sKey := "128";

    sEncrypted := EncryptData(sInputData, sPassword, sAlgorithm, sKey);

    :IF Empty(sEncrypted);
        ErrorMes("Payload encryption failed");
        /* Displays on failure: Payload encryption failed;
        :RETURN "";
    :ENDIF;

    :RETURN sEncrypted;
:ENDPROC;

/* Usage;
DoProc("EncryptInterfacePayload");
```

### Encrypt multiple fields and verify round-trip

Encrypt several values with shared settings, then verify one of them by decrypting it with the same password.

```ssl
:PROCEDURE BuildEncryptedPatientData;
    :DECLARE sPassword, sAlgorithm, sKey;
    :DECLARE sPatientID, sResultCode, sComment;
    :DECLARE sEncPatientID, sEncResultCode, sEncComment, sVerify;
    :DECLARE oPayload;

    sPassword := "PatientExchangeSecret";
    sAlgorithm := "3DES";
    sKey := "128";

    sPatientID := "P-100245";
    sResultCode := "POS";
    sComment := "Handle as restricted data";

    sEncPatientID := EncryptData(sPatientID, sPassword, sAlgorithm, sKey);
    sEncResultCode := EncryptData(sResultCode, sPassword, sAlgorithm, sKey);
    sEncComment := EncryptData(sComment, sPassword, sAlgorithm, sKey);

    sVerify := DecryptData(sEncPatientID, sPassword);

    :IF !(sVerify == sPatientID);
        ErrorMes("Round-trip verification failed");
        /* Displays on failure: Round-trip verification failed;
        :RETURN NIL;
    :ENDIF;

    oPayload := CreateUdObject();
    oPayload:patientID := sEncPatientID;
    oPayload:resultCode := sEncResultCode;
    oPayload:comment := sEncComment;
    oPayload:algorithm := sAlgorithm;
    oPayload:keyLength := sKey;

    :RETURN oPayload;
:ENDPROC;

/* Usage;
DoProc("BuildEncryptedPatientData");
```

## Related

- [`DecryptData`](DecryptData.md)
- [`HashData`](HashData.md)
- [`string`](../types/string.md)
