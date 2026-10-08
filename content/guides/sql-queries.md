# Working with SQL in SSL

SSL provides several functions for executing SQL against the LIMS database. Choosing the right one depends on what you need back — a success flag, a single value, a result array, or an XML dataset.

## Choosing the right function

| Function | Use when you need | Returns |
|----------|-------------------|---------|
| [`RunSQL`](../reference/functions/RunSQL.md) | Execute INSERT, UPDATE, DELETE, or DDL | boolean ([`.T.`](../reference/literals/true.md) on success) |
| [`LSearch`](../reference/functions/LSearch.md) | Retrieve a single value from one row | The value, or a default if no rows |
| [`LSelect`](../reference/functions/LSelect.md) / [`LSelect1`](../reference/functions/LSelect1.md) | Retrieve multiple rows as an array | 2D array (rows × columns) |
| [`GetDataSet`](../reference/functions/GetDataSet.md) | XML dataset from a SELECT | XML string |
| [`SQLExecute`](../reference/functions/SQLExecute.md) | Named-parameter queries; configurable return type | Array, XML string, or dataset object |

```ssl
:DECLARE sName, aResults, sXml, sBatch, aRows;

/* Single value;
sName := LSearch("SELECT name FROM users WHERE user_id = ?", "",, {"USR001"});

/* Multiple rows;
aResults := LSelect1("SELECT sample_id, status FROM samples WHERE batch = ?",, {"B-100"});

/* Execute a statement;
RunSQL("UPDATE samples SET status = 'C' WHERE sample_id = ?",, {"S-001"});

/* XML dataset;
sXml := GetDataSet("SELECT sample_id FROM samples WHERE batch = ?", {"B-100"});

/* Named-parameter query;
sBatch := "B-100";
aRows := SQLExecute("SELECT sample_id FROM samples WHERE batch = ?sBatch?");
```

Two idioms in these examples are worth decoding up front:

- **Adjacent commas** (`,,`) skip an optional middle parameter — here the connection name, so the call uses the default connection. `LSearch("...", "",, {...})` passes the SQL, then a default value, skips the connection name, then passes the bound values. [`GetDataSet`](../reference/functions/GetDataSet.md) has no connection parameter, so its values array comes second with nothing skipped.
- **`?sBatch?`** is [`SQLExecute`](../reference/functions/SQLExecute.md)'s named-parameter form: the engine substitutes the value of the variable `sBatch` from the calling scope. The other functions use positional `?` placeholders with a values array instead. Both are covered in detail [below](#sqlexecute-flexible-execution).

## Connection names

Most SQL functions accept an optional connection name parameter that identifies which configured database to run the query against. When omitted, the function uses the current default connection.

The connection name is the key registered in the system's database configuration. You can discover available names at runtime with [`GetConnectionStrings`](../reference/functions/GetConnectionStrings.md), which returns a 2D array where column 1 is the connection name, column 2 is the provider settings string (such as `SQL;NATIVESQL;...;USEUTC`), and column 3 is the full connection string.

```ssl
:DECLARE aConns, nIndex, aRows, sDefault;

/* See what connections are available;
aConns := GetConnectionStrings();
:FOR nIndex := 1 :TO ALen(aConns);
    UsrMes(aConns[nIndex, 1] + " (" + aConns[nIndex, 2] + ")");
:NEXT;

/* Query using the default connection (omit the parameter);
aRows := LSelect1("SELECT sample_id FROM sample WHERE status = ?",, {"A"});

/* Query against a specific named connection;
aRows := LSelect1("SELECT sample_id FROM sample WHERE status = ?", "ARCHIVE", {"A"});

/* Check what the current default is;
sDefault := GetDefaultConnection();
```

