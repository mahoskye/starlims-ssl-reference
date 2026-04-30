---
title: "AzureStorage"
summary: "Provides SSL access to Azure Table Storage and Azure Blob Storage through one class."
id: ssl.class.azurestorage
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AzureStorage

Provides SSL access to Azure Table Storage and Azure Blob Storage through one class.

`AzureStorage` lets an SSL script work with Azure tables and blobs after you create the object with either a configured Azure connection or explicit account credentials. The class exposes table operations for creating tables, inserting entities, selecting entities, updating entities, and deleting entities. It also exposes blob operations for creating containers, uploading files, downloading blobs to local files, deleting blobs, and reading blob contents as text. Create and delete operations are idempotent for existing or missing tables and containers, `SelectEntity` returns [`NIL`](../literals/nil.md) when the requested entity is not found, `SelectEntities` returns an array of matching entities, and `UpdateEntity` returns [`.T.`](../literals/true.md) on success or [`.F.`](../literals/false.md) when the target entity does not exist.

## When to use

- When you need to store structured records in Azure Table Storage from SSL.
- When you need to upload, download, or delete files in Azure Blob Storage.
- When your Azure connection is already configured in LIMS and you want to reuse that configuration.
- When you need one API surface for both table and blob operations.

## Constructors

### `AzureStorage{}`

Uses the first configured Azure connection available to the application.

**Raises:**

- **When no Azure connection is configured:** `Azure connection error: Could not find a connection string that has provider name = 'MicrosoftAzure'.`

### `AzureStorage{sConnectionName}`

Uses the named Azure connection from the application configuration.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sConnectionName` | [string](../types/string.md) | yes | Name of the configured Azure connection to use. |

**Raises:**

- **When the named connection does not exist:** `Azure connection error: Could not find Azure connection string with name = '<sConnectionName>'.`
- **When the configured connection string is missing required account settings:** A runtime error indicating the missing token such as `Account Name` or `Account Key`.

### `AzureStorage{sAccountName, sAccountKey}`

Creates the client from an explicit Azure account name and key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sAccountName` | [string](../types/string.md) | yes | Azure storage account name. |
| `sAccountKey` | [string](../types/string.md) | yes | Azure storage account key. |

This constructor uses HTTP.

### `AzureStorage{sAccountName, sAccountKey, bUseHttp}`

Creates the client from an explicit Azure account name and key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sAccountName` | [string](../types/string.md) | yes | Azure storage account name. |
| `sAccountKey` | [string](../types/string.md) | yes | Azure storage account key. |
| `bUseHttp` | [boolean](../types/boolean.md) | no | Despite the parameter name, passing [`.T.`](../literals/true.md) uses HTTPS and [`.F.`](../literals/false.md) uses HTTP. |

## Methods Summary

| Name | Returns | Description |
|------|---------|-------------|
| `CreateTable` | none | Creates a table if needed. |
| `DeleteTable` | none | Deletes a table if it exists. |
| `InsertEntity` | none | Inserts one table entity. |
| `InsertEntities` | none | Inserts multiple table entities in batches. |
| `SelectEntity` | [object](../types/object.md) | Returns one entity or [`NIL`](../literals/nil.md) when not found. |
| `SelectEntities` | [array](../types/array.md) | Returns entities that match an equality-based filter. |
| `DeleteEntity` | none | Deletes one entity if it exists. |
| `DeleteEntities` | none | Deletes multiple entities in batches. |
| `UpdateEntity` | [boolean](../types/boolean.md) | Updates one entity and reports success. |
| `CreateContainer` | none | Creates a blob container if needed. |
| `DeleteContainer` | none | Deletes a blob container if it exists. |
| `PutBlob` | none | Uploads a local file as a blob. |
| `GetBlob` | [string](../types/string.md) | Downloads a blob and returns the local file path. |
| `DeleteBlob` | none | Deletes a blob. |
| `ReadBlobAsText` | [string](../types/string.md) | Returns blob contents as text. |

## Methods

### `CreateTable`

Creates a table when it does not already exist.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTableName` | [string](../types/string.md) | yes | Azure table name. It must start with a letter, contain only letters and numbers, and be 3 to 63 characters long. |

**Returns:** none — Returns nothing.

**Raises:**

- **When `sTableName` is invalid:** `Invalid table name.` followed by the Azure table naming rules.
- **When Azure returns an unexpected success status:** A runtime error describing the unexpected HTTP status.

If the table already exists, the method completes without error.

### `DeleteTable`

