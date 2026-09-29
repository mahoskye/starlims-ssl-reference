# Native Members on SSL Values

A colon member call on an SSL value, such as `sText:Trim()`, `dToday:AddDays(1)`, or `sFmt:Format(...)`, reaches a member of the value's underlying .NET type. These native members are separate from SSL's own functions and from the SSL-defined members listed on each [type page](../reference/types/index.md). They are not SSL elements, so they do not appear in the function or class reference.

Native members come in two shapes:

- **Methods** take parentheses, even with no arguments: `sText:ToUpper()`.
- **Properties** take no parentheses: `sText:Length`. Calling a property as a method fails. `sText:Length()` raises `Run-time error: Invalid method: Length`.

## Native members count from zero

SSL strings and arrays are 1-based. Native members use .NET's 0-based positions, the same rule that applies to .NET collections reached through colon access, such as `:GetProperty("Tables")[0]` on a dataset (see [`SQLExecute`](../reference/functions/SQLExecute.md#return-a-dataset-and-traverse-rows-with-0-based-net-indexing)).

| SSL function | Result | Native member | Result |
|---|---|---|---|
| [`At`](../reference/functions/At.md)`("W", "Hello World")` | `7` | `"Hello World":IndexOf("W")` | `6` |
| [`SubStr`](../reference/functions/SubStr.md)`(s, 1, 3)` | first three characters | `s:Substring(0, 3)` | first three characters |

`IndexOf` returns `-1` when the text is not found, where [`At`](../reference/functions/At.md) returns `0`. Convert positions explicitly when you mix the two styles.

```ssl
:PROCEDURE CompareIndexing;
	:DECLARE sText, nSslPos, nNativePos, sSslPart, sNativePart;

	sText := "Hello World";

	nSslPos := At("W", sText);
	nNativePos := sText:IndexOf("W");
	sSslPart := SubStr(sText, 1, 3);
	sNativePart := sText:Substring(0, 3);

	UsrMes("At: " + LimsString(nSslPos));
	UsrMes("IndexOf: " + LimsString(nNativePos));
	UsrMes("SubStr: " + sSslPart);
	UsrMes("Substring: " + sNativePart);

	:RETURN nNativePos;
:ENDPROC;

/* Usage;
DoProc("CompareIndexing");
```

[`UsrMes`](../reference/functions/UsrMes.md) logs:

```text
At: 7
IndexOf: 6
SubStr: Hel
Substring: Hel
```

## Verified members