The same connection name parameter appears in [`RunSQL`](../reference/functions/RunSQL.md), [`LSelect1`](../reference/functions/LSelect1.md), [`SQLExecute`](../reference/functions/SQLExecute.md), and related functions as the second argument after the SQL string. Watch for three exceptions: [`LSearch`](../reference/functions/LSearch.md) takes the connection name as its **third** argument (after the default value), [`LSelect`](../reference/functions/LSelect.md) takes a field list second and the connection name **third**, and [`GetDataSet`](../reference/functions/GetDataSet.md) has no connection parameter at all — use [`GetDataSetEx`](../reference/functions/GetDataSetEx.md) (connection name second) to query a named connection.

## Parameterized queries

All SQL functions support parameterized queries using the `?` placeholder. This is the **recommended approach** for any query that includes user-supplied or variable data.

### How it works

Place a `?` in your SQL wherever a value should go, then pass the values as an array as the last argument. The engine replaces each `?` with a database-appropriate parameter (e.g., `@param1` for SQL Server, `:param1` for Oracle) and binds the values safely.

```ssl
:DECLARE sSQL, aResults;

/* Parameterized — safe;
sSQL := "SELECT * FROM samples WHERE batch_id = ? AND status = ?";
aResults := LSelect1(sSQL,, {"B-100", "A"});
```

The values are **bound as parameters**, not interpolated into the SQL string. This means:

- No SQL injection risk from the values
- Proper handling of special characters (quotes, etc.)
- Correct type binding for dates, numbers, and nulls
- Better query plan caching on the database server

### Parameter count must match

The number of `?` placeholders must match the number of elements in the values array. Too few values raises an error, and the message depends on the function: [`RunSQL`](../reference/functions/RunSQL.md) raises `ExecuteNonQuery exception Not enough values provided for parameters.`, while [`LSelect`](../reference/functions/LSelect.md), [`LSelect1`](../reference/functions/LSelect1.md), [`LSearch`](../reference/functions/LSearch.md) and [`GetDataSet`](../reference/functions/GetDataSet.md) raise `Parameters count mismatch`. Each `?` is positional — there are no named parameters, so if you need the same value in multiple places, you must pass it multiple times.

```ssl
:DECLARE sSQL;

/* Correct: 2 placeholders, 2 values;
RunSQL("UPDATE t SET a = ? WHERE b = ?",, {sNewValue, sKeyValue});

/* Wrong: 2 placeholders, 1 value — throws error;
RunSQL("UPDATE t SET a = ? WHERE b = ?",, {sNewValue});

/* Same value used twice — must appear twice in the array;
sSQL := "INSERT INTO audit_log (changed_by, approved_by, sample_id)";
sSQL := sSQL + " VALUES (?, ?, ?)";
RunSQL(sSQL,, {sCurrentUser, sCurrentUser, sSampleId});
```

### Placeholders inside string literals are ignored

The engine skips `?` characters that appear inside single-quoted string literals in the SQL. This means you can safely include literal question marks in string values:

```ssl
/* The ? inside 'What?' is not treated as a placeholder;
RunSQL("INSERT INTO log (msg, user_id) VALUES ('What?', ?)",, {sUserId});
```

### Building IN clauses

SQL `IN (...)` clauses need special handling because you can't use a single `?` for a list of values. SSL provides two helpers:

#### PrepareArrayForIn