Deletes a table when it exists.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTableName` | [string](../types/string.md) | yes | Azure table name. |

**Returns:** none — Returns nothing.

**Raises:**

- **When Azure returns an unexpected success status:** A runtime error describing the unexpected HTTP status.

If the table does not exist, the method completes without error.

### `InsertEntity`

Inserts one entity into a table.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTableName` | [string](../types/string.md) | yes | Azure table name. |
| `oEntity` | [object](../types/object.md) | yes | Entity object. It must include `PartitionKey` and `RowKey` properties before insertion. |

**Returns:** none — Returns nothing.

**Raises:**

- **When `oEntity` does not contain `PartitionKey`:** `Cannot insert an Azure table entity without a 'PartitionKey' property.`
- **When `oEntity` does not contain `RowKey`:** `Cannot insert an Azure table entity without a 'RowKey' property.`
- **When Azure returns an unexpected success status:** A runtime error describing the unexpected HTTP status.

### `InsertEntities`

Inserts multiple entities into a table in batches.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTableName` | [string](../types/string.md) | yes | Azure table name. |
| `aEntities` | [array](../types/array.md) | yes | Array of entity objects. Each entity must include `PartitionKey` and `RowKey`. |

**Returns:** none — Returns nothing.

**Raises:**

- **When any entity is missing `PartitionKey`:** `Cannot insert an Azure table entity without a 'PartitionKey' property.`
- **When any entity is missing `RowKey`:** `Cannot insert an Azure table entity without a 'RowKey' property.`
- **When Azure returns an unexpected batch status:** A runtime error describing the unexpected HTTP status.

If `aEntities` is [`NIL`](../literals/nil.md) or empty, the method does nothing.

### `SelectEntity`

Returns one entity identified by partition key and row key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTableName` | [string](../types/string.md) | yes | Azure table name. |
| `sPartitionKey` | [string](../types/string.md) | yes | Partition key value. |
| `sRowKey` | [string](../types/string.md) | yes | Row key value. |

**Returns:** [object](../types/object.md) — The matching entity, or [`NIL`](../literals/nil.md) when Azure returns `404 Not Found`.

### `SelectEntities`

Returns all entities that match an equality-based attribute filter.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTableName` | [string](../types/string.md) | yes | Azure table name. |
| `oAttributes` | [object](../types/object.md) | yes | Filter object. String, number, date, and boolean properties become equality conditions. If a property value is an array, each element becomes an OR condition for that property. |

**Returns:** [array](../types/array.md) — Array of matching entities. If Azure returns `404 Not Found`, the method returns an empty array rather than [`NIL`](../literals/nil.md).

**Raises:**

- **When a filter property uses an unsupported value type:** `Data type for attribute '<name>' is not supported. Only the following data types are supported with Azure queries: string, number, date, bool.`

### `DeleteEntity`

Deletes one entity identified by partition key and row key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTableName` | [string](../types/string.md) | yes | Azure table name. |
| `sPartitionKey` | [string](../types/string.md) | yes | Partition key value. |
| `sRowKey` | [string](../types/string.md) | yes | Row key value. |

**Returns:** none — Returns nothing.

If the entity does not exist, the method completes without error.

### `DeleteEntities`

Deletes multiple entities in batches.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTableName` | [string](../types/string.md) | yes | Azure table name. |
| `aEntities` | [array](../types/array.md) | yes | Array of key pairs. Each element must be an array whose first value is the partition key and second value is the row key. |

**Returns:** none — Returns nothing.

**Raises:**

- **When Azure returns an unexpected batch status:** A runtime error describing the unexpected HTTP status.

If `aEntities` is [`NIL`](../literals/nil.md) or empty, the method does nothing.

### `UpdateEntity`

Updates one existing entity identified by its `PartitionKey` and `RowKey`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTableName` | [string](../types/string.md) | yes | Azure table name. |
| `oEntity` | [object](../types/object.md) | yes | Entity object to write back. It must include non-empty string `PartitionKey` and `RowKey` properties. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the update succeeds, or [`.F.`](../literals/false.md) when the target entity does not exist.

**Raises:**

- **When `oEntity` does not contain `PartitionKey`:** `Cannot update an Azure table entity without a 'PartitionKey' property.`
- **When `oEntity` does not contain `RowKey`:** `Cannot update an Azure table entity without a 'RowKey' property.`
- **When `PartitionKey` is not a non-empty string:** `Update Azure table entity: 'PartitionKey' must be a non-null string.`
- **When `RowKey` is not a non-empty string:** `Update Azure table entity: 'RowKey' must be a non-null string.`
- **When Azure returns an unexpected success status:** A runtime error describing the unexpected HTTP status.

