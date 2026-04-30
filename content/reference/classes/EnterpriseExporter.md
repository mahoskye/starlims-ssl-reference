---
title: "EnterpriseExporter"
summary: "Exports tables into a destination folder."
id: ssl.class.enterpriseexporter
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# EnterpriseExporter

Exports tables into a destination folder.

`EnterpriseExporter` writes each exported table into its own subfolder under the path you pass to the constructor. In default mode, pass a simple array of table names. If you enable `IsEnterpriseOnly` or `FromSQL`, pass an array of table entries where each item contains the table name and an optional second string value that changes what gets exported for that table.

## When to use

- When you need to export selected regular tables or system tables to disk.
- When you want the default exporter to write all available tables by passing an empty table list.
- When you need to control the source used for each exported table in enterprise-only mode.
- When you need SQL-mode export options such as `NullAsBlank` or `InvariantDateColumns`.
- When you want a log file for per-table export progress.

## Constructors

### `EnterpriseExporter{aTables, bSysTables, sPath}`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `aTables` | [array](../types/array.md) | yes | Table list. Use a simple array of table names in default mode, or an array of table entries in `IsEnterpriseOnly` and `FromSQL` modes. In entry-based modes, each entry starts with the output table name and can include a second string value used as the source string for that table. |
| `bSysTables` | [boolean](../types/boolean.md) | yes | When [`.T.`](../literals/true.md), exports system-table content instead of regular table content. |
| `sPath` | [string](../types/string.md) | yes | Destination folder for the export output. The exporter writes one subfolder and one `.txt` file per table. |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `AbortOnError` | [boolean](../types/boolean.md) | read-write | Writable flag on the class. In practice, setting it does not change `DoExport()` behavior. |
| `LogFile` | [string](../types/string.md) | read-write | Log file path or `"console"` for console logging. |
| `IsEnterpriseOnly` | [boolean](../types/boolean.md) | write-only | Switches the export to enterprise-only mode, where each table entry can supply a custom `FROM` source. |
| `FromSQL` | [boolean](../types/boolean.md) | write-only | Switches the export to SQL mode, where each table entry can supply a full SQL statement. |
| `NullAsBlank` | [boolean](../types/boolean.md) | write-only | In SQL mode, controls whether exported `NULL` values are treated as blanks. Defaults to [`.F.`](../literals/false.md). |
| `InvariantDateColumns` | [array](../types/array.md) | write-only | In SQL mode, supplies the invariant date columns passed to the export operation. |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `DoExport()` | [boolean](../types/boolean.md) | Runs the export and returns the completion result from the underlying export process. It also updates `ErrorMsg` with the final exporter message when the call returns normally. |

## Inheritance

**Base class:** `EnterpriseImpExBase`

Inherited member:

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `ErrorMsg` | [string](../types/string.md) | read-write | Final error text from the export run. |

## Best practices

!!! success "Do"
    - Pass a destination folder, not a file name.
    - Use a simple array of table names for default-mode exports.
    - Use table-entry arrays when `IsEnterpriseOnly` or `FromSQL` is enabled.
    - In enterprise-only mode, use the second entry value as the `FROM` source when you need a custom source per exported table.
    - In SQL mode, use the second entry value for the full SQL statement you want exported for that table.
    - Set `LogFile` when you need per-table confirmation and troubleshooting.
    - Use `NullAsBlank` and `InvariantDateColumns` only with `FromSQL`.
    - Use [`:TRY`](../keywords/TRY.md) and [`GetLastSSLError`](../functions/GetLastSSLError.md) if your script must handle invalid table definitions safely.

!!! failure "Don't"
    - Describe `sPath` as a single export file. The exporter creates a subfolder for each table and writes that table's text file inside it.
    - Assume an empty `aTables` array always means "export everything." That only happens in default mode.
    - Use a one-dimensional table list with `IsEnterpriseOnly` or `FromSQL`. Those modes expect table entries.
    - Treat the second value in a table entry as arbitrary metadata. In enterprise-only mode it is the `FROM` source, and in SQL mode it is the full SQL statement.
    - Rely on `AbortOnError` to stop the run. Setting it does not affect `DoExport()`.
    - Treat `DoExport()` by itself as a per-table success report for multi-table runs. Use the log file when you need table-by-table confirmation.
    - Expect `NullAsBlank` or `InvariantDateColumns` to affect default or enterprise-only exports. They are used only in SQL mode.
    - Assume every bad table definition only returns [`.F.`](../literals/false.md). Undefined tables can raise an error during export setup.

