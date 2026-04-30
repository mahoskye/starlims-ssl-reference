---
title: "array"
summary: "Represents ordered, 1-based collections of SSL values, including nested arrays."
id: ssl.type.array
element_type: type
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# array

## What it is

Represents ordered, 1-based collections of SSL values, including nested arrays.

The `array` type stores values in positional order. Arrays are 1-based, so the first element is `aValues[1]`, not `aValues[0]`. Arrays can contain mixed value types, including strings, numbers, objects, [`NIL`](../literals/nil.md), and other arrays.

For display purposes, arrays render in brace syntax such as `{"A",2,NIL}`. [`Empty`](../functions/Empty.md) returns [`.T.`](../literals/true.md) only when the array has no top-level elements, and `Count` returns the number of top-level elements.

Use arrays when values need to stay in a defined order, when you need positional access such as `aRows[1]` or `aRows[nIndex][2]`, when a function returns tabular data or a list of items, or when you need to collect or reshape values while the script runs.

## Creating values

Arrays are commonly created with literal syntax such as `{1, 2, 3}` or nested forms such as `{{"A", 1}, {"B", 2}}`. You can also start with an empty array and append elements.

```ssl
aItems := {"S-1001", "S-1002", "S-1003"};
aEmpty := {};
aEmpty:Append("S-1004");
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
| `not-equals` | [`!=`](../operators/not-equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the operands do not reference the same array instance. |

## Members

| Member | Kind | Parameters | Returns | Description |
|---|---|---|---|---|
| `Append` | Method | `element` (`any`) | none | Adds an element to the end of the array. |
| `RemoveAt` | Method | `index` ([`number`](number.md)) | none | Removes the element at the specified 1-based position. |
| `InsertAt` | Method | `index` ([`number`](number.md)), `value` (`any`) | none | Inserts a value at the specified 1-based position. |
| `Index` | Method | `index` ([`number`](number.md)) | `any` | Returns the value at the specified 1-based position. In SSL code this is normally used through indexing syntax such as `aValues[2]`. |
| `IsEmpty` | Method | none | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the array has zero elements. |
| [`ToJson`](../functions/ToJson.md) | Method | none | [`string`](string.md) | Serializes the array as JSON array text. |
| `clone` | Method | none | `array` | Returns a deep copy of the array and its contained values. |
| `GetList` | Method | none | `any` | Returns the array contents in list form for APIs that expose list-style access. |
| `value` | Property | — | `any` | Gets or replaces the full array contents. |
| `Count` | Property | — | [`number`](number.md) | Returns the number of top-level elements. |

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
    - Check `IsEmpty()` or `Count` before indexing when the array may be empty.
    - Use `clone()` before changing a copied array when the original must remain unchanged.

!!! failure "Don't"
    - Assume arrays are 0-based. That causes off-by-one bugs because SSL arrays start at `1`.
    - Use fractional index values. Array indexing requires integers and raises an error for non-integer indexes.
    - Assume nested arrays are flattened automatically. Treat each nested array as its own ordered collection.

## Errors and edge cases

- `aValues[1]` is the first element. `aValues[0]` is invalid.
- Invalid positions for `RemoveAt`, `InsertAt`, or index access raise runtime errors.
- Arrays can hold mixed value types, so validate or normalize element types before doing arithmetic or exact comparisons.
- `clone()` deep-copies nested arrays and other contained values instead of reusing the same references.
- [`ToJson()`](../functions/ToJson.md) returns JSON array text and emits `null` for [`NIL`](../literals/nil.md) entries.

## Examples

### Collecting ordered sample IDs

Starts with an empty array, appends three sample IDs, then reads them back in order with a 1-based loop.

```ssl
:PROCEDURE CollectSampleIds;
    :DECLARE aSampleIds, nIndex;

    aSampleIds := {};

    aSampleIds:Append("S-1001");
    aSampleIds:Append("S-1002");
    aSampleIds:Append("S-1003");

    :FOR nIndex := 1 :TO ALen(aSampleIds);
        UsrMes("Queued sample " + aSampleIds[nIndex]);
    :NEXT;

    :RETURN aSampleIds;
:ENDPROC;

/* Usage;
DoProc("CollectSampleIds");
```

[`UsrMes`](../functions/UsrMes.md) displays once per element:

```text
Queued sample S-1001
Queued sample S-1002
Queued sample S-1003
```

### Updating nested result rows

Inserts a new row, updates two values in existing rows by index, then removes a row. After all edits, two rows remain.

```ssl
:PROCEDURE PrepareResultRows;
    :DECLARE aResults, aRow;

    aResults := {
        {"S-1001", "Pending", 7.1},
        {"S-1002", "Pending", 6.8}
    };

    aResults:InsertAt(2, {"S-1001A", "Pending", 7.0});

    aResults[1][2] := "Reviewed";
    aResults[3][3] := 6.9;

    aResults:RemoveAt(2);

    aRow := aResults[1];

    UsrMes("First row status: " + aRow[2]);
    UsrMes("Remaining rows: " + LimsString(aResults:Count));

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("PrepareResultRows");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
First row status: Reviewed
Remaining rows: 2
```

### Cloning an array before reshaping it

Creates an independent snapshot with `clone()`, appends a test to the snapshot's first row, and serializes the snapshot. The original array is unchanged.

```ssl
:PROCEDURE BuildAuditSnapshot;
    :DECLARE aOriginal, aSnapshot, sJson;

    aOriginal := {
        {"S-1001", {"pH", "Conductivity"}},
        {"S-1002", {"pH"}}
    };

    aSnapshot := aOriginal:clone();
    aSnapshot[1][2]:Append("Turbidity");

    sJson := aSnapshot:ToJson();

    UsrMes("Original tests: " + LimsString(aOriginal[1][2]:Count));
    UsrMes("Snapshot tests: " + LimsString(aSnapshot[1][2]:Count));
    UsrMes(sJson);

    :RETURN aSnapshot;
:ENDPROC;

/* Usage;
DoProc("BuildAuditSnapshot");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Original tests: 2
Snapshot tests: 3
[["S-1001",["pH","Conductivity","Turbidity"]],["S-1002",["pH"]]]
```

## Related elements

- [`AAdd`](../functions/AAdd.md)
- [`ALen`](../functions/ALen.md)
- [`AScan`](../functions/AScan.md)
- [`object`](object.md)