### `CreateContainer`

Creates a blob container when it does not already exist.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sContainerName` | [string](../types/string.md) | yes | Blob container name. It must be lowercase, may include numbers and dashes, must be 3 to 63 characters long, and cannot contain consecutive dashes. |

**Returns:** none — Returns nothing.

**Raises:**

- **When `sContainerName` is invalid:** `Invalid container name.` followed by the container naming rules.
- **When Azure returns an unexpected success status:** A runtime error describing the unexpected HTTP status.

If the container already exists, the method completes without error.

### `DeleteContainer`

Deletes a blob container when it exists.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sContainerName` | [string](../types/string.md) | yes | Blob container name. |

**Returns:** none — Returns nothing.

**Raises:**

- **When Azure returns an unexpected success status:** A runtime error describing the unexpected HTTP status.

If the container does not exist, the method completes without error.

### `PutBlob`

Uploads a local file as a blob.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sContainerName` | [string](../types/string.md) | yes | Blob container name. |
| `sLocalPath` | [string](../types/string.md) | yes | Local file path to upload. |
| `sBlobName` | [string](../types/string.md) | no | Blob name. When omitted or [`NIL`](../literals/nil.md), the method uses the base file name from `sLocalPath`. |

**Returns:** none — Returns nothing.

**Raises:**

- **When `sLocalPath` does not exist:** `File does not exist: <sLocalPath>`
- **When the file is larger than 64 MB:** `Not implemented for files bigger than 64 MB: <sLocalPath>`
- **When `sBlobName` is empty, longer than 1024 characters, or ends with `.` or [`/`](../operators/divide.md):** `Invalid blob name. Blob names cannot end with a dot (.) or a forward slash (/). A blob name must be between 1 and 1024 characters long.`
- **When Azure returns an unexpected success status:** A runtime error describing the unexpected HTTP status.

### `GetBlob`

Downloads a blob to a local file and returns the destination path.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sContainerName` | [string](../types/string.md) | yes | Blob container name. |
| `sBlobName` | [string](../types/string.md) | yes | Blob name. |
| `sDestPath` | [string](../types/string.md) | no | Destination file path. When omitted or [`NIL`](../literals/nil.md), the method creates a temporary file path under the application work area. |

**Returns:** [string](../types/string.md) — The path of the downloaded local file.

### `DeleteBlob`

Deletes a blob.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sContainerName` | [string](../types/string.md) | yes | Blob container name. |
| `sBlobName` | [string](../types/string.md) | yes | Blob name. |

**Returns:** none — Returns nothing.

### `ReadBlobAsText`

Downloads a blob to a temporary file, reads that file as text, deletes the temporary file, and returns the text.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sContainerName` | [string](../types/string.md) | yes | Blob container name. |
| `sBlobName` | [string](../types/string.md) | yes | Blob name. |

**Returns:** [string](../types/string.md) — Blob contents read as text.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Use a configured connection name when Azure credentials are managed centrally in LIMS.
    - Include `PartitionKey` and `RowKey` on every table entity you insert or update.
    - Treat `SelectEntity()` returning [`NIL`](../literals/nil.md) as a normal not-found result.
    - Check the boolean result from `UpdateEntity()` to detect a missing target row.
    - Use `GetBlob()` when you need a local file and `ReadBlobAsText()` when you need the blob contents as text.

!!! failure "Don't"
    - Assume the credential constructors default to HTTPS. The two-argument constructor uses HTTP, and the three-argument constructor only uses HTTPS when `bUseHttp` is [`.T.`](../literals/true.md).
    - Build `SelectEntities()` filters with comparison operators such as less-than or greater-than.
      The public API only builds equality filters from the properties you supply.
    - Expect `GetBlob()` to return blob contents. It returns a file path to the downloaded blob.
    - Omit `PartitionKey` or `RowKey` when inserting or updating entities. Those calls fail before the request is sent.

## Caveats

- The parameterless constructor requires at least one Azure connection configured for the application.
- A named connection must include the Azure account settings the class expects, including account name and account key.
- The three-argument constructor's `bUseHttp` parameter name does not match the observed behavior. Passing [`.T.`](../literals/true.md) enables HTTPS and [`.F.`](../literals/false.md) uses HTTP.
- `CreateTable()` and `CreateContainer()` succeed silently when the target already exists.
- `DeleteTable()`, `DeleteEntity()`, and `DeleteContainer()` succeed silently when the target does not exist.
- `SelectEntities()` always returns an array object from SSL, even when Azure reports no matches.
- `PutBlob()` reads the full file into memory and rejects files larger than 64 MB.
- `ReadBlobAsText()` is intended for text content. Use `GetBlob()` for binary files or when you need a saved local copy.

