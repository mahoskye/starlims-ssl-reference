---
title: "DecryptData"
summary: "Decrypts an encrypted string with a password and returns the plaintext string."
id: ssl.function.decryptdata
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DecryptData

Decrypts an encrypted string with a password and returns the plaintext string.

`DecryptData` takes encrypted text and a password, then returns the decrypted string. If `sInputData` is [`NIL`](../literals/nil.md) or an empty string, the function returns an empty string without validating `sPassword`. Otherwise, if `sPassword` is [`NIL`](../literals/nil.md) or an empty string, the function raises an error. If the password is wrong or the value cannot be decrypted, the function returns an empty string instead of raising. Use it when you need to recover data that was previously encrypted, such as values produced by [`EncryptData`](EncryptData.md). For one-way transformations, use [`HashData`](HashData.md).

## When to use

- When you need to recover plaintext from data that was previously encrypted.
- When your script must treat decryption failure as a normal branch by checking for an empty-string result.
- When you need reversible protection rather than one-way hashing.

## Syntax

```ssl
DecryptData(sInputData, sPassword)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sInputData` | [string](../types/string.md) | yes | — | The encrypted string to decrypt. If this value is [`NIL`](../literals/nil.md) or empty, the function returns an empty string. |
| `sPassword` | [string](../types/string.md) | yes | — | The password used for decryption. If this value is [`NIL`](../literals/nil.md) or empty and `sInputData` is not empty, the function raises an error. |

## Returns

**[string](../types/string.md)** — The decrypted plaintext. Returns an empty string when `sInputData` is empty or when the supplied value cannot be decrypted.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sPassword` is [`NIL`](../literals/nil.md) or empty and `sInputData` is not empty. | `Password cannot be null or empty string.` |

## Best practices

!!! success "Do"
    - Validate that `sPassword` is present before calling the function.
    - Treat an empty-string return as a failed decryption attempt and handle it explicitly.
    - Keep the encryption and decryption workflow paired with the same business process so you know which password to use.

!!! failure "Don't"
    - Assume a failed decryption will raise an error. Wrong passwords and unreadable ciphertext return an empty string instead.
    - Pass an empty password and rely on exception handling as your main validation path. Check inputs before calling.
    - Treat an empty-string result as valid decrypted content when the source data should contain a real value.

## Caveats

- Empty `sInputData` and a failed decryption both produce an empty-string result, so validate the calling context if that distinction matters.
- The function only accepts `sInputData` and `sPassword`. It does not expose algorithm, key-length, or return-format options at the call site.

## Examples

### Decrypt a stored value

Uses a sample encrypted value representing a stored profile setting, decrypts it with `DecryptData`, and handles the empty-string result that indicates decryption failure.

```ssl
:PROCEDURE ShowDecryptedEmail;
    :DECLARE sEncryptedEmail, sPassword, sEmail;

    sPassword := "SecureP@ssw0rd";
    sEncryptedEmail := EncryptData("alex@example.com", sPassword, "3DES", "128", "BASE64");

    sEmail := DecryptData(sEncryptedEmail, sPassword);

    :IF Empty(sEmail);
        UsrMes("Email could not be decrypted");
        :RETURN "";
    :ENDIF;

    UsrMes("Decrypted email: " + sEmail); /* Displays decrypted email value;

    :RETURN sEmail;
:ENDPROC;

/* Usage;
DoProc("ShowDecryptedEmail");
```

### Validate required input and handle failure

Guards against an empty password before calling `DecryptData`, then handles the empty-string result that indicates a wrong password or unreadable ciphertext.

```ssl
:PROCEDURE ReadSecretNote;
    :PARAMETERS sEncryptedNote, sPassword;
    :DECLARE sNote;

    :IF Empty(sPassword);
        UsrMes("Cannot decrypt note because the password is empty");
        :RETURN "";
    :ENDIF;

    sNote := DecryptData(sEncryptedNote, sPassword);

    :IF Empty(sNote);
        UsrMes("The note could not be decrypted with the supplied password");
        :RETURN "";
    :ENDIF;

    :RETURN sNote;
:ENDPROC;

/* Usage;
DoProc(
    "ReadSecretNote",
    {EncryptData("example note", "SecureP@ssw0rd"), "SecureP@ssw0rd"}
);
```

### Round-trip verification with EncryptData

Encrypts a connection string with [`EncryptData`](EncryptData.md), decrypts it with `DecryptData`, and confirms the round-trip produces the original value.

```ssl
:PROCEDURE VerifyEncryptedSetting;
    :DECLARE sPlainText, sPassword, sEncrypted, sDecrypted;
    :DECLARE bMatches;

    sPlainText := "Server=LAB01|User=api_user|Mode=readonly";
    sPassword := "MySecureP@ssw0rd";

    sEncrypted := EncryptData(sPlainText, sPassword, "3DES", "128", "BASE64");
    sDecrypted := DecryptData(sEncrypted, sPassword);

    bMatches := sDecrypted == sPlainText;

    :IF !bMatches;
        ErrorMes("Encrypted setting verification failed");
        :RETURN .F.;
    :ENDIF;

    UsrMes("Encrypted setting verified successfully");

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("VerifyEncryptedSetting");
```

## Related

- [`EncryptData`](EncryptData.md)
- [`HashData`](HashData.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
