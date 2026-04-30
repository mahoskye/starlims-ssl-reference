---
title: "ArrayCalc"
summary: "Perform a selected array operation by passing an operation code."
id: ssl.function.arraycalc
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ArrayCalc

Perform a selected array operation by passing an operation code.

ArrayCalc is a multi-purpose array function. The behavior depends on the value of `sOperation`. Some operations return a calculated value, some return a new array, and some modify `aTarget` in place and return that same array. If `sOperation` is omitted, empty, or not recognized, ArrayCalc returns [`NIL`](../literals/nil.md).

ArrayCalc always requires a non-[`NIL`](../literals/nil.md) target array. When omitted, `nStart` defaults to `1` and `nCount` defaults to `ALen(aTarget)`. Those defaults only affect the operations that use range arguments.

## When to use

- When you need one of the built-in statistical operations such as `MIN`, `MAX`, `SUM`, `AVG`, or `DEV`.
- When you need copy, delete, fill, insert, merge, or sort behavior through one
  function.
- When existing code already uses ArrayCalc operation strings and you want to
  stay consistent with that style.

## Syntax

```ssl
ArrayCalc(aTarget, [sOperation], [vValue], [nStart], [nCount])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Target array for the selected operation. |
| `sOperation` | [string](../types/string.md) | no | empty string | Exact operation code such as `DUP`, `SUM`, `COPY`, or `SORT`. The documented codes are uppercase. Unrecognized values return [`NIL`](../literals/nil.md). |
| `vValue` | any | no | omitted | Extra value used by operations such as `MERGE`, `SORT`, `ADD`, `FILL`, and `INS`. For `SORT`, pass a numeric column index, an array of numeric column indexes, or a comparison code block. |
| `nStart` | [number](../types/number.md) | no | `1` | Starting index used by `COPY`, `DEL`, `FILL`, and `INS`. |
| `nCount` | [number](../types/number.md) | no | `ALen(aTarget)` | Element count used by `COPY`, `DEL`, and `FILL`. If the requested range extends past the end of `aTarget`, ArrayCalc shortens the count to the available elements. |

## Operations

### Statistical

| Operation | Effect | Return |
|-----------|--------|--------|
| `MIN` | Return the smallest element. | value |
| `MAX` | Return the largest element. | value |
| `SUM` | Sum all elements. | [number](../types/number.md) |
| `AVG1` | Average all elements. | [number](../types/number.md) |
| `AVG` | Average non-empty, nonzero elements. | [number](../types/number.md) |
| `DEV1` | Sample standard deviation across all elements. | [number](../types/number.md) |
| `DEV` | Sample standard deviation while skipping empty strings and zero values. | [number](../types/number.md) |

### Array manipulation

| Operation | Effect | Return |
|-----------|--------|--------|
| `DUP` | Clone the target array. | new array |
| `COPY` | Copy a slice into a new array. | new array |
| `ADD` | Append one value to `aTarget`. | `aTarget` |
| `INS` | Insert one value at `nStart`. | `aTarget` |
| `DEL` | Remove a slice from `aTarget`. | `aTarget` |
| `FILL` | Fill a range in `aTarget`. | `aTarget` |
| `MERGE` | Append another array to `aTarget`. | `aTarget` |
| `SORT` | Sort `aTarget` in place. Omit `vValue` for the default sort, pass a column index or array of column indexes for 2D arrays, or pass a comparison code block. | `aTarget` |

## Returns

**any** — Result depends on `sOperation`. Statistical operations return a numeric result, `DUP` and `COPY` return a new array, and the in-place operations return `aTarget`. ArrayCalc returns [`NIL`](../literals/nil.md) when `sOperation` is empty or not recognized.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |
| `MERGE` receives a non-array `vValue`. | `For MERGE operations, value parameter must be an array.` |
| `SORT` receives an empty array for `vValue`. | A runtime error is raised. |
| `SORT` receives an unsupported type for `vValue`. Accepted types are a numeric column index, an array of numeric column indexes, or a comparison code block. | A runtime error is raised. |
| A `SORT` comparison code block returns a non-numeric result. | `Array sort: the code block which compares two elements of the array, needs to return an integer value (less than zero if first element is smaller; zero if they are equal; and greater than zero if first element is greater).` |
| `nStart` is not a whole number for `COPY`. The same condition raises the same message for `DEL`, `FILL`, and `INS`. | `For COPY operations, starting index must be an integer value.` |
| `nStart < 1` for `COPY`. The same condition raises the same message for `DEL`, `FILL`, and `INS`. | `For COPY operations, starting index cannot be less than one.` |
| `nCount` is not a whole number for `COPY`. The same condition raises the same message for `DEL` and `FILL`. | `For COPY operations, count must be an integer value.` |
| `nCount < 0` for `COPY`. The same condition raises the same message for `DEL` and `FILL`. | `For COPY operations, count cannot be less than zero.` |
| `MIN` receives an empty array. The same pattern applies to `MAX`. | `For MIN operations, target array must have at least one element.` |
| A scanned element is [`NIL`](../literals/nil.md) during `MIN`. The same pattern applies to `MAX`. | `For MIN operations, array elements cannot be null.` |
| Scanned elements use mixed types during `MIN`. The same pattern applies to `MAX`. | `For MIN operations, array elements must have the same type.` |
| `AVG1` receives a target array with no elements. | `For AVG1 operations, target array must contain at least one element (cannot divide by zero).` |
| `AVG` receives a target array with no non-empty elements. | `For AVG operations, target array must contain at least one non-empty element (cannot divide by zero).` |
| `DEV1` receives a target array with fewer than two elements. | `For DEV1 operations, target array must contain at least two elements (cannot divide by zero).` |
| Fewer than two non-empty, nonzero elements remain after filtering for `DEV`. | `For DEV operations, target array must contain at least two elements (cannot divide by zero).` |

## Best practices

!!! success "Do"
    - Use the operation codes exactly as documented in uppercase.
    - Treat `DUP` and `COPY` as the non-mutating options when you need to keep
      the original array unchanged.
    - Use `SORT` with a numeric column index, an array of column indexes, or a
      comparison code block that returns a negative, zero, or positive number.
    - Use [`AScan`](AScan.md), [`AFill`](AFill.md), [`AAdd`](AAdd.md), or [`SortArray`](SortArray.md) directly when a dedicated function expresses the intent more clearly than ArrayCalc.

!!! failure "Don't"
    - Assume every operation mutates `aTarget`. `DUP`, `COPY`, and the
      statistical operations return separate results.
    - Assume `AVG` and `AVG1` mean the same thing. `AVG` skips empty
      strings and zero values, while `AVG1` uses the full array.
    - Assume `COPY` or `DEL` fails when `nCount` runs past the end of the
      array. ArrayCalc trims the count to the available range.
    - Rely on an invalid operation code raising an error. ArrayCalc
      returns [`NIL`](../literals/nil.md) for unrecognized operations.

## Examples

### Calculate a sum

Passes the `"SUM"` operation code to add all four numeric elements and returns the total.

```ssl
:PROCEDURE ShowBatchTotal;
    :DECLARE aReadings, nTotal;

    aReadings := {10, 20, 30, 40};
    nTotal := ArrayCalc(aReadings, "SUM");

    UsrMes("Total is " + LimsString(nTotal));
