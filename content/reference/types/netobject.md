---
title: "netobject"
summary: "Provides dynamic access to external objects for property access, method invocation, and selected interop scenarios in SSL."
id: ssl.type.netobject
element_type: type
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# netobject

## What it is

Provides dynamic access to external objects for property access, method invocation, and selected interop scenarios in SSL.

The `netobject` type represents a value returned by SSL's .NET interop helpers such as [`MakeNETObject`](../functions/MakeNETObject.md), [`LimsNETConnect`](../functions/LimsNETConnect.md), and [`LimsNETTypeOf`](../functions/LimsNETTypeOf.md). Use it when you need to work with a .NET value from SSL code.

`netobject` lets you read and write public fields or properties with `GetProperty()` and `SetProperty()`, test for a public field or property with `IsProperty()`, and call public methods with `Invoke()`. Returned values come back as ordinary SSL values when possible; .NET values that still need interop access remain `netobject` values.

`IsEmpty()` returns [`.T.`](../literals/true.md) only when the wrapped reference is null. [`ToJson()`](../functions/ToJson.md) is supported only when the wrapped value is a `DataSet`; other wrapped values raise an error. `netobject` does not support [`AddProperty()`](../functions/AddProperty.md).

## Creating values

`netobject` values cannot be created with a literal. They are returned by interop functions.

```ssl
oBuilder := LimsNETConnect("System", "System.Text.StringBuilder", {"LAB"}, .F.);
oMath := LimsNETTypeOf("System.Math");
```

- **Runtime type:** `OBJECT`
- **Literal syntax:** None. Use [`MakeNETObject`](../functions/MakeNETObject.md), [`LimsNETConnect`](../functions/LimsNETConnect.md), or [`LimsNETTypeOf`](../functions/LimsNETTypeOf.md).

## Members

| Member | Kind | Returns | Description |
|---|---|---|---|
| `GetProperty(sName)` | Method | `any` | Reads a public field or property by name. |
| `SetProperty(sName, vValue)` | Method | `none` | Writes an existing public field or property by name. |
| `IsProperty(sName)` | Method | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when a public field or property with the given name exists. |
| `Invoke(sName, [aArgs])` | Method | `any` | Calls a public method by name and returns its result. |
| `IsEmpty()` | Method | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) only when the wrapped reference is null. |
| [`ToJson()`](../functions/ToJson.md) | Method | [`string`](string.md) | Serializes the wrapped value to JSON when it is a `DataSet`. Other wrapped values raise an error. |

## Indexing

Direct indexing is available only when the wrapped value exposes an indexer shape that `netobject` understands.

| Wrapped value | Read access | Write access |
|---|---|---|
| `DataRow` | By column name or numeric column index | Yes |
| `DataRowCollection` | By numeric row index | No documented direct write form |
| `DataTableCollection` | By numeric index or table name | No documented direct write form |
| `DataColumnCollection` | By numeric index or column name | No documented direct write form |
| Arrays | By numeric index | Yes |
| Other values with an `Item` indexer | Depends on the wrapped type | Depends on the wrapped type |

Numeric indexing follows the wrapped value's own indexer behavior. `netobject` does not normalize every wrapped collection to SSL array semantics.

## Notes for daily SSL work

!!! success "Do"
    - Call `IsEmpty()` and `IsProperty()` before accessing a property on a `netobject` whose wrapped value may be null or whose schema may vary.
    - Use `SetProperty()` only for members that already exist on the wrapped value.
    - Use [`ToJson()`](../functions/ToJson.md) only when you know the wrapped value is a `DataSet`.

!!! failure "Don't"
    - Call `GetProperty()` or `Invoke()` blindly when the value might be null or the member might not exist. Null wrapped values raise a null-reference error, and invalid member names raise an error.
    - Assume numeric indexing is always SSL-style 1-based. Wrapped collections use their own indexing behavior.
    - Treat `netobject` like a dynamic SSL object that supports [`AddProperty()`](../functions/AddProperty.md). It cannot add new members to the wrapped value.

## Errors and edge cases

- `GetProperty()`, `SetProperty()`, `IsProperty()`, and `Invoke()` raise a null-reference error when the wrapped value is null and the target member is not static.
- Invalid property names raise an error from `GetProperty()` or `SetProperty()`. Invalid method names raise an error from `Invoke()`.
- `IsProperty()` checks fields and properties, not methods.
- `IsEmpty()` only checks whether the wrapped reference is null. It does not inspect row counts, collection lengths, or other content.

## Examples

### Reading a property and invoking a method

Creates a `StringBuilder` wrapping `"LAB"`, reads its `Length` property (3), appends `"-01"`, and returns the resulting string `"LAB-01"`.

```ssl
:PROCEDURE ReadNetObjectProperties;
	:DECLARE oBuilder, bHasLength, nLength, sResult;

	oBuilder := LimsNETConnect("System", "System.Text.StringBuilder", {"LAB"}, .F.);

	bHasLength := oBuilder:IsProperty("Length");

	:IF bHasLength;
		nLength := oBuilder:GetProperty("Length");
		InfoMes("Initial length: " + LimsString(nLength));
	:ENDIF;

	oBuilder:Invoke("Append", {"-01"});
	sResult := oBuilder:Invoke("ToString");

	:RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("ReadNetObjectProperties");
```

### Invoking a static .NET member

Uses [`LimsNETTypeOf`](../functions/LimsNETTypeOf.md) to obtain a `netobject` representing `System.Math`, then calls `Abs(-42)` = 42 and `Max(42, 10)` = 42.

```ssl
:PROCEDURE UseStaticNetType;
	:DECLARE oMath, nAbsolute, nLargest;

	oMath := LimsNETTypeOf("System.Math");

	nAbsolute := oMath:Invoke("Abs", {(0 - 42)});
	nLargest := oMath:Invoke("Max", {nAbsolute, 10});

	:RETURN nLargest;
:ENDPROC;

/* Usage;
DoProc("UseStaticNetType");
```

### Working with indexed collections and ToJson

Builds a `DataSet` with one row, reads a cell value through the `DataRow` indexer by column name, and serializes the dataset to JSON.

```ssl
:PROCEDURE SerializeDataSetNetObject;
	:DECLARE oDataSet, oTable, oColumns, oRows, oTables, oRow, sSampleID, sJson;

	oDataSet := LimsNETConnect("System.Data", "System.Data.DataSet", {}, .F.);
	oTable := LimsNETConnect("System.Data", "System.Data.DataTable", {"sample"}, .F.);

	oColumns := oTable:GetProperty("Columns");
	oColumns:Invoke("Add", {"sample_id"});
	oColumns:Invoke("Add", {"status"});

	oRows := oTable:GetProperty("Rows");
	oRows:Invoke("Add", {{"S-1001", "Logged"}});

	oTables := oDataSet:GetProperty("Tables");
	oTables:Invoke("Add", {oTable});

	oRow := oRows[1];
	sSampleID := oRow["sample_id"];
	sJson := oDataSet:ToJson();

	InfoMes("Sample: " + sSampleID);

	:RETURN sJson;
:ENDPROC;

/* Usage;
DoProc("SerializeDataSetNetObject");
```

## Related elements

- [`MakeNETObject`](../functions/MakeNETObject.md)
- [`LimsNETConnect`](../functions/LimsNETConnect.md)
- [`LimsNETTypeOf`](../functions/LimsNETTypeOf.md)
- [`object`](object.md)
