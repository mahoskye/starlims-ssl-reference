# Data Source Files

A **data source** is a named, parameterized piece of data-retrieval code that callers run with [`RunDS`](../reference/functions/RunDS.md). A data source runs in one of two modes:

- **STARLIMS mode**: the body is SSL. Whatever the body returns with [`:RETURN`](../reference/keywords/RETURN.md) is the data source's result. These are sometimes called SSL data sources.
- **SQL mode**: the body is a SQL query in your database's dialect, preceded by optional directives and a `:PARAMETERS` line. The examples on this page use T-SQL (MS SQL Server). The query's rows are the result. These are sometimes called SQL data sources.

The mode belongs to the data source: you create or configure a data source in one mode or the other, and the body must match it. SSL features such as `:RETURN` and [`SQLExecute`](../reference/functions/SQLExecute.md) work only in STARLIMS mode. A SQL-mode body is a query, not SSL.

Data sources use parameter syntax and directives that don't appear in ordinary scripts. If you are writing an ordinary script, follow the rules in [Getting Started](../getting-started.md). The rest of this page covers data sources specifically.

## File types at a glance

| File type | Body | Parameter syntax | Result |
|-----------|------|------------------|--------|
| **Server script** | SSL | `:PARAMETERS p1, p2;` + [`:DEFAULT`](../reference/keywords/DEFAULT.md) lines | Whatever the script returns |
| **Data source, STARLIMS mode** | SSL | `:PARAMETERS p1 := val1, p2 := val2;` | Whatever the body `:RETURN`s |
| **Data source, SQL mode** | Directives, then a SQL query | `:PARAMETERS p1 := val1, p2 := val2;`, referenced in the query as `@p1` | The query's rows |

## Inline parameter defaults

In data sources of either mode, [`:PARAMETERS`](../reference/keywords/PARAMETERS.md) uses inline `:=` assignment for defaults — there is **no** separate [`:DEFAULT`](../reference/keywords/DEFAULT.md) statement:

```ssl
:PARAMETERS sStatus := "A", nMaxRows := 100;
```

**Rules:**

- Defaults are set inline with `:=` on the `:PARAMETERS` line. A parameter without a default is accepted, but what it receives when the caller leaves it out is not documented, so give a default to every parameter a caller may omit.
- `:PARAMETERS;` with no parameters is an error. A data source that takes no parameters leaves the `:PARAMETERS` line out.
- Do **not** use `:DEFAULT` lines in data sources — defaults are inline only.
- The inline-default form is what sets a STARLIMS-mode data source apart from a server script. The same `:PARAMETERS` line is not valid in a server script.

## STARLIMS-mode data sources

In STARLIMS mode the body is ordinary SSL. It can declare variables, define [`:PROCEDURE`](../reference/keywords/PROCEDURE.md) blocks and call them with [`DoProc`](../reference/functions/DoProc.md), and run queries with [`SQLExecute`](../reference/functions/SQLExecute.md), which marks parameters as `?name?`:

```ssl
:PARAMETERS sStatus := "Logged", sFromId := "";

:RETURN SQLExecute("
	SELECT sample_id, status, logdate
	FROM sample
	WHERE status = ?sStatus?
		AND sample_id >= ?sFromId?
	ORDER BY sample_id
");
```

This data source returns the matching rows as an array of rows, and [`RunDS`](../reference/functions/RunDS.md) passes that array back to the caller. [`PARAMETERS`](../reference/keywords/PARAMETERS.md#using-parameters-in-a-data-source-file) has another example.

`RunDS`'s return-type argument (`"ssldataset"`, `"xml"`, and so on) converts only an [`SSLDataset`](../reference/classes/SSLDataset.md) result. Any other value, including the array above, comes back unchanged whatever return type the caller asks for. If callers need those return types, have the body return an `SSLDataset`, for example from [`GetSSLDataset`](../reference/functions/GetSSLDataset.md).

## SQL-mode data sources

A SQL-mode data source is a SQL query. Parameters from the `:PARAMETERS` line are referenced as `@name`. The `?name?` markers used by `SQLExecute` do not work here. Directives come before the query:

```ssl
:DSN := DATABASE;
:TABLENAME := sample;
:NULLASBLANK := true;
:INVARIANTDATECOLUMNS := logdate;
:PARAMETERS sStatus := "Logged", sFromId := "";

SELECT sample_id, status, logdate
FROM sample
WHERE status = @sStatus
	AND sample_id >= @sFromId
ORDER BY sample_id
```

Comments in a SQL-mode data source use SQL syntax: `-- line comments` and `/* block comments */`. The SSL comment form, which ends at the first `;`, does not apply, so semicolons inside a SQL comment or string literal are just text.

It takes the same parameters and applies the same filter as the STARLIMS-mode example above, so both are called the same way. `RunDS` returns the rows as an array unless the caller asks for another return type.

### Directives

The directives are not SSL keywords. Their names are case-sensitive, so write them in uppercase: a lowercase `:nullasblank` line is ignored.

| Directive | Purpose |
|-----------|---------|
| `:DSN := name;` | Database connection name to use |
| `:TABLENAME := name;` | Table name for the resulting dataset |
| `:NULLASBLANK := true;` | Controls null-to-blank conversion. Write `true` or `false`. |
| `:INVARIANTDATECOLUMNS := col1, col2;` | Columns treated as invariant (culture-neutral) dates |

**`:NULLASBLANK`** takes the words `true` or `false`, matched case-insensitively (`TRUE` and `False` work too). With `true`, a `NULL` column value comes back as a blank value of the column's type, such as `""` for text and `0` for a number. With `false`, it comes back as [`NIL`](../reference/literals/nil.md). When the directive is absent, null-to-blank is on.

!!! warning "`.T.` and `.F.` do nothing here"
    `:NULLASBLANK` does not accept the SSL boolean literals. `:NULLASBLANK := .F.;` raises no error, but it is ignored, so null-to-blank stays on and `NULL` values still come back blank. Write `:NULLASBLANK := false;` to get `NIL` for `NULL` values.

**`:INVARIANTDATECOLUMNS`** takes bare column names separated by commas, such as `:INVARIANTDATECOLUMNS := logdate, releasedate;`. Do not quote the names: a quoted name raises no error, but the quotes are kept as part of the name, so it matches no column.

## Calling data sources

Data sources are invoked at runtime via [`RunDS`](../reference/functions/RunDS.md):

```ssl
:DECLARE oResult, oDs;

/* Call with default parameters;
oResult := RunDS("Category.DataSourceName");

/* Call with parameter overrides, in :PARAMETERS order;
oResult := RunDS("Category.DataSourceName", {"Released", "S-1000"});

/* Return as an SSLDataset object;
oDs := RunDS("Category.DataSourceName",, "ssldataset");
```

Parameter values bind by **position**, in the order the data source declares them in `:PARAMETERS`; names are not matched. For the examples above, `{"Released", "S-1000"}` sets `sStatus` to `"Released"` and `sFromId` to `"S-1000"`. Trailing values you leave out take their inline defaults, and values beyond the declared parameters are silently ignored. Passing `{name, value}` pairs does not work: each pair is bound whole to one parameter.

The return-type argument in the last call converts only an `SSLDataset` result. A STARLIMS-mode data source that returns an array still returns that array (see [STARLIMS-mode data sources](#starlims-mode-data-sources)).

Use [`GetDSParameters`](../reference/functions/GetDSParameters.md) to get a data source's parameter names in declaration order, which is the order `RunDS` binds them.
