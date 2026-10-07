---
title: "array"
summary: "Represents ordered, 1-based collections of SSL values, including nested arrays."
id: ssl.type.array
element_type: type
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# array

## What it is

Represents ordered, 1-based collections of SSL values, including nested arrays.

The `array` type stores values in positional order. Arrays are 1-based, so the first element is `aValues[1]`, not `aValues[0]`. Arrays can contain mixed value types, including strings, numbers, objects, [`NIL`](../literals/nil.md), and other arrays.

For display purposes, arrays render in brace syntax such as `{"A",2,NIL}`. [`Empty`](../functions/Empty.md) returns [`.T.`](../literals/true.md) only when the array has no top-level elements, and [`ALen`](../functions/ALen.md) returns the number of top-level elements.

Use arrays when values need to stay in a defined order, when you need positional access such as `aRows[1]` or `aRows[nIndex][2]`, when a function returns tabular data or a list of items, or when you need to collect or reshape values while the script runs.

## Creating values

Arrays are commonly created with literal syntax such as `{1, 2, 3}` or nested forms such as `{{"A", 1}, {"B", 2}}`. You can also start with an empty array and append elements with [`AAdd`](../functions/AAdd.md).

```ssl
aItems := {"S-1001", "S-1002", "S-1003"};
aEmpty := {};
AAdd(aEmpty, "S-1004");
```

| Attribute | Value |
|---|---|
| Runtime type | `ARRAY` |
| Literal syntax | `{elem1, elem2}` |
| Nested literal syntax | `{{row1}, {row2}}` |

## Operators

Arrays support identity comparison operators. Arithmetic and relational operators are not supported.