## Examples

### Create a table and insert one entity

Create a table if needed, build a single entity, and insert it.

```ssl
:PROCEDURE CreateCustomerRecord;
	:DECLARE oAzure, oCustomer, sTableName;

	sTableName := "Customers";
	oAzure := AzureStorage{"AzureStorage"};

	oAzure:CreateTable(sTableName);

	oCustomer := CreateLocal();
	oCustomer:PartitionKey := "CUSTOMER";
	oCustomer:RowKey := "CUST001";
	oCustomer:CompanyName := "Acme Corp";
	oCustomer:ContactName := "Jane Smith";
	oCustomer:Phone := "555-1234";

	oAzure:InsertEntity(sTableName, oCustomer);

	UsrMes("Inserted customer " + oCustomer:RowKey 
			+ " into " + sTableName);
:ENDPROC;

/* Usage;
DoProc("CreateCustomerRecord");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Inserted customer CUST001 into Customers
```

### Query matching entities and update one

Use an equality-based filter with `SelectEntities()`, then update one returned entity.

```ssl
:PROCEDURE RestockProducts;
	:DECLARE oAzure, oFilter, aProducts, oProduct;
	:DECLARE sTableName, bUpdated;

	sTableName := "ProductInventory";
	oAzure := AzureStorage{"InventoryConnection"};

	oFilter := CreateLocal();
	oFilter:Status := "LOW";
	oFilter:Warehouse := {"MAIN", "BACKUP"};

	aProducts := oAzure:SelectEntities(sTableName, oFilter);

	:IF ALen(aProducts) == 0;
		UsrMes("No low-stock products matched the filter");
		:RETURN .F.;
	:ENDIF;

	oProduct := aProducts[1];
	oProduct:Status := "RESTOCKED";
	oProduct:RestockNote := "Updated from SSL example";

	bUpdated := oAzure:UpdateEntity(sTableName, oProduct);

	:IF bUpdated;
		UsrMes("Updated product " + oProduct:RowKey);
	:ELSE;
		UsrMes("The selected product was no longer available for update");
	:ENDIF;

	:RETURN bUpdated;
:ENDPROC;

/* Usage;
DoProc("RestockProducts");
```

### Upload files, download a copy, and read a blob as text

Manage a blob container, upload files, then use both blob retrieval patterns.

```ssl
:PROCEDURE ManageDocumentStorage;
	:DECLARE oAzure, aFiles, sContainerName, sLocalPath;
	:DECLARE sBlobName, sDownloadedPath, sBlobText, oErr, nIndex;

	oAzure := AzureStorage{"myaccount", "mysecretkey", .T.};
	sContainerName := "documents";

	oAzure:CreateContainer(sContainerName);

	aFiles := {"report.txt", "invoice.txt"};

	:FOR nIndex := 1 :TO ALen(aFiles);
		sLocalPath := "C:\\Temp\\" + aFiles[nIndex];
		sBlobName := aFiles[nIndex];

		:TRY;
			oAzure:PutBlob(sContainerName, sLocalPath, sBlobName);
			UsrMes("Uploaded " + sBlobName);
			/* Displays the uploaded blob name;
		:CATCH;
			oErr := GetLastSSLError();
			ErrorMes(
				"UPLOAD ERROR",
				"Upload failed for " + sBlobName + ": " + oErr:Description
			);
			/* Displays upload failure details;
		:ENDTRY;
	:NEXT;

	sDownloadedPath := oAzure:GetBlob(sContainerName, "report.txt");
	UsrMes("Downloaded report to " + sDownloadedPath);
	/* Displays the downloaded file path;

	sBlobText := oAzure:ReadBlobAsText(sContainerName, "invoice.txt");
	UsrMes("Invoice text length: " + LimsString(Len(sBlobText)));
	/* Displays the invoice text length;

	oAzure:DeleteContainer(sContainerName);
:ENDPROC;

/* Usage;
DoProc("ManageDocumentStorage");
```

## Related

- [`CreateLocal`](../functions/CreateLocal.md)
- [`GetLastSSLError`](../functions/GetLastSSLError.md)
- [`SSLExpando`](SSLExpando.md)
- [`SSLError`](SSLError.md)
