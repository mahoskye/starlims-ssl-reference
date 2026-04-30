---
title: "_AND"
summary: "Performs a bitwise AND operation between two integer numbers and returns the result."
id: ssl.function._and
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# _AND

Performs a bitwise AND operation between two integer numbers and returns the result.

`_AND(nValue1, nValue2)` performs a bitwise AND on two integer values and returns the result as a number. Both operands must be whole numbers; fractional values and non-numeric types raise a runtime error.

## When to use

- When you need to check or mask specific bits within an integer—for example, evaluating flag fields or extracting bit-packed data.
- When combining multiple integer values using bitwise AND logic for configuration, permissions, or device communication.
- When implementing low-level algorithms that require manipulation of bits within integers, such as cryptography, compression, or protocol handling.

## Syntax

```ssl
_AND(nValue1, nValue2)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nValue1` | [number](../types/number.md) | yes | — | The first operand for the bitwise AND. Must be a whole number; fractional values raise a runtime error. |
| `nValue2` | [number](../types/number.md) | yes | — | The second operand for the bitwise AND. Must be a whole number; fractional values raise a runtime error. |

## Returns

**[number](../types/number.md)** — The result of the bitwise AND operation between two integers.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `_AND` is called on a non-numeric type. | `the operator/method: _AND is not implemented on type: {type}. Operand: {operand}` |
| Either operand is not a whole number. | `SSLDouble: {value} _AND {v}: invalid operand(s). Expected integers.` |
| `nValue2` is [`NIL`](../literals/nil.md). | `SSLDouble - invalid operand: (of type null) for operator: _AND.` |

## Best practices

!!! success "Do"
    - Ensure both operands are valid integers before using the function.
    - Use this function for bit-level operations such as masking or flag evaluation.
    - Validate or document the input types in your code contracts or comments when using bitwise operations.

!!! failure "Don't"
    - Pass floating-point numbers, strings, or null as operands. Only integer operands produce valid results; other types trigger runtime errors, making error handling and predictable code harder.
    - Use it as a substitute for logical AND (e.g., conditional logic). Bitwise and logical AND have different behavior; confusing the two can cause subtle bugs.
    - Assume silent conversion or automatic error handling for non-integer values. Unhandled type errors will halt execution at runtime, not return a fallback value.

## Caveats

- Bitwise AND does not perform logical conjunction; results may be counterintuitive if used with boolean values or coercible types.

## Examples

### Mask permission flags

Checks a permission integer where bit 0 is read, bit 1 is write, and bit 2 is delete. Masking `nUserPermissions = 5` (binary `101`) against each bit constant shows which permissions are set.

```ssl
:PROCEDURE CheckUserPermission;
	:DECLARE nUserPermissions, nReadPermission, nWritePermission, nDeletePermission;
	:DECLARE bCanRead, bCanWrite, bCanDelete;

	nUserPermissions := 5;
	nReadPermission := 1;
	nWritePermission := 2;
	nDeletePermission := 4;

	bCanRead := _AND(nUserPermissions, nReadPermission) == nReadPermission;
	bCanWrite := _AND(nUserPermissions, nWritePermission) == nWritePermission;
	bCanDelete := _AND(nUserPermissions, nDeletePermission) == nDeletePermission;

	UsrMes("User has Read: " + LimsString(bCanRead));
	UsrMes("User has Write: " + LimsString(bCanWrite));
	UsrMes("User has Delete: " + LimsString(bCanDelete));
:ENDPROC;

/* Usage;
DoProc("CheckUserPermission");
```

[`UsrMes`](UsrMes.md) displays:

```text
User has Read: .T.
User has Write: .F.
User has Delete: .T.
```

### Extract fields from a packed integer

Extracts three byte-sized fields from `nPackedData = 197631` (0x303FF) using byte masks and right-shift. Each mask isolates one byte; the shift moves it to the low position before converting to a readable value.

```ssl
:PROCEDURE ExtractPackedFields;
	:DECLARE nPackedData, nStatusCode, nPriority, nCategory;
	:DECLARE sResult, nMaskLow, nMaskMid, nMaskHigh;

	nMaskLow := 255;
	nMaskMid := 65280;
	nMaskHigh := 16711680;

	nPackedData := 197631;

	nStatusCode := _AND(nPackedData, nMaskLow);
	nPriority := _AND(nPackedData, nMaskMid) >> 8;
	nCategory := _AND(nPackedData, nMaskHigh) >> 16;

	sResult := "Status: " + LimsString(nStatusCode) + " Priority: " + LimsString(nPriority)
				+ " Category: " + LimsString(nCategory);
	UsrMes(sResult);

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ExtractPackedFields");
```

[`UsrMes`](UsrMes.md) displays:

```text
Status: 255 Priority: 3 Category: 3
```

### Decode protocol flags from a packet byte

Decodes `nPacket = 219` (binary `11011011`) into version (bits 0–2), encryption flag (bit 3), compression flag (bit 4), and priority (bits 5–7). Each mask isolates its field; the priority field is shifted right to normalize it.

```ssl
:PROCEDURE DecodeProtocolFlags;
	:DECLARE nPacket, nVersion, nEncrypted, nCompressed, nPriority;
	:DECLARE sReport;

	nPacket := 219;

	nVersion := _AND(nPacket, 7);
	nEncrypted := _AND(nPacket, 8);
	nCompressed := _AND(nPacket, 16);
	nPriority := _AND(nPacket, 224) >> 5;

	sReport := "Packet Flags Decoded" + Chr(13) + Chr(10);
	sReport := sReport + "Version: " + LimsString(nVersion) + Chr(13) + Chr(10);
	sReport := sReport + "Encrypted: " + IIf(nEncrypted != 0, "Yes", "No") + Chr(13) + Chr(10);
	sReport := sReport + "Compressed: " + IIf(nCompressed != 0, "Yes", "No") + Chr(13) + Chr(10);
	sReport := sReport + "Priority Level: " + LimsString(nPriority);

	UsrMes(sReport);
:ENDPROC;

/* Usage;
DoProc("DecodeProtocolFlags");
```

[`UsrMes`](UsrMes.md) displays:

```text
Packet Flags Decoded
Version: 3
Encrypted: Yes
Compressed: Yes
Priority Level: 6
```

## Related

- [`_OR`](_OR.md)
- [`_XOR`](_XOR.md)
- [`_NOT`](_NOT.md)
- [`LimsXOr`](LimsXOr.md)
- [`number`](../types/number.md)
