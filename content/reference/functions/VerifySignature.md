---
title: "VerifySignature"
summary: "Verifies a base64-encoded digital signature against a string by using the public key from a supplied X.509 certificate."
id: ssl.function.verifysignature
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# VerifySignature

Verifies a base64-encoded digital signature against a string by using the public key from a supplied X.509 certificate.

`VerifySignature` loads `sCertificateString` as a raw base64-encoded DER certificate, converts `sData` to UTF-8 bytes, decodes `sSignature` from base64, and checks whether the signature matches the data. The function returns [`.T.`](../literals/true.md) only when all inputs are well-formed and the signature verifies successfully. Malformed inputs raise an error instead of returning [`.F.`](../literals/false.md).

Use this function when you already have the expected certificate and need to confirm that a payload was signed with the matching private key. It verifies the signature only. It does not establish whether the certificate is trusted, current, or approved for your workflow.

## When to use

- When you need to validate that an incoming payload was signed by the holder of
  a known certificate.
- When you need a [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md) result for a signature check after normalizing the certificate, payload, and signature inputs.
- When you need to distinguish a genuine signature mismatch from malformed input by wrapping the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md).

## Syntax

```ssl
VerifySignature(sCertificateString, sData, sSignature)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCertificateString` | [string](../types/string.md) | yes | — | Raw base64-encoded DER X.509 certificate containing the public key used for verification. PEM text is not accepted directly. |
| `sData` | [string](../types/string.md) | yes | — | Original string that was signed. Verification uses the UTF-8 bytes of this exact value. |
| `sSignature` | [string](../types/string.md) | yes | — | Base64-encoded signature to verify against `sData`. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the signature matches `sData` for the supplied certificate; [`.F.`](../literals/false.md) when the inputs are well-formed but the signature does not match.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCertificateString` is empty, [`NIL`](../literals/nil.md), not valid base64, not a DER certificate, or does not expose a supported public key for this verification. | Raises an error. |
| `sData` is [`NIL`](../literals/nil.md). | Raises an error. |
| `sSignature` is [`NIL`](../literals/nil.md) or not valid base64. Unsupported or malformed signature content can also raise an error. | Raises an error. |

## Best practices

!!! success "Do"
    - Convert PEM certificates to the raw base64 DER body before calling `VerifySignature`.
    - Preserve the exact original payload string. Even small text changes cause verification to fail.
    - Wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when certificate or signature data comes from external systems.

!!! failure "Don't"
    - Treat [`.F.`](../literals/false.md) as the only failure mode. Bad certificate or signature input raises an error instead.
    - Assume a certificate is trusted just because `VerifySignature` returns [`.T.`](../literals/true.md). Trust, expiry, and revocation checks are separate concerns.
    - Pass PEM headers, footer lines, or embedded formatting directly as `sCertificateString`.

## Caveats

- `VerifySignature` verifies the signature with the certificate's public key by using a SHA-1 digest of the UTF-8 bytes of `sData`.

## Examples

### Verify a signed payload

Check whether a payload signature is valid and branch on the boolean result. The function returns [`.T.`](../literals/true.md) only when the signature passes; a mismatch returns [`.F.`](../literals/false.md) without raising an error.

```ssl
:PROCEDURE VerifySignedPayload;
    :DECLARE sCertificate, sPayload, sSignature, bIsValid;

    sCertificate := "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtestcertificate";
    sPayload := "ORDER|2026-04-19|ACME-1001|APPROVED";
    sSignature := "MEUCIQCexamplebase64signaturevalue";

    bIsValid := VerifySignature(sCertificate, sPayload, sSignature);

    :IF bIsValid;
        UsrMes("Signature is valid");
        :RETURN .T.;
    :ENDIF;

    UsrMes("Signature did not match the payload");

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("VerifySignedPayload");
```

### Handle malformed partner input

Catch malformed certificate or signature data separately from a normal mismatch. A [`.F.`](../literals/false.md) result from a well-formed input is handled without a [`:CATCH`](../keywords/CATCH.md); an exception from bad input is handled in the [`:CATCH`](../keywords/CATCH.md) block.

```ssl
:PROCEDURE ValidatePartnerMessage;
    :PARAMETERS sCertificate, sPayload, sSignature;
    :DECLARE bIsValid, oErr;

    :TRY;
        bIsValid := VerifySignature(sCertificate, sPayload, sSignature);

        :IF bIsValid;
            UsrMes("Partner message verified");
            :RETURN .T.;
        :ENDIF;

        ErrorMes("Partner message signature did not match");

        :RETURN .F.;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Partner message could not be verified: " + oErr:Description);  /* Displays a verification error;

        :RETURN .F.;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ValidatePartnerMessage", {"MIIBIjANBgkq...", "ORDER|2026-04-19|ACME-1001", "MEUCIQCexample..."});
```

### Verify multiple signed records in one pass

Loop through a batch of signed records, track mismatches, and capture malformed records separately. The third record uses `"not-base64"` as its signature, which raises an error that lands in the [`:CATCH`](../keywords/CATCH.md) block.

```ssl
:PROCEDURE AuditSignedRecords;
    :DECLARE sCertificate, aRecords, aFailedIds, aErrorIds;
    :DECLARE nIndex, bIsValid, oErr;

    sCertificate := "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtestcertificate";
    aRecords := {
        {"REC-001", "alpha|100", "MEQCIFirstExampleSignature"},
        {"REC-002", "beta|200", "MEQCSecondExampleSignature"},
        {"REC-003", "gamma|300", "not-base64"}
    };
    aFailedIds := {};
    aErrorIds := {};

    :FOR nIndex := 1 :TO ALen(aRecords);
        :TRY;
            bIsValid := VerifySignature(
                sCertificate,
                aRecords[nIndex, 2],
                aRecords[nIndex, 3]
            );

            :IF !bIsValid;
                AAdd(aFailedIds, aRecords[nIndex, 1]);
            :ENDIF;

        :CATCH;
            oErr := GetLastSSLError();
            AAdd(aErrorIds, aRecords[nIndex, 1]);
            UsrMes("Record " + aRecords[nIndex, 1] + " raised an error: " + oErr:Description);  /* Displays the record error;
        :ENDTRY;
    :NEXT;

    :IF ALen(aFailedIds) > 0;
        UsrMes("Signature mismatches: " + LimsString(ALen(aFailedIds)));
    :ENDIF;

    :IF ALen(aErrorIds) > 0;
        ErrorMes("Malformed records: " + LimsString(ALen(aErrorIds)));
    :ENDIF;

    :RETURN ALen(aFailedIds) == 0 .AND. ALen(aErrorIds) == 0;
:ENDPROC;

/* Usage;
DoProc("AuditSignedRecords");
```

## Related

- [`HashData`](HashData.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
