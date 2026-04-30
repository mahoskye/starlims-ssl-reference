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
/* Single value;
sName := LSearch("SELECT name FROM users WHERE user_id = ?", "",, {"USR001"});

/* Multiple rows;
aResults := LSelect1("SELECT sample_id, status FROM samples WHERE batch = ?",, {"B-100"});

/* Execute a statement;
RunSQL("UPDATE samples SET status = 'C' WHERE sample_id = ?",, {"S-001"});

/* XML dataset;
sXml := GetDataSet("SELECT sample_id FROM samples WHERE batch = ?",, {"B-100"});

/* Named-parameter query;
sBatch := "B-100";
aRows := SQLExecute("SELECT sample_id FROM samples WHERE batch = ?sBatch?");
```

## Connection names

Most SQL functions accept an optional connection name parameter that identifies which configured database to run the query against. When omitted, the function uses the current default connection.

The connection name is the key registered in the system's database configuration. You can discover available names at runtime with [`GetConnectionStrings`](../reference/functions/GetConnectionStrings.md), which returns a 2D array where column 1 is the connection name, column 2 is the provider, and column 3 is the full connection string.

```ssl
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

The same connection name parameter appears in [`RunSQL`](../reference/functions/RunSQL.md), [`LSearch`](../reference/functions/LSearch.md), [`LSelect1`](../reference/functions/LSelect1.md), [`SQLExecute`](../reference/functions/SQLExecute.md), [`GetDataSet`](../reference/functions/GetDataSet.md), and related functions — always as the second argument after the SQL string.

## Parameterized queries

All SQL functions support parameterized queries using the `?` placeholder. This is the **recommended approach** for any query that includes user-supplied or variable data.

### How it works

Place a `?` in your SQL wherever a value should go, then pass the values as an array as the last argument. The engine replaces each `?` with a database-appropriate parameter (e.g., `@param1` for SQL Server, `:param1` for Oracle) and binds the values safely.

```ssl
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

The number of `?` placeholders must match the number of elements in the values array. A mismatch throws a "Parameters count mismatch" error. Each `?` is positional — there are no named parameters, so if you need the same value in multiple places, you must pass it multiple times.

```ssl
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

Sanitizes an array for use with a parameterized `IN` clause. It modifies the array in place — replacing empty string elements with a sentinel value that matches nothing, and appending a typed sentinel for empty arrays so the query stays syntactically valid.

```ssl
:DECLARE aSampleIds, sTemp, sPlaceholders, sSQL, aResults;

/* Build the array of values to match;
aSampleIds := {"S-001", "S-002", "S-003"};

/* Prepare the array — replaces empty strings with sentinels;
PrepareArrayForIn(aSampleIds, "string");
/* Array is now: {"S-001", "S-002", "S-003"} (unchanged, no empties);

/* Build matching ? placeholders: ?,?,?;
sTemp         := Replicate("?,", ALen(aSampleIds));
sPlaceholders := Left(sTemp, Len(sTemp) - 1);
/* sPlaceholders = "?,?,?";

/* Use with parameterized query;
sSQL := "SELECT sample_id, status FROM samples";
sSQL := sSQL + " WHERE sample_id IN (" + sPlaceholders + ")";

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
    Both functions handle empty arrays gracefully by substituting a type-appropriate sentinel value that matches no real rows. This ensures the SQL is syntactically valid and returns zero rows instead of throwing an error.

## String concatenation (not recommended)

The alternative to parameterized queries is building the SQL string with concatenation and [`LimsString`](../reference/functions/LimsString.md):

```ssl
/* String concatenation — avoid when possible;
sSQL := "SELECT * FROM samples WHERE batch_id = " + LimsString(sBatchId);
sSQL := sSQL + " AND status = " + LimsString(sStatus);
aResults := LSelect1(sSQL);
```

[`LimsString`](../reference/functions/LimsString.md) wraps strings in single quotes and formats dates and numbers for SQL. While it handles basic quoting, it is **not a substitute for parameterized queries**:

- No protection against SQL injection if values contain crafted content
- Date and number formatting depends on server locale settings
- More error-prone to construct correctly

!!! warning "Prefer parameterized queries"
    Use `?` placeholders with an array of values for any query that includes variable data. Reserve string concatenation for fully static SQL or cases where the table/column name itself is dynamic (which cannot be parameterized).

## Function reference

### LSearch — single value

Returns the first column of the first row, or a default value if no rows match:

```ssl
/* Get a single value with a fallback default;
sStatus := LSearch("SELECT status FROM samples WHERE sample_id = ?", "UNKNOWN",, {"S-001"});

/* Numeric result;
nCount := LSearch("SELECT COUNT(*) FROM samples WHERE batch_id = ?", 0,, {"B-100"});
```

The second parameter is the default returned when the query finds no rows. This avoids needing to check for NIL after every lookup.

### LSelect1 — result array

Returns a 2D array where rows are the first dimension and columns are the second:

```ssl
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

Returns [`.T.`](../reference/literals/true.md) on success. Error behavior depends on [`IgnoreSqlErrors`](../reference/functions/IgnoreSqlErrors.md) and [`ShowSqlErrors`](../reference/functions/ShowSqlErrors.md) flags (see [SQL & Transactions guide](sql-transactions.md#sql-error-handling)).

```ssl
bOk := RunSQL("INSERT INTO audit_log (action, ts) VALUES (?, ?)",, {"LOGIN", DToS(Now())});
:IF !bOk;
    ErrorMes("Audit log insert failed");
:ENDIF;
```

### GetDataSet — XML output

Returns a SELECT result as an XML string. Useful when passing data to external systems or storing structured output:

```ssl
sXml := GetDataSet("SELECT sample_id, status FROM samples WHERE batch = ?",, {"B-100"});
```

## SQLExecute — flexible execution

[`SQLExecute`](../reference/functions/SQLExecute.md) differs from the other SQL functions in two ways: it uses **named `?varName?` placeholders** instead of a positional values array, and its return type is controlled by an explicit parameter.

### Named parameters

Instead of passing a separate values array, you embed variable names directly in the SQL using `?varName?` syntax. The engine substitutes the current value of each named variable from the calling scope at execution time:

```ssl
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

SSL includes a [`DetectSqlInjections`](../reference/functions/DetectSqlInjections.md) function that can be enabled per connection to detect suspicious patterns:

```ssl
/* Enable injection detection on the default connection;
DetectSqlInjections(.T.);

/* Your queries run with detection active;
RunSQL(sUserSuppliedSQL);

/* Disable when done;
DetectSqlInjections(.F.);
```

However, **parameterized queries are the primary defense**. [`DetectSqlInjections`](../reference/functions/DetectSqlInjections.md) is a secondary safeguard, not a replacement for proper parameter binding.
