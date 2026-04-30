---
title: "ArrayNew"
summary: "Create a new array with up to three dimensions."
id: ssl.function.arraynew
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ArrayNew

Create a new array with up to three dimensions.

ArrayNew creates a one-dimensional, two-dimensional, or three-dimensional
array. If `nDim1` is omitted, it defaults to `0`, so `ArrayNew()` returns an
empty array.

Each supplied dimension must be a non-negative integer. If you supply `nDim2`
or `nDim3`, the previous dimension must also be supplied and greater than zero.
The later dimension itself may be `0`, which creates empty nested arrays at
that level.

## When to use

- When you need a fixed-size one-dimensional array.
- When you need a two-dimensional or three-dimensional array structure.
- When you want an explicitly empty array by calling `ArrayNew()` or `ArrayNew(0)`.

## Syntax

```ssl
ArrayNew([nDim1], [nDim2], [nDim3])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nDim1` | [number](../types/number.md) | no | `0` | Size of the first dimension. |
| `nDim2` | [number](../types/number.md) | no | omitted | Size of the second dimension. If supplied, `nDim1` must also be supplied and greater than zero. |
| `nDim3` | [number](../types/number.md) | no | omitted | Size of the third dimension. If supplied, `nDim2` must also be supplied and greater than zero. |

## Returns

**[array](../types/array.md)** — New array with the requested dimensions. For two-dimensional and three-dimensional arrays, each element of the outer dimensions contains a nested array.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| Any supplied dimension is negative. | `If used, dimension parameters cannot be less than zero.` |
| Any supplied dimension is not a whole number. | `If used, dimension parameters must be integer values.` |
| A later dimension is supplied without a valid earlier dimension. | `If dimension N is used, then dimension N-1 must be greater than zero.` |

## Best practices

!!! success "Do"
    - Supply dimensions in order from the first dimension outward.
    - Use `ArrayNew(0)` when you want an explicitly empty array.
    - Choose ArrayNew when you need a fixed shape before populating values by index.

!!! failure "Don't"
    - Pass a second or third dimension unless the preceding dimension is present and greater than zero.
    - Pass fractional dimension values. ArrayNew requires integer sizes.
    - Assume omitted later dimensions become nested arrays automatically. Only the supplied dimensions are created.

## Examples

### Create a one-dimensional array

Creates a seven-element array pre-sized for a week's worth of daily sales totals, then confirms the size.

```ssl
:PROCEDURE InitDailySalesTotals;
	:DECLARE aDailySales;

	aDailySales := ArrayNew(7);

	UsrMes("Created array with " + LimsString(ALen(aDailySales)) + " elements");
:ENDPROC;

/* Usage;
DoProc("InitDailySalesTotals");
```

[`UsrMes`](UsrMes.md) displays:

```text
Created array with 7 elements
```

### Create a two-dimensional array

Creates a 4×3 array, assigns values into the first two rows, then reads back the outer dimension count and the inner count to confirm the shape.

```ssl
:PROCEDURE BuildProductSalesTable;
	:DECLARE aSalesData;

	aSalesData := ArrayNew(4, 3);

	aSalesData[1, 1] := 150;
	aSalesData[1, 2] := 175;
	aSalesData[1, 3] := 200;

	aSalesData[2, 1] := 80;
	aSalesData[2, 2] := 95;
	aSalesData[2, 3] := 110;

	UsrMes("Rows: " + LimsString(ALen(aSalesData)));
	UsrMes("Columns in row 1: " + LimsString(ALen(aSalesData[1])));
:ENDPROC;

/* Usage;
DoProc("BuildProductSalesTable");
```

[`UsrMes`](UsrMes.md) displays:

```text
Rows: 4
Columns in row 1: 3
```

## Related

- [`AAdd`](AAdd.md)
- [`ALen`](ALen.md)
- [`ArrayCalc`](ArrayCalc.md)
- [`DelArray`](DelArray.md)
- [`array`](../types/array.md)
