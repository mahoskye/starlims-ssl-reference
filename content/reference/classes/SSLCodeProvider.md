---
title: "SSLCodeProvider"
summary: "Compiles published server scripts and data sources and returns the compilation results as an SSLCompilerErrorList."
id: ssl.class.sslcodeprovider
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLCodeProvider

Compiles published server scripts and data sources and returns the compilation results as an `SSLCompilerErrorList`.

Use `SSLCodeProvider{}` when you need to validate published SSL code before a release, during deployment checks, or while troubleshooting compile failures. The class can compile all server scripts, all data sources, one item, or all items in one or more categories. For single-item methods, pass either the item GUID or its full name in `category.name` format.

## When to use

- When you need to validate all published server scripts before a release.
- When you need to check one changed script or data source after an edit.
- When you need to recompile all content in a category during focused testing.
- When you need to capture compile errors in an automation script and report them.

## Constructors

### `SSLCodeProvider{}`

Creates a code provider instance.

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `CompileAll` | `SSLCompilerErrorList` | Compiles all server scripts and data sources. |
| `CompileAllServerScripts` | `SSLCompilerErrorList` | Compiles all server scripts. |
| `CompileAllDataSources` | `SSLCompilerErrorList` | Compiles all data sources. |
| `CompileServerScript` | `SSLCompilerErrorList` | Compiles one server script by GUID or full name. |
| `CompileServerScripts` | `SSLCompilerErrorList` | Compiles multiple server scripts. |
| `CompileServerScriptCategory` | `SSLCompilerErrorList` | Compiles all server scripts in one category. |
| `CompileServerScriptCategories` | `SSLCompilerErrorList` | Compiles all server scripts in multiple categories. |
| `CompileDataSource` | `SSLCompilerErrorList` | Compiles one data source by GUID or full name. |
| `CompileDataSources` | `SSLCompilerErrorList` | Compiles multiple data sources. |
| `CompileDataSourceCategory` | `SSLCompilerErrorList` | Compiles all data sources in one category. |
| `CompileDataSourceCategories` | `SSLCompilerErrorList` | Compiles all data sources in multiple categories. |
| `CompileScript` | `SSLCompilerErrorList` | Accepts SSL code text, but currently raises a not-implemented error for non-null input. |

### `CompileAll`

Compiles all published server scripts and all published data sources.

**Returns:** SSLCompilerErrorList — Compilation errors collected from both server scripts and data sources.

### `CompileAllServerScripts`

Compiles all server scripts.

**Returns:** SSLCompilerErrorList — Compilation errors collected from all server scripts.

### `CompileAllDataSources`

Compiles all data sources.

**Returns:** SSLCompilerErrorList — Compilation errors collected from all data sources.

### `CompileServerScript`

Compiles one server script by GUID or full name.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sScriptId` | [string](../types/string.md) | yes | Server script GUID or full name in `category.script` format. |

**Returns:** SSLCompilerErrorList — Compilation errors for the requested server script.

**Raises:**
- `Argument sScriptId cannot be null.` when `sScriptId` is omitted.
- `Argument sScriptId cannot be null or empty.` when `sScriptId` is an empty string.
- An argument error when `sScriptId` is not a GUID and is not supplied as a full `category.script` name.

### `CompileServerScripts`

Compiles multiple server scripts.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `aScriptsIds` | [array](../types/array.md) | yes | Array of server script GUIDs or full names in `category.script` format. |

**Returns:** SSLCompilerErrorList — Combined compilation errors for the requested server scripts.

**Raises:**
- `Argument aScriptsIds cannot be null.` when `aScriptsIds` is omitted.

### `CompileServerScriptCategory`

Compiles all server scripts in one category.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sCategoryId` | [string](../types/string.md) | yes | Category GUID used to select the server scripts to compile. |

**Returns:** SSLCompilerErrorList — Combined compilation errors for the server scripts in that category.

**Raises:**
- `Argument sCategoryId cannot be null.` when `sCategoryId` is omitted.

### `CompileServerScriptCategories`

Compiles all server scripts in multiple categories.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `aCategoriesIds` | [array](../types/array.md) | yes | Array of category GUIDs. |

**Returns:** SSLCompilerErrorList — Combined compilation errors for all server scripts in the requested categories.

**Raises:**
- `Argument aCategoriesIds cannot be null.` when `aCategoriesIds` is omitted.

### `CompileDataSource`

