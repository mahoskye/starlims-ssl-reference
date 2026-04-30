---
title: "GetTables"
summary: "Extracts table names from the FROM portion of a SQL SELECT string."
id: ssl.function.gettables
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetTables

Extracts table names from the `FROM` portion of a SQL `SELECT` string.

`GetTables` performs text parsing on a SQL string and returns the table names it can identify after the `FROM` clause. The implementation first looks for a `SELECT ... FROM` pattern, then scans the text up to the first `WHERE`, `GROUP`, `HAVING`, or `ORDER` keyword and collects table names that appear at the start of the list, after commas, or after `JOIN`.

If the input is [`NIL`](../literals/nil.md), empty, or does not match that `SELECT ... FROM` pattern, the function returns an empty array. It parses query text only. It does not connect to the database, validate whether the tables exist, or resolve aliases.

## When to use

- When you need a quick list of table names from a `SELECT` statement.
- When inspecting user-built SQL before applying your own checks or rules.
- When you need the first-level tables named in a `FROM` clause with joins or comma-separated sources.

## Syntax

```ssl
GetTables([sSql])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSql` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | SQL text to inspect for table names. |

## Returns

**[array](../types/array.md)** — Table names found in the `FROM` portion of the SQL text, one per element. Returns an empty array when the input is [`NIL`](../literals/nil.md), empty, or does not match the `SELECT ... FROM` pattern. Names with a leading [`#`](../operators/hash.md) are returned without the [`#`](../operators/hash.md).

## Best practices

!!! success "Do"
    - Pass a normal `SELECT` statement when you want predictable results.
    - Treat the result as a text-parsing aid, then apply any validation you need separately.
    - Expect an empty array when the SQL does not contain a recognizable `SELECT ... FROM` section.

!!! failure "Don't"
    - Use it as a database-existence check. It parses SQL text only.
    - Assume it understands every SQL construct beyond the first `FROM` section it scans.
    - Assume the result includes aliases, schema validation, or later query sections after `WHERE`, `GROUP`, `HAVING`, or `ORDER`.

## Caveats

- The function is case-insensitive when locating the `SELECT`, `FROM`, and stop keywords.
- It recognizes unquoted names, quoted names, bracketed names, and qualified names such as `schema.table`.

## Examples

### Extract tables from a multi-join query

Parses a three-table join query and iterates over the returned array, showing that `GetTables` collects names from both the initial `FROM` entry and all subsequent `JOIN` clauses.

```ssl
:PROCEDURE ListJoinedTables;
    :DECLARE sSql, aTables, nIndex;

    sSql := "
        SELECT s.sampleid, t.testcode, r.result
        FROM sample s
        INNER JOIN test t
          ON t.sampleid = s.sampleid
        LEFT OUTER JOIN result r
          ON r.sampleid = s.sampleid
          AND r.testcode = t.testcode
        WHERE s.status = 'L'
    ";

    aTables := GetTables(sSql);

    :IF ALen(aTables) > 0;
        :FOR nIndex := 1 :TO ALen(aTables);
            UsrMes("Matched table: " + aTables[nIndex]);
            /* Displays matched table names;
        :NEXT;
    :ELSE;
        UsrMes("No tables matched the SQL text");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("ListJoinedTables");
```

### Reject SQL that references disallowed tables

Extracts all table names from the incoming SQL and checks each one against an allowlist, reporting disallowed names and returning [`.F.`](../literals/false.md) if any are found.

```ssl
:PROCEDURE ValidateQuerySources;
    :PARAMETERS sSql;
    :DECLARE aTables, aAllowed, nIndex, bValid;

    aAllowed := {"sample", "test", "result"};
    aTables := GetTables(sSql);
    bValid := ALen(aTables) > 0;

    :IF !bValid;
        UsrMes("Query must contain a recognizable SELECT and FROM clause");
        :RETURN .F.;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aTables);
        :IF AScan(aAllowed, Lower(aTables[nIndex])) == 0;
            UsrMes("Disallowed table in query: " + aTables[nIndex]);
            /* Displays each disallowed table name;
            bValid := .F.;
        :ELSE;
            UsrMes("Allowed table: " + aTables[nIndex]);
            /* Displays each allowed table name;
        :ENDIF;
    :NEXT;

    :RETURN bValid;
:ENDPROC;

/* Usage;
DoProc("ValidateQuerySources", {"SELECT s.sampleid FROM sample s WHERE s.status = 'L'"});
```

## Related

- [`GetDBMSName`](GetDBMSName.md)
- [`IsTable`](IsTable.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
