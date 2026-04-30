---
title: "Rand"
summary: "Generates a pseudo-random number between 0 (inclusive) and 1 (exclusive)."
id: ssl.function.rand
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Rand

Generates a pseudo-random number between 0 (inclusive) and 1 (exclusive).

`Rand()` returns the next value from a shared random number generator. `Rand(nSeed)` reseeds that shared generator by converting `nSeed` to an integer, then returns the first value from the reseeded sequence. Because the generator is shared, a seeded call also affects the values returned by later unseeded `Rand()` calls. Repeating the same `Rand(nSeed)` call produces the same first value each time.

## When to use

- When you need a pseudo-random fractional value for sampling, branching, or test data.
- When you want reproducible results by reseeding the generator with a known value.
- When you need a repeatable sequence and can seed once, then continue with
  `Rand()`.

## Syntax

```ssl
Rand([nSeed])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `nSeed` | [number](../types/number.md) | no | [`NIL`](../literals/nil.md) | Optional numeric seed. When supplied, the value is converted to an integer and used to reseed the shared generator before the function returns a value. |

## Returns

**[number](../types/number.md)** — A pseudo-random number greater than or equal to `0` and less than `1`.

## Best practices

!!! success "Do"
    - Seed once when you need a repeatable sequence, then continue with `Rand()` for subsequent values.
    - Reuse the same numeric seed when you need the same first generated value again.
    - Treat fractional seeds as integer seeds, because the function truncates them before use.

!!! failure "Don't"
    - Call `Rand(nSeed)` before every draw if you expect a progressing sequence. Repeating the same seed restarts the sequence each time.
    - Assume `Rand(nSeed)` is isolated from later calls. It reseeds the shared generator used by `Rand()`.
    - Pass strings, arrays, or objects as the seed.

## Examples

### Pick a random array element

Use `Rand()` to select one value from an array.

```ssl
:PROCEDURE PickRandomCode;
	:DECLARE aCodes, nIndex, nCount, sCode;

	aCodes := {"Alpha", "Bravo", "Charlie", "Delta"};
	nCount := ALen(aCodes);

    nIndex := Integer(Rand() * nCount) + 1;
    sCode := aCodes[nIndex];

    UsrMes("Selected code: " + sCode);
:ENDPROC;

/* Usage;
DoProc("PickRandomCode");
```

[`UsrMes`](UsrMes.md) displays:

```text
Selected code: Charlie
```

The selected element varies on every call.

### Repeat the same first seeded value

Use the same seed twice when you need the same first result again.

```ssl
:PROCEDURE CompareSeededValue;
	:DECLARE nSeed, nFirst, nSecond, bSame, sMessage;

    nSeed := 12345;

    nFirst := Rand(nSeed);
    nSecond := Rand(nSeed);
    bSame := nFirst == nSecond;

    sMessage := "First: " + LimsString(nFirst);
    sMessage := sMessage + ", Second: " + LimsString(nSecond);
    sMessage := sMessage + ", Same value: " + LimsString(bSame);

    UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("CompareSeededValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
First: <seeded_value>, Second: <seeded_value>, Same value: T
```

Both values are identical and `Same value` is `T` regardless of the runtime's RNG implementation. The exact numbers depend on the platform.

### Seed once, then consume a repeatable sequence

Seed the generator once and use later `Rand()` calls to advance through that seeded sequence.

```ssl
:PROCEDURE BuildRepeatableSequence;
	:DECLARE nSeed, aValues, nIndex, sMessage;

    nSeed := 250;
    aValues := {};

    AAdd(aValues, Rand(nSeed));

    :FOR nIndex := 1 :TO 2;
        AAdd(aValues, Rand());
    :NEXT;

    sMessage := "Sequence: " + LimsString(aValues[1]);
    sMessage := sMessage + ", " + LimsString(aValues[2]);
    sMessage := sMessage + ", " + LimsString(aValues[3]);

    UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("BuildRepeatableSequence");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sequence: <first_value>, <second_value>, <third_value>
```

The same seed always produces the same sequence. The exact numbers depend on the platform's RNG implementation.

## Related

- [`Integer`](Integer.md)
- [`number`](../types/number.md)