## Caveats

- In default mode, an empty table list exports all regular tables or all system tables, depending on `bSysTables`.
- In enterprise-only mode and SQL mode, an empty table list fails.
- If both `IsEnterpriseOnly` and `FromSQL` are set to [`.T.`](../literals/true.md), enterprise-only mode takes precedence.
- If a table export fails after its output folder is created, that table's output folder is removed.
- An undefined table or a table with no defined fields can raise an error instead of only returning [`.F.`](../literals/false.md).
- `ErrorMsg` reports the final exporter message, which can be blank even after an earlier table failed.

## Examples

### Export selected regular tables

Passes a named table list in default mode. Because `DoExport()` does not report per-table status, the example sets `LogFile` so the log captures each table's outcome. The success branch reports the log for follow-up; the failure branch reads `ErrorMsg` for the final exporter message.

```ssl
:PROCEDURE ExportSelectedTables;
	:DECLARE aTables, oExporter, bSuccess;

	aTables := {"users", "roles", "permissions"};
	oExporter := EnterpriseExporter{aTables, .F., "C:/Exports/EnterpriseData"};
	oExporter:LogFile := "C:/Exports/EnterpriseData/export.log";

	bSuccess := oExporter:DoExport();

	:IF bSuccess;
		UsrMes("Export run completed. Review the log file for per-table results.");
	:ELSE;
		/* Displays on failure: final exporter message;
		UsrMes("Export failed: " + oExporter:ErrorMsg);
	:ENDIF;

	:RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("ExportSelectedTables");
```

### Export in enterprise-only mode with a custom source

Sets `IsEnterpriseOnly` and passes a table entry array where each entry's second value is the `FROM` source for the generated `SELECT`. Here `enterprise_users_view` replaces the default table name as the source for the `users` output.

```ssl
:PROCEDURE ExportEnterpriseOnlyTable;
	:DECLARE aTables, oExporter, bSuccess;

	aTables := {{"users", "enterprise_users_view"}};

	oExporter := EnterpriseExporter{aTables, .F., "C:/Exports/EnterpriseOnly"};
	oExporter:IsEnterpriseOnly := .T.;
	oExporter:LogFile := "C:/Exports/EnterpriseOnly/export.log";

	bSuccess := oExporter:DoExport();

	:IF .NOT. bSuccess;
		/* Displays on failure: final exporter message;
		UsrMes("Enterprise-only export failed: " + oExporter:ErrorMsg);
	:ENDIF;

	:RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("ExportEnterpriseOnlyTable");
```

### Export in SQL mode with date handling options

Sets `FromSQL` and supplies a full SQL statement as the second value in each table entry. `NullAsBlank` converts exported `NULL` values to blank strings, and `InvariantDateColumns` ensures `reported_on` and `approved_on` are written in a locale-independent format.

```ssl
:PROCEDURE ExportWithSQLMode;
	:DECLARE aTables, aDateCols, oExporter, bSuccess;

	aTables := {{
		"analysis_results",
		"
SELECT sample_id, result_value, reported_on, approved_on
FROM analysis_results
WHERE approved_on IS NOT NULL
ORDER BY sample_id
"
	}};
	aDateCols := {"reported_on", "approved_on"};

	oExporter := EnterpriseExporter{aTables, .F., "C:/Exports/SqlMode"};
	oExporter:FromSQL := .T.;
	oExporter:NullAsBlank := .T.;
	oExporter:InvariantDateColumns := aDateCols;
	oExporter:LogFile := "C:/Exports/SqlMode/export.log";

	bSuccess := oExporter:DoExport();

	:IF .NOT. bSuccess;
		/* Displays on failure: final exporter message;
		UsrMes("SQL-mode export failed: " + oExporter:ErrorMsg);
	:ENDIF;

	:RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("ExportWithSQLMode");
```

## Related

- [`GetLastSSLError`](../functions/GetLastSSLError.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