| Operator | Symbol | Returns | Behavior |
|---|---|---|---|
| `strict-equals` | [`==`](../operators/strict-equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) only when both operands reference the same array instance. |
| `equals` | [`=`](../operators/equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) only when both operands reference the same array instance. |
| `not-equals` | [`!=`](../operators/not-equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the operands do not reference the same array instance. |

## Members

Arrays have no SSL-defined `:` members. Calls such as `aValues:Append(x)`, `aValues:InsertAt(n, x)`, `aValues:RemoveAt(n)`, `aValues:IsEmpty()`, `aValues:ToJson()` and `aValues:clone()`, and properties such as `aValues:Count` and `aValues:value`, raise `Run-time error: Invalid method: …` or `Invalid property: …`. Work with arrays through the array functions instead:

| Task | Use |
|---|---|
| Count elements | [`ALen`](../functions/ALen.md) |
| Append an element | [`AAdd`](../functions/AAdd.md) |
| Find an element | [`AScan`](../functions/AScan.md) |
| Sort | [`SortArray`](../functions/SortArray.md) |
| Test for no elements | [`Empty`](../functions/Empty.md) |
| Serialize to JSON | [`ToJson`](../functions/ToJson.md) |
| Copy | `aValues:Clone()`, a .NET member; see below |

## Calling .NET `Array` methods

An `array` value also exposes the public members of a .NET `System.Object[]` array through the `:` method-call syntax, such as `aValues:Length` and `aValues:Clone()`.

In practice, this passthrough is rarely the best path for SSL arrays, for two reasons:

- The most useful array operations in .NET — `Sort`, `Reverse`, `IndexOf`, `BinarySearch` — are static methods on `System.Array` that take the array as an explicit parameter rather than a receiver. They are reached through the static form of [`LimsNETConnect`](../functions/LimsNETConnect.md), such as `LimsNETConnect(, "System.Array",, .T.)` (see [`netobject`](netobject.md)), rather than through the implicit `:` passthrough on an array value.
- The instance-level members reachable through the `:` syntax are limited (`Length`, `Rank`, `GetType()`, `Clone()`). `Length` matches [`ALen`](../functions/ALen.md), and `Clone()` returns a new array with the same top-level elements.

Prefer SSL-native array functions ([`ALen`](../functions/ALen.md), [`AScan`](../functions/AScan.md), [`SortArray`](../functions/SortArray.md), [`AAdd`](../functions/AAdd.md)) for portability and readability. Reach for the .NET passthrough only when you need a specific `System.Array` operation that the SSL library does not cover.

This passthrough is an interop convenience, not part of the SSL language surface. The members are not declared in SSL and do not appear in editor autocomplete. Their names are case-sensitive: `aValues:Clone()` works, but `aValues:clone()` raises `Invalid method: clone`, and `aValues:length` raises `Invalid property: length` (see [Member names and case](../../guides/native-members.md#member-names-and-case)).

### Example: reading the underlying `Array.Length` property

Reads the .NET `Length` property with `:`. The result matches [`ALen`](../functions/ALen.md), so this mainly shows that native members work on `array` values; `ALen` is the usual choice.

```ssl
:PROCEDURE ShowArrayLength;
    :DECLARE aSamples, nLength;

    aSamples := {"S-1001", "S-1002", "S-1003"};
    nLength := aSamples:Length;

    UsrMes("Length: " + LimsString(nLength));

    :RETURN nLength;
:ENDPROC;

/* Usage;
DoProc("ShowArrayLength");
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
Length: 3
```

## Indexing

| Attribute | Value |
|---|---|
| Supported | `true` |
| Base | `1` |
| Read behavior | Returns the value at the specified 1-based index |
| Assignment | Supported, for example `aValues[2] := "Released";` |

Index expressions must evaluate to an integer. If the index expression is not an integer, SSL raises an error with the message `Argument for index must be an integer: <value>`.

## Notes for daily SSL work

!!! success "Do"
    - Use 1-based loops such as `:FOR nIndex := 1 :TO ALen(aValues);` when iterating arrays.
    - Check [`Empty`](../functions/Empty.md) or [`ALen`](../functions/ALen.md) before indexing when the array may be empty.
    - Copy with `aValues:Clone()` (capital `C`) before changing an array when the original must remain unchanged.

!!! failure "Don't"
    - Assume arrays are 0-based. That causes off-by-one bugs because SSL arrays start at `1`.
    - Use fractional index values. Array indexing requires integers and raises an error for non-integer indexes.
    - Assume nested arrays are flattened automatically. Treat each nested array as its own ordered collection.

## Errors and edge cases

- `aValues[1]` is the first element. `aValues[0]` is invalid.
- Index access outside the array raises a runtime error.
- Arrays can hold mixed value types, so validate or normalize element types before doing arithmetic or exact comparisons.
- `Clone()` copies only the top level. Only a flat copy has been checked; when an array holds nested arrays, don't assume the copy's nested arrays are independent of the original's.
- [`ToJson`](../functions/ToJson.md)`(aValues)` returns JSON array text and emits `null` for [`NIL`](../literals/nil.md) entries.

## Examples

### Collecting ordered sample IDs

Starts with an empty array, appends three sample IDs with [`AAdd`](../functions/AAdd.md), then reads them back in order with a 1-based loop.

```ssl
:PROCEDURE CollectSampleIds;
    :DECLARE aSampleIds, nIndex;

    aSampleIds := {};

    AAdd(aSampleIds, "S-1001");
    AAdd(aSampleIds, "S-1002");
    AAdd(aSampleIds, "S-1003");

    :FOR nIndex := 1 :TO ALen(aSampleIds);
        UsrMes("Queued sample " + aSampleIds[nIndex]);
    :NEXT;

    :RETURN aSampleIds;
:ENDPROC;

/* Usage;
DoProc("CollectSampleIds");
```

[`UsrMes`](../functions/UsrMes.md) logs once per element:

```text
Queued sample S-1001
Queued sample S-1002
Queued sample S-1003
```

### Updating nested result rows

Appends a new row with [`AAdd`](../functions/AAdd.md), then updates values in existing rows by index. After the edits, three rows remain.

```ssl
:PROCEDURE PrepareResultRows;
    :DECLARE aResults, aRow;

    aResults := {
        {"S-1001", "Pending", 7.1},
        {"S-1002", "Pending", 6.8}
    };

    AAdd(aResults, {"S-1003", "Pending", 7.0});

    aResults[1][2] := "Reviewed";
    aResults[3][3] := 6.9;

    aRow := aResults[1];

    UsrMes("First row status: " + aRow[2]);
    UsrMes("Remaining rows: " + LimsString(ALen(aResults)));

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("PrepareResultRows");
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
First row status: Reviewed
Remaining rows: 3
```

### Copying an array before changing it

Copies a flat array with the .NET `Clone()` member, changes the copy, and serializes both with [`ToJson`](../functions/ToJson.md). The original is unchanged. The member name is case-sensitive: `Clone()`, not `clone()`.

```ssl
:PROCEDURE BuildAuditSnapshot;
    :DECLARE aOriginal, aSnapshot;

    aOriginal := {"Logged", "Logged", "Released"};

    aSnapshot := aOriginal:Clone();
    aSnapshot[1] := "Reviewed";

    UsrMes("Original: " + ToJson(aOriginal));
    UsrMes("Snapshot: " + ToJson(aSnapshot));

    :RETURN aSnapshot;
:ENDPROC;

/* Usage;
DoProc("BuildAuditSnapshot");
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
Original: ["Logged","Logged","Released"]
Snapshot: ["Reviewed","Logged","Released"]
```

## Caveats

- Arrays have no `Count` property and no SSL-defined methods: `aValues:Count` raises `Run-time error: Invalid property: Count`, and `aValues:Append(x)` raises `Invalid method: Append`. Use [`ALen`](../functions/ALen.md) and the other array functions listed under [Members](#members).
- A `:` member call on an array reaches a .NET array member (e.g. `aValues:Length`). A member that doesn't exist, or doesn't accept the arguments given, raises an error such as `Run-time error: Invalid method: Split`. Check a member before relying on it; see [Native Members](../../guides/native-members.md).

## Related elements

- [`AAdd`](../functions/AAdd.md)
- [`ALen`](../functions/ALen.md)
- [`AScan`](../functions/AScan.md)
- [`object`](object.md)
