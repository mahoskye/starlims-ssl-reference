# Data Source Files

STARLIMS has three kinds of executable SSL files. **Data source files** are not compiled directly — they are preprocessed by server-side builders that rewrite them into compiler-compatible SSL before compilation. This means data source files use parameter syntax and directives that do not exist elsewhere in the SSL grammar.

## File types at a glance

| File type | Compiler-handled | Parameter syntax | Notes |
|-----------|------------------|------------------|-------|
| **Server script** | Yes | `:PARAMETERS p1, p2;` + [`:DEFAULT`](../reference/keywords/DEFAULT.md) lines | Standard SSL — all grammar rules apply |
| **SSL data source** | Preprocessed first | `:PARAMETERS p1 := val1, p2 := val2;` | Rewritten into script form before compilation |
| **SQL data source** | Preprocessed first | `:PARAMETERS p1 := val1, p2 := val2;` | Rewritten into a [`GetSSLDataset`](../reference/functions/GetSSLDataset.md) call before compilation |

If you are writing an ordinary script, follow the rules in [Getting Started](../getting-started.md). The rest of this page covers data source files specifically.

## Inline parameter defaults

In SSL and SQL data source files, [`:PARAMETERS`](../reference/keywords/PARAMETERS.md) uses inline `:=` assignment for defaults — there is **no** separate [`:DEFAULT`](../reference/keywords/DEFAULT.md) statement:

```ssl
:PARAMETERS sStatus := "A", nMaxRows := 100;
```

**Rules:**

- Every parameter **must** have a default value (the builder reports an error otherwise).
- `:PARAMETERS;` with no parameters is an error.
- Do **not** use `:DEFAULT` lines in data sources — defaults are inline only.
- Standard script layout rules do not apply.

The builder rewrites the inline form into compiler-compatible SSL before compilation:

```ssl
:PARAMETERS sStatus, nMaxRows;
:DEFAULT sStatus, "A";
:DEFAULT nMaxRows, 100;
```

## SQL data source directives

SQL data source files accept additional directives that the `SqlDataSourceBuilder` consumes during preprocessing. They are **not** SSL keywords:

```ssl
:DSN := connectionName;
:TABLENAME := tableName;
:NULLASBLANK := true;
:INVARIANTDATECOLUMNS := col1, col2;
:PARAMETERS sStatus := "A", nLimit := 50;

SELECT *
FROM sample
WHERE status = ?sStatus?
```

| Directive | Purpose |
|-----------|---------|
| `:DSN := name;` | Database connection name to use |
| `:TABLENAME := name;` | Table name for the resulting dataset |
| `:NULLASBLANK := true;` | Controls null-to-blank conversion |
| `:INVARIANTDATECOLUMNS := col1, col2;` | Columns treated as invariant (culture-neutral) dates |

The builder rewrites the entire file into an SSL script that calls [`GetSSLDataset`](../reference/functions/GetSSLDataset.md) with the appropriate arguments.

## Calling data sources

Data sources are invoked at runtime via [`RunDS`](../reference/functions/RunDS.md):

```ssl
/* Call with default parameters;
oResult := RunDS("Category.DataSourceName");

/* Call with parameter overrides — array of {name, value} pairs;
oResult := RunDS("Category.DataSourceName", {{"sStatus", "P"}, {"nLimit", 25}});

/* Return as an SSLDataset object;
oDs := RunDS("Category.DataSourceName",, "ssldataset");
```

Use [`GetDSParameters`](../reference/functions/GetDSParameters.md) to introspect a data source's parameter metadata at runtime.
