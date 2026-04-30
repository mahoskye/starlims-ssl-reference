---
title: "ShowSqlErrors"
summary: "Sets the SQL error display flag and returns the previous setting."
id: ssl.function.showsqlerrors
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ShowSqlErrors

Sets the SQL error display flag and returns the previous setting.

`ShowSqlErrors(bEnable)` updates the current SQL error display setting to the boolean value you pass and returns the value that was in effect before the change. This makes it useful for temporary changes around a specific block of database work where you want to restore the earlier behavior afterward.

## When to use

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
| `bEnable` | [boolean](../types/boolean.md) | yes | — | [`.T.`](../literals/true.md) enables SQL error display. [`.F.`](../literals/false.md) disables it. |

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
- This setting can affect behavior together with [`IgnoreSqlErrors`](IgnoreSqlErrors.md). Fatal SQL errors can still be raised when SQL error suppression is enabled if SQL error display is also enabled.

## Examples

### Restore the previous setting after a lookup

Enable SQL error display for a single lookup, then restore the previous setting in [`:FINALLY`](../keywords/FINALLY.md) so callers are not affected.

```ssl
:PROCEDURE LookupSampleStatus;
	:PARAMETERS sSampleId;
	:DECLARE bPrevShow, sSql, sStatus;

	bPrevShow := ShowSqlErrors(.T.);

	:TRY;
		sSql :=
		"
		    SELECT status
		    FROM sample
		    WHERE sampleid = ?
		";
		sStatus := LSearch(sSql, "",, {sSampleId});

		:IF !Empty(sStatus);
			UsrMes("Sample status: " + sStatus);
		:ENDIF;
	:FINALLY;
		ShowSqlErrors(bPrevShow);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("LookupSampleStatus", {"S-2024-001"});
```

### Coordinate SQL error display with IgnoreSqlErrors

Suppress both SQL errors and SQL error display together for a cleanup operation, then restore both original settings in [`:FINALLY`](../keywords/FINALLY.md).

```ssl
:PROCEDURE RunQuietCleanup;
	:DECLARE bPrevIgnore, bPrevShow, dCutoff, sDeleteSql;

	dCutoff := Today() - 30;
	bPrevIgnore := IgnoreSqlErrors(.T.);
	bPrevShow := ShowSqlErrors(.F.);

	:TRY;
		sDeleteSql :=
		"
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
