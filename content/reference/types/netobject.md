---
title: "netobject"
summary: "Provides dynamic access to external objects for property access, method invocation, and selected interop scenarios in SSL."
id: ssl.type.netobject
element_type: type
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# netobject

## What it is

Provides dynamic access to external objects for property access, method invocation, and selected interop scenarios in SSL.

The `netobject` type represents a value returned by SSL's .NET interop helpers such as [`MakeNETObject`](../functions/MakeNETObject.md), [`LimsNETConnect`](../functions/LimsNETConnect.md), and [`LimsNETTypeOf`](../functions/LimsNETTypeOf.md). Use it when you need to work with a .NET value from SSL code.

You work with a `netobject` through its native .NET members, called with `:`: `oBuilder:Append("-01")`, `oBuilder:ToString()`, `oBuilder:Length`. Returned values come back as ordinary SSL values when possible; .NET values that still need interop access remain `netobject` values. Members can be chained, as in `oTable:Rows:Count` or `oDs:Tables[0]:Rows[0]["sample_id"]`.

`netobject` has no SSL-defined members. `GetProperty()`, `SetProperty()`, `IsProperty()`, `Invoke()`, `IsEmpty()` and `ToJson()` all raise `Run-time error: Invalid method: …` on a `netobject`, in any letter case. Native member names are case-sensitive: see [Member names and case](../../guides/native-members.md#member-names-and-case). The same native members are reachable on ordinary SSL values, such as `sValue:ToUpper()` or `aValues:Length`; see [Native Members on SSL Values](../../guides/native-members.md).

## Creating values

`netobject` values cannot be created with a literal. They are returned by interop functions.

```ssl
oBuilder := LimsNETConnect("System", "System.Text.StringBuilder", {"LAB"}, .F.);
oMath := LimsNETConnect(, "System.Math",, .T.);
```

- **Runtime type:** `OBJECT`
- **Literal syntax:** None. Use [`MakeNETObject`](../functions/MakeNETObject.md), [`LimsNETConnect`](../functions/LimsNETConnect.md), or [`LimsNETTypeOf`](../functions/LimsNETTypeOf.md).

## Members

A `netobject` has no SSL-defined members; use the wrapped .NET type's own members. For common needs:

| Task | Use |
|---|---|
| Read a property | `oNet:PropertyName`, e.g. `oBuilder:Length` |
| Call a method | `oNet:MethodName(args)`, e.g. `oBuilder:Append("-01")` |
| Call a static method | Connect to the type as static with [`LimsNETConnect`](../functions/LimsNETConnect.md)`(, "System.Math",, .T.)`, then `oMath:Abs(-42)` |
| Serialize a `DataSet` to JSON | [`ToJson`](../functions/ToJson.md)`(oDataSet)` |
| Check the type | [`LimsTypeEx`](../functions/LimsTypeEx.md) returns `"OBJECT"` |

A type object from [`LimsNETTypeOf`](../functions/LimsNETTypeOf.md) does not call the type's static methods: `LimsNETTypeOf("System.Math"):Abs(-42)` raises `Invalid method: Abs`. Use the static form of [`LimsNETConnect`](../functions/LimsNETConnect.md) for that.

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

Numeric indexing follows the wrapped value's own indexer, which for .NET collections is **0-based**: `oTable:Rows[0]` is the first row, and `oTable:Rows[1]` on a one-row table raises `There is no row at position 1.`

## Notes for daily SSL work

!!! success "Do"
    - Call native members by their exact .NET names and casing, such as `oBuilder:Append("-01")` and `oTable:Rows:Count`.
    - Index .NET collections from `0`: `oTable:Rows[0]`, `oDs:Tables[0]`.
    - Use the static form of [`LimsNETConnect`](../functions/LimsNETConnect.md) to call static methods such as `System.Math.Abs`.

!!! failure "Don't"
    - Call `GetProperty()`, `SetProperty()`, `IsProperty()`, `Invoke()`, `IsEmpty()` or `ToJson()` on a `netobject`. They raise `Invalid method`; use the native members and the [`ToJson`](../functions/ToJson.md) function instead.
    - Assume numeric indexing is SSL-style 1-based. .NET collections start at `0`.
    - Treat `netobject` like a dynamic SSL object that supports [`AddProperty()`](../functions/AddProperty.md). It cannot add new members to the wrapped value.

## Errors and edge cases

- Calling a member that the wrapped type doesn't have, or that doesn't accept the arguments given, raises `Run-time error: Invalid method: …` (or `Invalid property: …` for a property).
- A member name in the wrong case raises the same errors.
- An index past the end of a .NET collection raises the collection's own error, such as `There is no row at position 1.`

## Examples

### Reading a property and calling a method

Creates a `StringBuilder` wrapping `"LAB"`, reads its `Length` property, appends `"-01"`, and returns the resulting string.

```ssl
:PROCEDURE ReadNetObjectProperties;
	:DECLARE oBuilder, nLength, sResult;

	oBuilder := LimsNETConnect("System", "System.Text.StringBuilder", {"LAB"}, .F.);

	nLength := oBuilder:Length;
	InfoMes("Initial length: " + LimsString(nLength));

	oBuilder:Append("-01");
	sResult := oBuilder:ToString();

	:RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("ReadNetObjectProperties");
```

`InfoMes` logs `Initial length: 3`, and the procedure returns `"LAB-01"`.

### Calling a static .NET method

Connects to `System.Math` as a static type with [`LimsNETConnect`](../functions/LimsNETConnect.md), then calls `Abs(-42)`, which returns `42`.

```ssl
:PROCEDURE UseStaticNetType;
	:DECLARE oMath, nAbsolute;

	oMath := LimsNETConnect(, "System.Math",, .T.);

	nAbsolute := oMath:Abs(-42);

	:RETURN nAbsolute;
:ENDPROC;

/* Usage;
DoProc("UseStaticNetType");
```

### Building a DataSet and serializing it with ToJson

Builds a `DataSet` with one row through chained native members, reads a cell through the `DataRow` indexer by column name (rows are 0-based), and serializes the dataset with the [`ToJson`](../functions/ToJson.md) function.

```ssl
:PROCEDURE SerializeDataSetNetObject;
	:DECLARE oDataSet, oTable, sSampleID, sJson;

	oDataSet := LimsNETConnect("System.Data", "System.Data.DataSet", {}, .F.);
	oTable := LimsNETConnect("System.Data", "System.Data.DataTable", {"sample"}, .F.);

	oTable:Columns:Add("sample_id");
	oTable:Columns:Add("status");
	oTable:Rows:Add({"S-1001", "Logged"});
	oDataSet:Tables:Add(oTable);

	sSampleID := oTable:Rows[0]["sample_id"];
	sJson := ToJson(oDataSet);

	InfoMes("Sample: " + sSampleID);

	:RETURN sJson;
:ENDPROC;

/* Usage;
DoProc("SerializeDataSetNetObject");
```

`InfoMes` logs `Sample: S-1001`. The returned JSON lists the dataset's tables, each with its `TableName`, `Columns` (name, data type and flags), `PrimaryKey` and `Rows`:

```text
{
	"Tables": [
		{
			"TableName": "sample",
			"Columns": [
				{
					"ColumnName": "sample_id",
					"DataType": "string",
					"AllowDBNull": true,
					"ReadOnly": false,
					"Unique": false
				},
				{
					"ColumnName": "status",
					"DataType": "string",
					"AllowDBNull": true,
					"ReadOnly": false,
					"Unique": false
				}
			],
			"PrimaryKey": [],
			"Rows": [
				{
					"sample_id": "S-1001",
					"status": "Logged"
				}
			]
		}
	],
	"Relations": []
}
```

## Caveats

- Only the wrapped type's native members are available, and a member that doesn't exist, or doesn't accept the arguments given, raises an error such as `Run-time error: Invalid method: Split`. Check a member before relying on it; see [Native Members](../../guides/native-members.md).

## Related elements

- [`MakeNETObject`](../functions/MakeNETObject.md)
- [`LimsNETConnect`](../functions/LimsNETConnect.md)
- [`LimsNETTypeOf`](../functions/LimsNETTypeOf.md)
- [`object`](object.md)
