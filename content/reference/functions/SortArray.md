---
title: "SortArray"
summary: "Sorts an array in place and returns the same array."
id: ssl.function.sortarray
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SortArray

Sorts an array in place and returns the same array.

`SortArray` reorders the elements in `aTarget` and returns the sorted array. Pass `1` or [`.T.`](../literals/true.md) in `vNumeric` to force numeric comparison. Pass a code block to compare two elements yourself. If `vNumeric` is omitted or contains any other value, the function uses the default sort behavior. `aTarget` cannot be [`NIL`](../literals/nil.md).

## When to use

- When you need to sort an existing array without creating a second array.
- When numeric values should be compared numerically instead of by default order.
- When you need custom ordering for arrays of rows or objects.
- When later logic should keep working with the same array reference after sorting.

## Syntax

```ssl
SortArray(aTarget, [vNumeric])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `aTarget` | [array](../types/array.md) | yes | — | Array to sort in place. |
| `vNumeric` | any | no | — | Sort mode selector. Pass `1` or [`.T.`](../literals/true.md) for numeric comparison, or pass a code block such as `{|vLeft, vRight| ...}` that returns a negative number, `0`, or a positive number. Other values use the default sort behavior. |

## Returns

**[array](../types/array.md)** — The same array after its elements have been reordered.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |
| The custom comparator does not return a numeric comparison result. | `Array sort: the code block which compares two elements of the array, needs to return an integer value (less than zero if first element is smaller; zero if they are equal; and greater than zero if first element is greater).` |

## Best practices

!!! success "Do"
    - Use [`.T.`](../literals/true.md) or `1` when you want numeric comparison explicitly.
    - Use a two-argument code block when sorting arrays of rows or objects.
    - Remember that the function mutates `aTarget` and returns that same array.

!!! failure "Don't"
    - Assume the code block receives one element. It compares two elements and must return a negative number, `0`, or a positive number.
    - Expect `SortArray` to leave the original array unchanged. Any other reference to the same array sees the new order.
    - Expect unsupported error behavior for other `vNumeric` values. Values other than [`.T.`](../literals/true.md), `1`, or a code block fall back to the default sort path.

## Caveats

- Only [`.T.`](../literals/true.md) and numeric `1` select the numeric comparer. Other truthy values fall back to the default sort.

## Examples

### Sort numbers in ascending order

Capture the original element order with [`BuildString`](BuildString.md), sort numerically, then show both the before and after strings.

```ssl
:PROCEDURE DemoNumericSort;
    :DECLARE aNumbers, sBefore, sAfter;

    aNumbers := {42, 15, 87, 3, 29};

    sBefore := BuildString(aNumbers, 1, ALen(aNumbers), ", ");
    SortArray(aNumbers, .T.);
    sAfter := BuildString(aNumbers, 1, ALen(aNumbers), ", ");

    UsrMes("Before: " + sBefore);
    /* Displays original order;

    UsrMes("After: " + sAfter);
    /* Displays sorted order;

    :RETURN aNumbers;
:ENDPROC;

/* Usage;
DoProc("DemoNumericSort");
```

### Sort objects with a custom comparator

Sort an array of UDO objects by a numeric property using a two-argument code block as the comparator.

```ssl
:PROCEDURE DemoPrioritySort;
    :DECLARE aSamples, fnByPriority, nIndex, oSample, sOutput;

    aSamples := {
        CreateUdObject({{"name", "Gamma"}, {"priority", 3}}),
        CreateUdObject({{"name", "Alpha"}, {"priority", 1}}),
        CreateUdObject({{"name", "Beta"}, {"priority", 2}})
    };

    fnByPriority := {|oLeft, oRight| oLeft:priority - oRight:priority};

    SortArray(aSamples, fnByPriority);
    sOutput := "";

    :FOR nIndex := 1 :TO ALen(aSamples);
        oSample := aSamples[nIndex];

        :IF nIndex > 1;
            sOutput += ", ";
        :ENDIF;

        sOutput += oSample:name + " (" + LimsString(oSample:priority) + ")";
    :NEXT;

    UsrMes("Sorted by priority: " + sOutput);

    :RETURN aSamples;
:ENDPROC;

/* Usage;
DoProc("DemoPrioritySort");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sorted by priority: Alpha (1), Beta (2), Gamma (3)
```

### Sort rows by multiple keys

Sort an array of rows by a primary key (priority) and a secondary key (sequence), wrapping the sort in [`:TRY`](../keywords/TRY.md) to handle a comparator that might return a non-numeric result.

```ssl
:PROCEDURE DemoMultiKeySort;
    :DECLARE aTasks, fnByPriorityThenSeq, nIndex, aTask, sOutput, oErr;

    aTasks := {
        {"S-100", 2, 15},
        {"S-101", 1, 30},
        {"S-102", 2, 10},
        {"S-103", 1, 20}
    };

    fnByPriorityThenSeq := {|aLeft, aRight| IIf(;
        aLeft[2] == aRight[2],;
        aLeft[3] - aRight[3],;
        aLeft[2] - aRight[2];
    )};

    :TRY;
        SortArray(aTasks, fnByPriorityThenSeq);
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes(oErr:Description);
        /* Displays on failure: SSL error description;
        :RETURN .F.;
    :ENDTRY;

    sOutput := "";

    :FOR nIndex := 1 :TO ALen(aTasks);
        aTask := aTasks[nIndex];

        :IF nIndex > 1;
            sOutput += " | ";
        :ENDIF;

        sOutput += aTask[1] + "-P" + LimsString(aTask[2])
            + "-S" + LimsString(aTask[3]);
    :NEXT;

    UsrMes("Sorted tasks: " + sOutput);

    :RETURN aTasks;
:ENDPROC;

/* Usage;
DoProc("DemoMultiKeySort");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sorted tasks: S-103-P1-S20 | S-101-P1-S30 | S-102-P2-S10 | S-100-P2-S15
```

## Related

- [`AAdd`](AAdd.md)
- [`ALen`](ALen.md)
- [`ArrayCalc`](ArrayCalc.md)
- [`DelArray`](DelArray.md)
- [`array`](../types/array.md)
