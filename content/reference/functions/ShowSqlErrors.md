---
title: "ShowSqlErrors"
summary: "Sets the SQL error display flag, which decides whether a failing RunSQL raises, and returns the previous setting."
id: ssl.function.showsqlerrors
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# ShowSqlErrors

Sets the SQL error display flag, which decides whether a failing RunSQL raises, and returns the previous setting.

`ShowSqlErrors(bEnable)` updates the current SQL error display setting to the boolean value you pass and returns the value that was in effect before the change. This makes it useful for temporary changes around a specific block of database work where you want to restore the earlier behavior afterward.

The flag starts at [`.T.`](../literals/true.md). While it is [`.T.`](../literals/true.md), a failing [`RunSQL`](RunSQL.md) raises an error, even though [`IgnoreSqlErrors`](IgnoreSqlErrors.md) is also [`.T.`](../literals/true.md) by default. Set it to [`.F.`](../literals/false.md) and, as long as `IgnoreSqlErrors` is still [`.T.`](../literals/true.md), `RunSQL` returns [`.F.`](../literals/false.md) instead, with the error details in [`GetLastSQLError`](GetLastSQLError.md).

## When to use

- When a best-effort block should get [`.F.`](../literals/false.md) back from a failing [`RunSQL`](RunSQL.md) instead of an error.
- When you want to temporarily enable SQL error display while diagnosing a database problem.
- When you need to restore the earlier SQL error display setting after a small, controlled section of work.
- When you are coordinating SQL error display with [`IgnoreSqlErrors`](IgnoreSqlErrors.md) in maintenance or troubleshooting flows.

## Syntax

```ssl
ShowSqlErrors(bEnable)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `bEnable` | [boolean](../types/boolean.md) | yes | — | [`.T.`](../literals/true.md) (the starting value) enables SQL error display, so a failing [`RunSQL`](RunSQL.md) raises. [`.F.`](../literals/false.md) disables it, so a failing `RunSQL` returns [`.F.`](../literals/false.md) while [`IgnoreSqlErrors`](IgnoreSqlErrors.md) is [`.T.`](../literals/true.md). |

## Returns

**[boolean](../types/boolean.md)** — The previous SQL error display setting.

## Best practices

!!! success "Do"
    - Save the returned value and restore it after the temporary database work is complete.
    - Keep the setting change scoped to a small, clearly defined block of work.
    - Use [`:TRY`](../keywords/TRY.md) and [`:FINALLY`](../keywords/FINALLY.md) when later code could fail before the original setting is restored.

!!! failure "Don't"
    - Leave the flag changed longer than necessary when the intent was only temporary troubleshooting.
    - Assume the setting resets automatically after the next SQL statement.
    - Change this flag without considering [`IgnoreSqlErrors`](IgnoreSqlErrors.md) when you need predictable SQL error handling behavior.

## Caveats

- The setting remains in effect for later SQL work until you change it again.
- This setting works together with [`IgnoreSqlErrors`](IgnoreSqlErrors.md). With both at their starting value of [`.T.`](../literals/true.md), a failing [`RunSQL`](RunSQL.md) raises. It returns [`.F.`](../literals/false.md) only when this flag is [`.F.`](../literals/false.md) and `IgnoreSqlErrors` is [`.T.`](../literals/true.md). If `IgnoreSqlErrors` is [`.F.`](../literals/false.md), failures raise whatever this flag is set to.
- After a [`.F.`](../literals/false.md) return, the error is in [`GetLastSQLError`](GetLastSQLError.md). Nothing is stored for [`GetLastSSLError`](GetLastSSLError.md).
- The flag does not change how [`LSearch`](LSearch.md) fails: a failing `LSearch` raises even while this flag is [`.F.`](../literals/false.md), rather than returning its default value. Wrap `LSearch` in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md).

## Examples

### Make one statement raise whatever the caller set

A caller may have turned SQL error display off to get [`.F.`](../literals/false.md) returns. This procedure needs its update to raise on failure so its own [`:CATCH`](../keywords/CATCH.md) can report it, so it turns display on for the one statement and restores the caller's setting in [`:FINALLY`](../keywords/FINALLY.md).

```ssl
:PROCEDURE ReleaseSample;
	:PARAMETERS sSampleId;
	:DECLARE bPrevShow, oErr;

	bPrevShow := ShowSqlErrors(.T.);

	:TRY;
		RunSQL("UPDATE sample SET status = 'Released' WHERE sampleid = ?",, {sSampleId});
		UsrMes("Released " + sSampleId);
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("Release failed for " + sSampleId, oErr:Description);
	:FINALLY;
		ShowSqlErrors(bPrevShow);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ReleaseSample", {"S-2024-001"});
```

### Coordinate SQL error display with IgnoreSqlErrors

Turn SQL error display off, with suppression on, so a failing cleanup statement returns [`.F.`](../literals/false.md) instead of raising. Then restore both original settings in [`:FINALLY`](../keywords/FINALLY.md).

```ssl
:PROCEDURE RunQuietCleanup;
	:DECLARE bPrevIgnore, bPrevShow, dCutoff, sDeleteSql;

	dCutoff := Today() - 30;
	bPrevIgnore := IgnoreSqlErrors(.T.);
	bPrevShow := ShowSqlErrors(.F.);

	:TRY;
		sDeleteSql := "
		    DELETE FROM temp_results
		    WHERE logdate < ?
		";
		RunSQL(sDeleteSql,, {dCutoff});
	:FINALLY;
		ShowSqlErrors(bPrevShow);
		IgnoreSqlErrors(bPrevIgnore);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("RunQuietCleanup");
```

## Related

- [`IgnoreSqlErrors`](IgnoreSqlErrors.md)
- [`SetSqlTimeout`](SetSqlTimeout.md)
- [`boolean`](../types/boolean.md)