The members below have been verified on STARLIMS v11. Other members may work, but verify them first (see [Verifying a member](#verifying-a-member)).

### Strings

| Member | Kind | Result |
|---|---|---|
| `Format(sPattern, aValues)` | Method | Fills `{0}`, `{1}`, ... placeholders in `sPattern`. See [Formatting text](#formatting-text-with-format). |
| `ToString()` | Method | The same text. |
| `ToUpper()` / `ToLower()` | Method | Upper-case or lower-case copy. |
| `Trim()` | Method | Copy with leading and trailing whitespace removed. |
| `PadLeft(nWidth)` | Method | Copy padded on the left with spaces to `nWidth` characters. |
| `Substring(nStart[, nLength])` | Method | Part of the string, from 0-based `nStart`. A range outside the string raises an error. |
| `IndexOf(sText[, nStart])` | Method | 0-based position of the first match, or `-1`. |
| `LastIndexOf(sText)` | Method | 0-based position of the last match, or `-1`. |
| `Replace(sOld, sNew)` | Method | Copy with every match replaced. Matching is **case-sensitive**, unlike SSL's [`Replace`](../reference/functions/Replace.md) function. |
| `Contains(sText)` / `StartsWith(sText)` / `EndsWith(sText)` | Method | Logical. |
| `Insert(nIndex, sText)` | Method | Copy with `sText` inserted at 0-based `nIndex`. |
| `Remove(nIndex[, nCount])` | Method | Copy with characters removed from 0-based `nIndex`. |
| `Equals(sText)` | Method | Logical. The comparison is case-sensitive. |
| `Length` | Property | Number of characters. |

### Numbers

| Member | Kind | Result |
|---|---|---|
| `ToString()` | Method | Text form: `42` gives `"42"`. |
| `ToString(sFormat)` | Method | Formatted text: `nNum:ToString("N2")` with `1234.5` gives `"1,234.50"`. |
| `GetType()` | Method | `System.Int32` for a whole number such as `42`, `System.Double` for `1.5`. |

### Logicals

| Member | Kind | Result |
|---|---|---|
| `ToString()` | Method | `"True"` or `"False"`, not `.T.` or `.F.`. Use [`LimsString`](../reference/functions/LimsString.md) for SSL's form. |

### Dates

Date members need a non-empty date. Any member access on an empty date raises an error, so guard with [`Empty`](../reference/functions/Empty.md) first.

| Member | Kind | Result |
|---|---|---|
| `ToString([sFormat])` | Method | Text form: for September 28, 2026, `ToString("yyyy-MM-dd")` gives `"2026-09-28"`. |
| `ToShortDateString()` | Method | Short date text, such as `9/29/2026`. The format follows the server's settings. |
| `AddDays(n)` / `AddHours(n)` / `AddMonths(n)` / `AddYears(n)` | Method | A new date. The argument must be a number. A string argument raises a conversion error. |
| `Subtract(dOther)` | Method | The difference between two dates. Read it with `:Days` or `:TotalDays`. |
| `Year`, `Month`, `Day`, `Hour`, `DayOfYear`, `DayOfWeek`, `Date`, `Ticks` | Property | Parts of the date. |

```ssl
:PROCEDURE ShowDueDate;
	:DECLARE dReceived, dDue, nDays, sDue;

	dReceived := DateFromNumbers(2026, 1, 31);
	dDue := dReceived:AddDays(30);
	nDays := dDue:Subtract(dReceived):Days;
	sDue := dDue:ToString("yyyy-MM-dd");

	UsrMes("Due: " + sDue);
	UsrMes("Month: " + LimsString(dDue:Month));
	UsrMes("Days: " + LimsString(nDays));

	:RETURN dDue;
:ENDPROC;

/* Usage;
DoProc("ShowDueDate");
```

[`UsrMes`](../reference/functions/UsrMes.md) logs:

```text
Due: 2026-03-02
Month: 3
Days: 30
```

### Arrays and objects

- An array exposes `Length` as a property: `aItems:Length` is the element count. `aItems:Count` raises `Invalid property: Count`. Use [`ALen`](../reference/functions/ALen.md) or `:Length`.
- Objects from [`CreateUdObject`](../reference/functions/CreateUdObject.md) have no native members. Only their own methods exist, and calling any other method raises `Method not found`. That includes `ToString`: `oRecord:ToString()` raises `Method not found: ToString`.

### Unknown members

- An unknown method, or a call whose arguments match no form of the member, raises `Run-time error: Invalid method: X`.
- An unknown property on a string, number, or array raises `Invalid property: X`.
- Not every form of a native member is reachable. `"a,b,c":Split(",")` raises `Invalid method: Split`, even though .NET strings have a `Split` method. Use [`BuildArray`](../reference/functions/BuildArray.md) to split delimited text.

## Formatting text with `Format`

`Format` takes a pattern as its first argument and fills its numbered placeholders from the values that follow. Pass the values as one array or as separate arguments. Both forms give the same result:

| Call | Result |
|---|---|
| `sFmt:Format("{0} of {1}", {3, 10})` | `3 of 10` |
| `sFmt:Format("{0} of {1}", 3, 10)` | `3 of 10` |
| `sFmt:Format("{0}{1}{2}{3}", {"a", "b", "c", "d"})` | `abcd` |
| `sFmt:Format("{0:N2}", {1234.5})` | `1,234.50` |

The text of the value you call `Format` on is not used. Only the pattern argument shapes the result. That is why the usual convention is an empty receiver named for its job:

```ssl
:PROCEDURE ShowProgress;
	:DECLARE sFmt, sProgress, sTotal;

	sFmt := "";
	sProgress := sFmt:Format("{0} of {1}", {3, 10});
	sTotal := sFmt:Format("{0:N2}", {1234.5});

	UsrMes(sProgress);
	UsrMes(sTotal);

	:RETURN sProgress;
:ENDPROC;

/* Usage;
DoProc("ShowProgress");
```

[`UsrMes`](../reference/functions/UsrMes.md) logs:

```text
3 of 10
1,234.50
```

The array form is the general one: you can build the array of values before the call.

## Verifying a member

- **Try an unfamiliar member in Designer before relying on it.** A member that exists on the .NET type can still fail, as `Split` does. Wrap the probe in [`:TRY`](../reference/keywords/TRY.md) and log the result or the error description.
- **Prefer SSL functions where they exist.** [`AllTrim`](../reference/functions/AllTrim.md), [`Upper`](../reference/functions/Upper.md), [`Lower`](../reference/functions/Lower.md), [`SubStr`](../reference/functions/SubStr.md), [`At`](../reference/functions/At.md), [`StrTran`](../reference/functions/StrTran.md) (case-sensitive) and [`Replace`](../reference/functions/Replace.md) (case-insensitive) are documented, 1-based, and follow SSL conventions. Reach for a native member when no SSL function covers the job, or when a convention calls for one, like `Format`.
- **Mind the differences.** Native results follow .NET conventions: 0-based positions, `-1` for not found, `"True"` instead of `.T.`, and case-sensitive matching.

!!! note "For validators and linters"
    A colon member call on a value, such as `sFmt:Format(...)` or `dDate:AddDays(1)`, is outside the SSL element list. Do not flag it as an unknown element because it is missing from the reference. Do not assume the full .NET member list is available either. Treat the members on this page as verified, and treat any other member as unverified until it is tested.
