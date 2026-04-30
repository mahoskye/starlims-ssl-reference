---
title: "Classes"
summary: "29 classes providing structured data access, document management, and system services."
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Classes

**29 classes** providing structured data access, document management, and system services.

| Class | Description |
|-------|-------------|
| [AzureStorage](AzureStorage.md) | Provides unified access to Azure Table Storage and Azure Blob Storage for storing structured data and files. |
| [BatchSupport](BatchSupport.md) | Provides runtime monitoring of batch processes and system resource usage. |
| [CDataColumn](CDataColumn.md) | Provides structured metadata for a single data table column, enabling inspection of name, type, data characteristics, and primary key participation. |
| [CDataColumns](CDataColumns.md) | Provides indexed access to metadata for all columns in a data table, enabling inspection and manipulation of column definitions. |
| [CDataField](CDataField.md) | Encapsulates access to a single cell value in a data row, enabling safe retrieval, assignment, and conversion between types for robust SSL data workflows. |
| [CDataRow](CDataRow.md) | Enables direct access and manipulation of a table row’s fields and primary keys within a CDataTable, supporting array-based and field-name lookups. |
| [CDataTable](CDataTable.md) | Provides data table structure and operations for loading, editing, serializing, and persisting tabular data in SSL, with built-in support for row/column navigation, SQL, and XML. |
| [Email](Email.md) | Sends, saves, and manages email messages with configurable recipients, attachments, encryption, and SMTP options. |
| [EnterpriseExporter](EnterpriseExporter.md) | Provides tools for exporting enterprise and system tables to a specified file path, supporting advanced export options and error handling. |
| [FtpsClient](FtpsClient.md) | Facilitates secure, scriptable file transfers and directory management over FTPS with proxy and TLS support. |
| [HtmlConverter](HtmlConverter.md) | Converts XFD form XML to HTML form XML and exposes the conversion log. |
| [PatcherSupport](PatcherSupport.md) | Enables dictionary-level data patching and synchronization by providing methods to compare, extract, and interact with STARLIMS system data tables. |
| [PdfSupport](PdfSupport.md) | Provides methods to create, modify, secure, and print PDF documents with fine-grained page and permission controls. |
| [RegSetup](RegSetup.md) | Provides methods to open, query, and close registry keys to interact with the Windows registry from SSL scripts. |
| [SDMS](SDMS.md) | Enables secure document exchange, retrieval, and management operations with an external SDMS system. |
| [SDMSDocUploader](SDMSDocUploader.md) | Enables automated upload, association, and revision management of files and metadata in SDMS workflows. |
| [SQLConnection](SQLConnection.md) | Exposes metadata for a configured database connection returned by `GetConnectionByName`. |
| [SSLBaseDictionary](SSLBaseDictionary.md) | Enables storage and management of key-value pairs with methods for adding, retrieving, updating, and removing entries. |
| [SSLCodeProvider](SSLCodeProvider.md) | Provides methods to compile SSL server scripts and data sources, returning detailed error information for validation and debugging. |
| [SSLDataset](SSLDataset.md) | Enables conversion between dataset structures and commonly used representations such as arrays and XML for data integration and manipulation workflows. |
| [SSLError](SSLError.md) | Captures and encapsulates errors from SSL runtime operations, providing detailed error messages, error codes, and context for diagnostic and handling purposes. |
| [SSLExpando](SSLExpando.md) | Provides a flexible, dynamic object that allows adding, retrieving, and serializing arbitrary properties with XML support. |
| [SSLIntDictionary](SSLIntDictionary.md) | Provides a dictionary for associating values with integer keys, including efficient lookup and management operations. |
| [SSLRegex](SSLRegex.md) | Enables pattern-based matching and validation of strings using regular expressions with optional case sensitivity control. |
| [SSLSQLError](SSLSQLError.md) | Provides a structured representation of a database error resulting from an SQL operation, supplying standardized details such as the error message, SQL state, stack trace, code, and affected statement. |
| [SSLStringDictionary](SSLStringDictionary.md) | Provides a key-value storage for strings with support for case sensitivity and flexible value types. |
| [Sequence](Sequence.md) | Manages the creation, configuration, and operation of database-backed numeric sequences for generating unique identifiers. |
| [TablesImport](TablesImport.md) | Imports table data from files in a specified folder and returns them as table objects for use in SSL scripts. |
| [WebServices](WebServices.md) | Provides factory methods for quickly creating HTTP and SOAP client objects to perform web requests and service interactions. |
