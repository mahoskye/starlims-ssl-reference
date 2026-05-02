# Data Source Files

STARLIMS has three kinds of executable SSL files: **server scripts**, **SSL data sources**, and **SQL data sources**. Data source files use parameter syntax and directives that don't appear in ordinary scripts. If you are writing an ordinary script, follow the rules in [Getting Started](../getting-started.md). The rest of this page covers data source files specifically.

## File types at a glance

| File type | Parameter syntax | Notes |
|-----------|------------------|-------|
| **Server script** | `:PARAMETERS p1, p2;` + [`:DEFAULT`](../reference/keywords/DEFAULT.md) lines | Standard SSL — all grammar rules apply |
| **SSL data source** | `:PARAMETERS p1 := val1, p2 := val2;` | Inline defaults; standard script layout rules do not apply |
| **SQL data source** | `:PARAMETERS p1 := val1, p2 := val2;` plus directives | Resolved at runtime through [`GetSSLDataset`](../reference/functions/GetSSLDataset.md) |

## Inline parameter defaults

In SSL and SQL data source files, [`:PARAMETERS`](../reference/keywords/PARAMETERS.md) uses inline `:=` assignment for defaults — there is **no** separate [`:DEFAULT`](../reference/keywords/DEFAULT.md) statement:

```ssl
:PARAMETERS sStatus := "A", nMaxRows := 100;
```

**Rules:**

- Every parameter **must** have a default value.
- `:PARAMETERS;` with no parameters is an error.
- Do **not** use `:DEFAULT` lines in data sources — defaults are inline only.
- Standard script layout rules do not apply.

## SQL data source directives

SQL data source files accept additional directives that are not SSL keywords and are valid only in this file type:

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
