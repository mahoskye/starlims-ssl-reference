---
title: "PatcherSupport"
summary: "Provides helper methods for collecting package-style dictionary metadata, connecting to another STARLIMS system, and comparing one collected result table to another."
id: ssl.class.patchersupport
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# PatcherSupport

Provides helper methods for collecting package-style dictionary metadata, connecting to another STARLIMS system, and comparing one collected result table to another.

`PatcherSupport` maintains its collected rows in `ResultTable`. Calling `GetDataFromWholeDictionary()` appends rows for application forms, application and category server scripts, application and category data sources, client scripts, and dictionary and database tables. Calling `Compare()` removes rows from the current `ResultTable` when the matching item in the destination table has the same stored hashes, then sorts the remaining rows and stores a serialized dataset copy in `DiffDataTable`.

## When to use

- When you need one result table that combines forms, server scripts, data sources, client scripts, and tables from a STARLIMS dictionary.
- When you need to compare one collected package table against another and keep only the rows that still differ.
- When you need to connect to another STARLIMS system before collecting data from that system.
- When you need to inspect accumulated errors after a log-file setup failure or a metadata retrieval failure.

## Constructors

### `PatcherSupport{}`

Creates a new `PatcherSupport` object with an empty result table.

The object also starts with a default log file path value, but trace logging is not configured until you assign `LogFilePath`.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `DiffDataTable` | [string](../types/string.md) | read-only | Serialized dataset string produced by the most recent successful `Compare()` call. Empty until a comparison serializes the current result table. |
| `InternalErrors` | [string](../types/string.md) | read-only | Accumulated error text captured when log-file setup fails or when metadata retrieval calls fail while collecting forms, scripts, data sources, or tables. |
| `LogFilePath` | [string](../types/string.md) | read-write | Current log file path. Setting it attempts to create or replace the file and resets the active trace listeners to write to that file. |
| `ResultTable` | [object](../types/object.md) | read-only | Current package table used for collected dictionary metadata and later comparison results. |

## Methods

### `Compare`

Compares the current `ResultTable` to another package table. The method returns [`NIL`](../literals/nil.md) when the destination value is not a table object or when either table is missing. Otherwise it compares form rows by `XFDHash`, `CodeHash`, and `ResourceHash`, compares non-form item rows by `CodeHash`, removes unchanged rows from the current `ResultTable`, sorts the remaining rows by category and application identifiers, stores a serialized dataset copy in `DiffDataTable`, and returns the filtered table.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oDestinationDataTable` | [object](../types/object.md) | yes | Table to compare against the current `ResultTable`. |

**Returns:** [object](../types/object.md) — Filtered result table, or [`NIL`](../literals/nil.md) when comparison cannot be performed.

### `ConnectToExternalSystem`

Attempts to connect to another STARLIMS system using the supplied URL, username, and password. The URL is converted to the generic service endpoint before login is attempted.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sUrl` | [string](../types/string.md) | yes | Base URL for the target STARLIMS system. |
| `sUser` | [string](../types/string.md) | yes | User name used for login. |
| `sPassword` | [string](../types/string.md) | yes | Password used for login. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when login succeeds, otherwise [`.F.`](../literals/false.md).

### `GetDataFromWholeDictionary`

Collects metadata for application forms, application and category server scripts, application and category data sources, client scripts, and dictionary and database tables into `ResultTable`.

**Returns:** none — No return value.

### `GetAllFormsFromDictionary_Test`

Collects application form metadata into `ResultTable`.

**Returns:** none — No return value.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Populate `ResultTable` before calling `Compare()` so the comparison has a source table to work with.
    - Check the boolean result from `ConnectToExternalSystem()` before trying to read remote dictionary content.
    - Read `InternalErrors` after failed metadata retrieval or log-path setup so you can diagnose what went wrong.
    - Set `LogFilePath` before long collection or comparison runs when you want a fresh trace file for that run.
    - Use `DiffDataTable` after `Compare()` when you need a serialized copy of the remaining differences.

!!! failure "Don't"
    - Call `Compare()` with a non-table value or with missing tables — the method returns [`NIL`](../literals/nil.md) instead of producing comparison output.
    - Assume `Compare()` returns every row from the source table — unchanged rows are removed from the current result set.
    - Treat `ConnectToExternalSystem()` failures as thrown errors — the method reports failure with [`.F.`](../literals/false.md).
    - Expect `GetDataFromWholeDictionary()` to clear earlier rows first — it appends collected metadata to the existing `ResultTable`.
    - Assume setting `LogFilePath` always succeeds — invalid or inaccessible paths are recorded in `InternalErrors` and the trace listeners are only updated on success.

## Caveats

- `Compare()` updates both `ResultTable` and `DiffDataTable` when it succeeds.
- `GetAllFormsFromDictionary_Test()` is a narrow helper that loads only form metadata.
- `InternalErrors` is not the same as the trace log. It captures accumulated error text, while `LogFilePath` controls file-based trace output.

## Examples

### Collect dictionary metadata and compare it to another table

Collects the local dictionary into one `PatcherSupport` object, connects to a remote system and collects its dictionary into a second object, then calls `Compare()` on the local patcher to remove unchanged rows. The serialized diff is available in `DiffDataTable` when `Compare()` succeeds.

```ssl
:PROCEDURE CompareDictionaryMetadata;
	:DECLARE oLocalPatcher, oRemotePatcher, oDiffTable;
	:DECLARE bConnected;

	oLocalPatcher := PatcherSupport{};
	oLocalPatcher:GetDataFromWholeDictionary();

	oRemotePatcher := PatcherSupport{};
	bConnected := oRemotePatcher:ConnectToExternalSystem(
		"https://external-starlims.example.com/starlims",
		"admin",
		"secret"
	);

	:IF bConnected;
		oRemotePatcher:GetDataFromWholeDictionary();
		oDiffTable := oLocalPatcher:Compare(oRemotePatcher:ResultTable);
	:ELSE;
		oDiffTable := NIL;
	:ENDIF;

	:IF Empty(oDiffTable);
		UsrMes("Comparison could not be completed.");
	:ELSE;
		UsrMes("Comparison completed.");

		:IF .NOT. Empty(oLocalPatcher:DiffDataTable);
			UsrMes("Serialized differences are available.");
		:ENDIF;
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("CompareDictionaryMetadata");
```

### Connect to another system before collecting metadata

Sets `LogFilePath` to create a trace file for the run, then calls `ConnectToExternalSystem()` before attempting to collect dictionary metadata. If connection fails, `InternalErrors` is checked for any captured error detail.

```ssl
:PROCEDURE CollectExternalDictionaryMetadata;
	:DECLARE oPatcher, bConnected;
	:DECLARE sUrl, sUser, sPassword;

	sUrl := "https://external-starlims.example.com/starlims";
	sUser := "admin";
	sPassword := "secret";

	oPatcher := PatcherSupport{};
	oPatcher:LogFilePath := "C:/Logs/PatcherSupport.log";

	bConnected := oPatcher:ConnectToExternalSystem(sUrl, sUser, sPassword);

	:IF bConnected;
		oPatcher:GetDataFromWholeDictionary();
		UsrMes("Dictionary metadata collected.");
	:ELSE;
		UsrMes("Connection failed.");

		:IF .NOT. Empty(oPatcher:InternalErrors);
			/* Displays internal error details on failure;
			UsrMes(oPatcher:InternalErrors);
		:ENDIF;
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("CollectExternalDictionaryMetadata");
```

## Related

- [`CDataTable`](CDataTable.md)