:ENDPROC;

/* Usage;
DoProc("ShowBatchTotal");
```

[`UsrMes`](UsrMes.md) displays:

```
Total is 100
```

### Merge one array into another

Uses the `"MERGE"` operation to append all elements from `aIncoming` to `aPending` in place, then reads the updated count.

```ssl
:PROCEDURE MergeQueues;
    :DECLARE aPending, aIncoming;

    aPending := {"A100", "A101"};
    aIncoming := {"A102", "A103"};

    ArrayCalc(aPending, "MERGE", aIncoming);

    UsrMes("Merged queue count: " + LimsString(ALen(aPending)));
:ENDPROC;

/* Usage;
DoProc("MergeQueues");
```

[`UsrMes`](UsrMes.md) displays:

```
Merged queue count: 4
```

### Sort numbers in descending order with a comparison code block

Passes a comparison block as `vValue` to `"SORT"` that returns a positive number when the right element is larger, placing the largest element first.

```ssl
:PROCEDURE SortDescendingScores;
    :DECLARE aScores;

    aScores := {12, 5, 27, 9};

    ArrayCalc(aScores, "SORT", {|nLeft, nRight| nRight - nLeft});

    UsrMes("Highest score: " + LimsString(aScores[1]));
:ENDPROC;

/* Usage;
DoProc("SortDescendingScores");
```

[`UsrMes`](UsrMes.md) displays:

```
Highest score: 27
```

## Related

- [`AAdd`](AAdd.md)
- [`AFill`](AFill.md)
- [`ALen`](ALen.md)
- [`AScan`](AScan.md)
- [`DelArray`](DelArray.md)
- [`SortArray`](SortArray.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
