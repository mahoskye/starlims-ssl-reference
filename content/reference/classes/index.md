---
title: "Classes"
summary: "29 classes providing structured data access, document management, and system services."
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Classes

**29 classes** providing structured data access, document management, and system services, grouped by what they are for.

Every class on this page is **constructed directly** with curly braces — `SSLRegex{"pattern"}`, `Email{}` — and cannot be created with [`CreateUdObject`](../functions/CreateUdObject.md). Objects that you *obtain from a call* rather than construct (the HTTP/SOAP client cluster, endpoint runtime objects) are documented separately under [Obtained Objects](../returns/index.md).

## Tabular data and datasets

Load, inspect, and edit tabular data. A [CDataTable](CDataTable.md) owns rows, columns, and fields — you construct the table and reach the parts through it.

| Class | Description |
|-------|-------------|
| [CDataTable](CDataTable.md) | Provides an in-memory table object for working with rows, columns, XML, and database persistence from SSL. |
| [CDataRow](CDataRow.md) | Represents one row in a CDataTable. |
| [CDataColumns](CDataColumns.md) | Provides access to the column definitions of a CDataTable. |
| [CDataColumn](CDataColumn.md) | Provides metadata for a single column in a CDataTable. |
| [CDataField](CDataField.md) | Represents one field in a CDataRow. |
| [SSLDataset](SSLDataset.md) | Represents dataset results so SSL code can work with query output as an object, convert the first table to an array, export XML, or pass the dataset handle to APIs that expect one. |
| [TablesImport](TablesImport.md) | Loads one imported table at a time from a folder structure and returns it as a CDataTable. |

## Dictionaries and dynamic objects

Key-value stores with different key types, plus the dynamic property-bag object that [FromJson](../functions/FromJson.md) and [CreateUdObject](../functions/CreateUdObject.md) produce.

| Class | Description |
|-------|-------------|
| [SSLBaseDictionary](SSLBaseDictionary.md) | Provides the shared dictionary surface used by SSL dictionary classes such as SSLStringDictionary{} and SSLIntDictionary{}. |
| [SSLStringDictionary](SSLStringDictionary.md) | Stores values by string key. |
| [SSLIntDictionary](SSLIntDictionary.md) | Stores values by whole-number keys. |
| [SSLExpando](SSLExpando.md) | SSLExpando is a built-in object class for storing named values whose shape is decided at runtime. |

## Documents and storage

Create and manage documents and files in external storage systems.

| Class | Description |
|-------|-------------|
| [PdfSupport](PdfSupport.md) | Provides methods to create, modify, secure, save, and print PDF documents. |
| [SDMS](SDMS.md) | Interacts with an external SDMS server to download documents, download Unified XML templates, create an SDMSDocUploader, and generate password hashes for SDMS authentication. |
| [SDMSDocUploader](SDMSDocUploader.md) | Uploads files into SDMS, attaches uploads to workflow steps, and checks in document revisions. |
| [AzureStorage](AzureStorage.md) | Provides SSL access to Azure Table Storage and Azure Blob Storage through one class. |
| [EnterpriseExporter](EnterpriseExporter.md) | Exports tables into a destination folder. |

## Communication

Send email, transfer files, and create web-service clients. The HTTP and SOAP client/response objects that [WebServices](WebServices.md) creates are documented under [Obtained Objects](../returns/index.md).

| Class | Description |
|-------|-------------|
| [Email](Email.md) | Composes, loads, saves, sends, or queues email messages with attachments and optional signing or encryption. |
| [FtpsClient](FtpsClient.md) | Transfers files and manages directories on an FTPS server. |
| [WebServices](WebServices.md) | Creates client objects for outbound HTTP and SOAP integrations. |

## Errors and diagnostics

Structured error objects. In practice these usually arrive from [GetLastSSLError](../functions/GetLastSSLError.md) and SQL-error accessors rather than being constructed.

| Class | Description |
|-------|-------------|
| [SSLError](SSLError.md) | Represents an SSL error and exposes its message, location, code, formatted diagnostic text, and nested SSL error details. |
| [SSLSQLError](SSLSQLError.md) | Represents the SQL-specific error object returned after a database failure. |

## Text and identifiers

Pattern matching and unique-identifier generation.

| Class | Description |
|-------|-------------|
| [SSLRegex](SSLRegex.md) | Matches SSL strings against a stored regular expression pattern. |
| [Sequence](Sequence.md) | Creates and manages a database sequence for a table field on Oracle or SQL Server. |

## System and platform

Interact with the STARLIMS platform itself — batch monitoring, the dictionary, the Windows registry, connection metadata, script compilation, and form conversion.

| Class | Description |
|-------|-------------|
| [BatchSupport](BatchSupport.md) | Provides batch-status checks and memory usage information for the current SSL process. |
| [PatcherSupport](PatcherSupport.md) | Provides helper methods for collecting package-style dictionary metadata, connecting to another STARLIMS system, and comparing one collected result table to another. |
| [RegSetup](RegSetup.md) | Provides access to Windows registry values under HKEY_LOCAL_MACHINE. |
| [SQLConnection](SQLConnection.md) | Represents a configured database connection returned by GetConnectionByName. |
| [SSLCodeProvider](SSLCodeProvider.md) | Compiles published server scripts and data sources and returns a list of compilation errors. |
| [HtmlConverter](HtmlConverter.md) | Converts XFD form XML into HTML form XML and exposes the most recent conversion log. |