Sanitizes an array for use with a parameterized `IN` clause. It modifies the array you pass in place, so there is nothing to assign: a literal empty-string element is replaced with a string sentinel that matches nothing (empty strings from the database or built at run time are not; see [`PrepareArrayForIn`](../reference/functions/PrepareArrayForIn.md#caveats)), and an empty array gains one sentinel of the requested type:

```ssl
:DECLARE aSampleIds, aOrderIds;

/* A populated array with a literal blank entry;
aSampleIds := {"S-001", "", "S-003"};
PrepareArrayForIn(aSampleIds, "string");
UsrMes(aSampleIds[2]);

/* An empty array;
aOrderIds := {};
PrepareArrayForIn(aOrderIds, "numeric");
UsrMes(LimsString(ALen(aOrderIds)) + " element: " + LimsString(aOrderIds[1]));
```

`UsrMes` logs:

```text
C7082BA7C83D38CAE98421BE494753931F8B52A8
1 element: -2147483648
```

The sentinel is what keeps an `IN (...)` query valid on MS SQL Server. Without it, an empty array would give you no placeholders and the statement would end in `IN ()`, which is a syntax error. After `PrepareArrayForIn`, the array always has at least one element, so the placeholder list has at least one `?`. The sentinel value matches no real row, so the query runs and returns no rows. This applies when you build the `?` list yourself: [`SQLExecute`](../reference/functions/SQLExecute.md)'s `?name?` substitution accepts an empty array and runs the query, which then returns no rows. Replacing a literal `""` works the same way: that entry can no longer match rows whose column holds an empty string. Blanks that came from the database or were built at run time are not replaced, so remove them yourself when they must not match.

Build the placeholder list from the prepared array:

```ssl
:DECLARE aSampleIds, sTemp, sPlaceholders, sSQL, aResults;

/* The list to match, which may arrive empty;
aSampleIds := {};
PrepareArrayForIn(aSampleIds, "string");

/* One ? per element, so at least one;
sTemp         := Replicate("?,", ALen(aSampleIds));
sPlaceholders := Left(sTemp, Len(sTemp) - 1);

/* Use with parameterized query;
sSQL := "SELECT sample_id, status FROM samples";
sSQL := sSQL + " WHERE sample_id IN (" + sPlaceholders + ")";

/* Runs as WHERE sample_id IN (?) and returns no rows;
aResults := LSelect1(sSQL,, aSampleIds);
```

[`PrepareArrayForIn`](../reference/functions/PrepareArrayForIn.md) returns the array (modified in place). The second parameter controls the sentinel type for empty arrays:

| Type | Use for |
|------|---------|
| `"string"` | Text columns |
| `"numeric"` | Numeric columns |
| `"date"` | Date columns |

#### BuildStringForIn

Builds a complete `('val1','val2','val3')` string for direct inclusion in SQL. Escapes single quotes within the values automatically.

```ssl
:DECLARE aSampleIds, sInClause, sSQL, aResults;

/* Build the array of values to match;
aSampleIds := {"S-001", "S-002", "S-003"};

/* Generate the IN clause string;
sInClause := BuildStringForIn(aSampleIds);
/* Result: ('S-001','S-002','S-003');

/* Use it in the query;
sSQL := "SELECT sample_id, status FROM samples";
sSQL := sSQL + " WHERE sample_id IN " + sInClause;

aResults := LSelect1(sSQL);
```

!!! note "Empty array behavior"
    [`PrepareArrayForIn`](../reference/functions/PrepareArrayForIn.md) adds one sentinel of the requested type to an empty array. [`BuildStringForIn`](../reference/functions/BuildStringForIn.md) returns a fixed quoted string sentinel for an empty or [`NIL`](../reference/literals/nil.md) array. Either way the `IN` clause stays syntactically valid and matches no real rows, so the query returns zero rows instead of raising an error.

## String concatenation (not recommended)

The alternative to parameterized queries is building the SQL string with concatenation:

```ssl
:DECLARE sSQL, aResults;

/* String concatenation — avoid when possible;
sSQL := "SELECT * FROM samples WHERE batch_id = '" + sBatchId + "'";
sSQL := sSQL + " AND status = '" + sStatus + "'";
aResults := LSelect1(sSQL);
```

[`LimsString`](../reference/functions/LimsString.md) converts a value to text but does not quote it or escape embedded quotes, so string values must be quoted (and their single quotes doubled) by hand, as above. Concatenation is **not a substitute for parameterized queries**:

- No protection against SQL injection if values contain crafted content
- Date and number formatting depends on server locale settings
- More error-prone to construct correctly

!!! warning "Prefer parameterized queries"
    Use `?` placeholders with an array of values for any query that includes variable data. Reserve string concatenation for fully static SQL or cases where the table/column name itself is dynamic (which cannot be parameterized).

## Function reference

### LSearch — single value

Returns the first column of the first row, or a default value if no rows match:

```ssl
:DECLARE sStatus, nCount;

/* Get a single value with a fallback default;
sStatus := LSearch("SELECT status FROM samples WHERE sample_id = ?", "UNKNOWN",, {"S-001"});

/* Numeric result;
nCount := LSearch("SELECT COUNT(*) FROM samples WHERE batch_id = ?", 0,, {"B-100"});
```

The second parameter is the default returned when the query finds no rows. Without one, a miss returns an empty string `""`, not NIL.

### LSelect1 — result array

Returns a 2D array where rows are the first dimension and columns are the second:

```ssl
:DECLARE aResults, nIndex, sSampleId, sStatus, sPriority;

aResults := LSelect1("SELECT sample_id, status, priority FROM samples WHERE batch = ?",, {"B-100"});

/* Access: aResults[row, column];
:FOR nIndex := 1 :TO ALen(aResults);
    sSampleId := aResults[nIndex, 1];     /* first column;
    sStatus   := aResults[nIndex, 2];     /* second column;
    sPriority := aResults[nIndex, 3];     /* third column;
    UsrMes(sSampleId + " — " + sStatus);
:NEXT;
```

If the query returns no rows, [`LSelect1`](../reference/functions/LSelect1.md) returns an empty array. Always check with [`ALen`](../reference/functions/ALen.md) before iterating.

### RunSQL — execute statements

Returns [`.T.`](../reference/literals/true.md) on success. Error behavior depends on the [`IgnoreSqlErrors`](../reference/functions/IgnoreSqlErrors.md) and [`ShowSqlErrors`](../reference/functions/ShowSqlErrors.md) flags (see [SQL & Transactions guide](sql-transactions.md#sql-error-handling)). Under their starting values a failing statement raises instead of returning [`.F.`](../reference/literals/false.md), so handle failures with [`:TRY`](../reference/keywords/TRY.md) / [`:CATCH`](../reference/keywords/CATCH.md):

```ssl
:DECLARE oErr;

:TRY;
    RunSQL("INSERT INTO audit_log (action, ts) VALUES (?, ?)",, {"LOGIN", DToS(Now())});
:CATCH;
    oErr := GetLastSSLError();
    ErrorMes("Audit log insert failed: " + oErr:Description);
:ENDTRY;
```

### GetDataSet — XML output

Returns a SELECT result as an XML string. Useful when passing data to external systems or storing structured output:

```ssl
:DECLARE sXml;

sXml := GetDataSet("SELECT sample_id, status FROM samples WHERE batch = ?", {"B-100"});
```

## SQLExecute — flexible execution

[`SQLExecute`](../reference/functions/SQLExecute.md) differs from the other SQL functions in two ways: it uses **named `?varName?` placeholders** instead of a positional values array, and its return type is controlled by an explicit parameter.

### Named parameters

Instead of passing a separate values array, you embed variable names directly in the SQL using `?varName?` syntax. The engine substitutes the current value of each named variable from the calling scope at execution time:

```ssl
:DECLARE sBatch, sStatus, aRows;

sBatch := "B-100";
sStatus := "A";

aRows := SQLExecute("SELECT sample_id FROM samples WHERE batch = ?sBatch? AND status = ?sStatus?");
```

No values array is needed — the variable names in the SQL string are resolved automatically.

!!! warning "Don't mix syntaxes"
    `?varName?` only works with [`SQLExecute`](../reference/functions/SQLExecute.md). The other functions ([`RunSQL`](../reference/functions/RunSQL.md), [`LSearch`](../reference/functions/LSearch.md), [`LSelect1`](../reference/functions/LSelect1.md), [`GetDataSet`](../reference/functions/GetDataSet.md)) use positional `?` with a values array. Using `?varName?` with those functions will not substitute values.

### Array expansion for IN clauses

When a `?varName?` placeholder refers to a local array variable, [`SQLExecute`](../reference/functions/SQLExecute.md) automatically expands it into a matching set of positional placeholders. A three-element array becomes `?,?,?` inline:

```ssl
:DECLARE aStatusCodes, aRows;

aStatusCodes := {"A", "P", "C"};

aRows := SQLExecute("
    SELECT sample_id, status
    FROM samples
    WHERE status IN (?aStatusCodes?)
");
```

This is the cleanest way to build a dynamic `IN` clause with [`SQLExecute`](../reference/functions/SQLExecute.md) — no placeholder string building required.

!!! warning "Array must be a local variable"
    The array must be declared and assigned as a local variable in the calling scope. Passing a UDObject property directly (e.g. `?oFilter:StatusCodes?`) causes a runtime error. Copy the property to a local variable first:

    ```ssl
    :DECLARE aStatusCodes, aRows;

    aStatusCodes := oFilter:StatusCodes;
    aRows := SQLExecute("SELECT * FROM samples WHERE status IN (?aStatusCodes?)");
    ```

### Return type

The sixth parameter controls what [`SQLExecute`](../reference/functions/SQLExecute.md) returns for `SELECT` statements:

| Value | Returns |
|-------|---------|
| omitted or [`.F.`](../reference/literals/false.md) | array (rows × columns) |
| [`.T.`](../reference/literals/true.md) or `"xml"` | XML string |
| `"dataset"` | [`netobject`](../reference/types/netobject.md) wrapping a .NET `DataSet` |

```ssl
:DECLARE aRows, sXml, oDs, bOk;

/* Default — returns array;
aRows := SQLExecute("SELECT sample_id, status FROM samples WHERE batch = ?sBatch?");

/* XML output;
sXml := SQLExecute("SELECT sample_id, status FROM samples WHERE batch = ?sBatch?",,,,, .T.);

/* Dataset object — returns a netobject wrapping a .NET DataSet;
oDs := SQLExecute("SELECT sample_id, status FROM samples WHERE batch = ?sBatch?",,,,, "dataset");

/* Non-SELECT — returns boolean success;
bOk := SQLExecute("DELETE FROM temp_data WHERE session_id = ?sSessionId?");
```

See the [`SQLExecute` reference](../reference/functions/SQLExecute.md) for a full example of traversing a dataset result.

## SQL injection protection

SSL can check the SQL text sent on a connection for suspicious patterns, such as comments and misplaced semicolons. [`DetectSqlInjections`](../reference/functions/DetectSqlInjections.md) turns that check on or off per connection and returns the previous state. Detection is on by default. If a block of code depends on it, save the previous state, make sure detection is on, and restore the saved state when the block ends. Don't finish with `DetectSqlInjections(.F.)`: detection was already on, so that would switch off a protection the rest of the code relies on:

```ssl
:DECLARE bPrev, aRows, oErr;

/* Detection is on by default, make sure it stays on for this block;
bPrev := DetectSqlInjections(.T.);

:TRY;
    /* User input travels as a bound value, never as SQL text;
    aRows := LSelect1("SELECT sample_id, status FROM samples WHERE sample_id = ?",, {sUserSampleId});
:CATCH;
    oErr := GetLastSSLError();
    ErrorMes("Sample lookup failed: " + oErr:Description);
:FINALLY;
    /* Restore the state the caller had;
    DetectSqlInjections(bPrev);
:ENDTRY;
```

However, **parameterized queries are the primary defense**. [`DetectSqlInjections`](../reference/functions/DetectSqlInjections.md) is a secondary safeguard, not a replacement for proper parameter binding.