Compiles one data source by GUID or full name.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sScriptId` | [string](../types/string.md) | yes | Data source GUID or full name in `category.datasource` format. |

**Returns:** SSLCompilerErrorList — Compilation errors for the requested data source.

**Raises:**
- `Argument sScriptId cannot be null.` when `sScriptId` is omitted.
- `Argument sScriptId cannot be null or empty.` when `sScriptId` is an empty string.
- An argument error when `sScriptId` is not a GUID and is not supplied as a full `category.datasource` name.

### `CompileDataSources`

Compiles multiple data sources.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `aScriptsIds` | [array](../types/array.md) | yes | Array of data source GUIDs or full names in `category.datasource` format. |

**Returns:** SSLCompilerErrorList — Combined compilation errors for the requested data sources.

**Raises:**
- `Argument aScriptsIds cannot be null.` when `aScriptsIds` is omitted.

### `CompileDataSourceCategory`

Compiles all data sources in one category.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sCategoryId` | [string](../types/string.md) | yes | Category GUID used to select the data sources to compile. |

**Returns:** SSLCompilerErrorList — Combined compilation errors for the data sources in that category.

**Raises:**
- `Argument sCategoryId cannot be null.` when `sCategoryId` is omitted.

### `CompileDataSourceCategories`

Compiles all data sources in multiple categories.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `aCategoriesIds` | [array](../types/array.md) | yes | Array of category GUIDs. |

**Returns:** SSLCompilerErrorList — Combined compilation errors for all data sources in the requested categories.

**Raises:**
- `Argument aCategoriesIds cannot be null.` when `aCategoriesIds` is omitted.

### `CompileScript`

Accepts a block of SSL code as text.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sCode` | [string](../types/string.md) | yes | SSL code text to compile. |

**Returns:** SSLCompilerErrorList — Intended compilation result object.

**Raises:**
- `Argument sCode cannot be null.` when `sCode` is omitted.
- `The method or operation is not implemented.` for any non-null `sCode` value.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Pass a full `category.name` or a GUID when targeting one server script or data source.
    - Use the bulk and category methods when validating larger changes.
    - Check the returned `SSLCompilerErrorList` even when you expect a clean compile.
    - Use category GUIDs with the `...Category` and `...Categories` methods.

!!! failure "Don't"
    - Pass a bare script or data source name without its category. Those calls are rejected unless you provide a GUID.
    - Use `CompileScript` for ad hoc code validation. It currently raises a not-implemented error for any non-null input.
    - Assume a successful call means every target compiled cleanly. Review the returned error list before continuing automation or deployment steps.

## Caveats

- Single-item compile methods require either a GUID or a full `category.name`.
- Category methods take category IDs, not category names.
- The class reports compile-time problems only. It does not validate runtime behavior.

## Examples

### Compile one server script

Compiles a specific server script by full name and returns the `SSLCompilerErrorList` to the caller for inspection.

```ssl
:PROCEDURE ValidateOneScript;
	:DECLARE oProvider, oErrors;

	oProvider := SSLCodeProvider{};
	oErrors := oProvider:CompileServerScript("QC.ReleaseSample");

	:RETURN oErrors;
:ENDPROC;
```

Call it with `DoProc("ValidateOneScript")`.

### Compile one category of data sources

Compiles all data sources in a known category by its GUID and returns the combined `SSLCompilerErrorList` to the caller.

```ssl
:PROCEDURE ValidateDataSourceCategory;
	:DECLARE oProvider, oErrors;

	oProvider := SSLCodeProvider{};
	oErrors := oProvider:CompileDataSourceCategory("7D7E2CC8-0CC9-4F32-9D31-54C51A7E7C40");

	:RETURN oErrors;
:ENDPROC;
```

Call it with `DoProc("ValidateDataSourceCategory")`.

### Compile all server scripts and data sources

Runs a full validation pass across all published scripts and data sources. Useful as a pre-deployment check.

```ssl
:PROCEDURE ValidateAllPublishedCode;
	:DECLARE oProvider, oErrors;

	oProvider := SSLCodeProvider{};
	oErrors := oProvider:CompileAll();

	:RETURN oErrors;
:ENDPROC;
```

Call it with `DoProc("ValidateAllPublishedCode")`.

### Compile a selected list of changed scripts

Compiles a targeted list of changed scripts in one pass rather than recompiling everything.

```ssl
:PROCEDURE ValidateChangedScripts;
	:DECLARE oProvider, oErrors, aScriptIds;

	aScriptIds := {"QC.ReleaseSample", "QC.ApproveBatch"};

	oProvider := SSLCodeProvider{};
	oErrors := oProvider:CompileServerScripts(aScriptIds);

	:RETURN oErrors;
:ENDPROC;
```

Call it with `DoProc("ValidateChangedScripts")`.

## Related

- [`SSLError`](SSLError.md)
- [`GetLastSSLError`](../functions/GetLastSSLError.md)
- [`RunDS`](../functions/RunDS.md)
