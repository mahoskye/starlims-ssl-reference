---
title: "Functions"
summary: "330 built-in functions organized by category."
starlims:
  applies_to: [11, 12]
  verified_against: [11]
---

# Functions

**330 built-in functions** organized by category.

## Categories

- [Array](#array) (15)
- [Database](#database) (54)
    - [SQL Queries](#sql-queries) (11)
    - [Transactions](#transactions) (4)
    - [Connections](#connections) (10)
    - [Schema](#schema) (5)
    - [SQL Utilities](#sql-utilities) (19)
    - [Dataset Builders](#dataset-builders) (5)
- [Date & Time](#date-time) (39)
- [Documentum](#documentum) (47)
    - [Auth](#auth) (3)
    - [Documents](#documents) (12)
    - [Folders & Cabinets](#folders-cabinets) (6)
    - [Users & Groups](#users-groups) (9)
    - [Workflows](#workflows) (12)
    - [Search](#search) (3)
    - [Documentum Errors](#documentum-errors) (2)
- [Email](#email) (4)
- [Execution & Dynamic Dispatch](#execution-dynamic-dispatch) (10)
- [FTP](#ftp) (12)
- [File System](#file-system) (19)
- [Inline Code](#inline-code) (5)
- [Messaging & Errors](#messaging-errors) (8)
- [Numeric & Math](#numeric-math) (24)
- [Object & Interop](#object-interop) (12)
- [Security](#security) (12)
- [String](#string) (35)
- [System & Batch](#system-batch) (6)
- [Type Conversion](#type-conversion) (16)
- [Variable & Session Management](#variable-session-management) (12)

## Array

| Function | Description |
|----------|-------------|
| [AAdd](AAdd.md) | Appends an element to the end of an array and returns the appended element. |
| [AEval](AEval.md) | Evaluates a code block for each array element and returns the same array. |
| [AEvalA](AEvalA.md) | Evaluates a code block for each selected array element and writes the result back to the same array. |
| [AFill](AFill.md) | Fills an array element range with the same value and returns the same array. |
| [ALen](ALen.md) | Returns the number of elements in an array. |
| [ArrayCalc](ArrayCalc.md) | Perform a selected array operation by passing an operation code. |
| [ArrayNew](ArrayNew.md) | Creates a new array with up to three dimensions. |
| [AScan](AScan.md) | Returns the index of the first array element that matches a value or condition. |
| [AScanExact](AScanExact.md) | Returns the index of the first array element that matches a value or condition exactly. |
| [BuildArray](BuildArray.md) | Splits text into a one-dimensional array using a literal delimiter. |
| [BuildArray2](BuildArray2.md) | Parses text into a two-dimensional array using separate row and column delimiters. |
| [CompArray](CompArray.md) | Determines whether two arrays are exactly equal. |
| [DelArray](DelArray.md) | Removes an element from an array at a specified one-based index and returns the same array. |
| [ExtractCol](ExtractCol.md) | Extracts one column from a two-dimensional array and returns the extracted values as a new array. |
| [SortArray](SortArray.md) | Sorts an array in place and returns the same array. |

## Database

### SQL Queries

| Function | Description |
|----------|-------------|
| [GetDataSet](GetDataSet.md) | Executes a SQL query on the default database connection and returns the result as an XML dataset string. |
| [GetDataSetEx](GetDataSetEx.md) | Executes a SQL command on a specified connection and returns the result as XML dataset text. |
| [GetNETDataSet](GetNETDataSet.md) | Executes a SQL command and returns the result either as dataset XML or as a netobject wrapping a dataset. |
| [GetSSLDataset](GetSSLDataset.md) | Executes a SQL statement and returns the result as an SSLDataset. |
| [LSearch](LSearch.md) | Returns a single value from a SQL query, or a caller-supplied fallback when the query produces no scalar result. |
| [LSelect](LSelect.md) | Executes a SQL SELECT statement and returns the result as a two-dimensional SSL array. |
| [LSelect1](LSelect1.md) | Executes a parameterized SQL SELECT command and returns the result as an array of rows. |
| [LSelectC](LSelectC.md) | Executes a SQL SELECT statement and returns the result as a two-dimensional SSL array. |
| [RunDS](RunDS.md) | Executes a data source by name or GUID and returns the result in the requested format. |
| [RunSQL](RunSQL.md) | Executes a non-query SQL statement and returns .T. on success. Under default settings, a failed statement raises an error. |
| [SQLExecute](SQLExecute.md) | Executes SQL and returns either query results or a success flag. |

### Transactions

| Function | Description |
|----------|-------------|
| [BeginLimsTransaction](BeginLimsTransaction.md) | Starts a LIMS database transaction on the default connection or on a named connection. |
| [EndLimsTransaction](EndLimsTransaction.md) | Ends a LIMS transaction on the default connection or on a named connection. |
| [GetTransactionsCount](GetTransactionsCount.md) | Returns the number of open database transactions for a specified or default connection. |
| [IsInTransaction](IsInTransaction.md) | Returns .T. if the specified database connection currently has an open transaction. |

### Connections

| Function | Description |
|----------|-------------|
| [GetConnectionByName](GetConnectionByName.md) | Retrieves a database connection object using a specified connection name. |
| [GetConnectionStrings](GetConnectionStrings.md) | Retrieves all configured database connections as a two-dimensional array. |
| [GetDBMSName](GetDBMSName.md) | Returns the DBMS platform name for a configured database connection. |
| [GetDBMSProviderName](GetDBMSProviderName.md) | Returns the uppercase DBMS provider identifier for a named database connection. |
| [GetDefaultConnection](GetDefaultConnection.md) | Returns the current default database connection name. |
| [IsDBConnected](IsDBConnected.md) | Checks whether STARLIMS currently has a database connection available for a given connection name. |
| [LimsSqlConnect](LimsSqlConnect.md) | Registers a configured database connection by connection name. |
| [LimsSqlDisconnect](LimsSqlDisconnect.md) | Closes an active database connection by name and removes it from the session's connection list. |
| [SetDefaultConnection](SetDefaultConnection.md) | Changes the active default database connection name and returns the previous default connection. |
| [SetSqlTimeout](SetSqlTimeout.md) | Sets the SQL command timeout for a database connection and returns the previous timeout value for that same connection. |

### Schema

| Function | Description |
|----------|-------------|
| [GetDSParameters](GetDSParameters.md) | Returns an array of parameter key strings for the named data source. |
| [GetTables](GetTables.md) | Extracts table names from the FROM portion of a SQL SELECT string. |
| [IsTable](IsTable.md) | Checks whether a table exists in a database connection. |
| [IsTableFld](IsTableFld.md) | Checks whether a field exists in a table for a selected database connection. |
| [TableFldLst](TableFldLst.md) | Returns the field names for a table on a selected database connection. |

### SQL Utilities

| Function | Description |
|----------|-------------|
| [AddColDelimiters](AddColDelimiters.md) | Qualify each column in an array as table.column with database-specific identifier delimiters. |
| [AddNameDelimiters](AddNameDelimiters.md) | Wrap a name in database-specific delimiters. |
| [ArrayToTVP](ArrayToTVP.md) | Converts a one-dimensional array into a table-valued parameter object. |
| [BuildStringForIn](BuildStringForIn.md) | Builds a quoted string list for a SQL IN clause from an array. |
| [CreateORMSession](CreateORMSession.md) | Creates the shared ORM session object for the current SSL runtime, or returns the existing one if it has already been created. |
| [DetectSqlInjections](DetectSqlInjections.md) | Enables or disables SQL injection detection for a database connection and returns the previous setting. |
| [GetLastSQLError](GetLastSQLError.md) | Returns the most recently stored SQL error as an SSLSQLError object, or NIL when no SQL error is currently recorded. |
| [GetNoLock](GetNoLock.md) | Returns the database-specific no-lock clause for a connection. |
| [GetRdbmsDelimiter](GetRdbmsDelimiter.md) | Returns the identifier delimiter character for the database behind a DSN. |
| [IgnoreSqlErrors](IgnoreSqlErrors.md) | Enables or disables SQL error suppression and returns the previous setting. |
| [LimsRecordsAffected](LimsRecordsAffected.md) | Returns the number of records affected by the most recent database operation. |
| [LimsSetCounter](LimsSetCounter.md) | Generates the next counter value and inserts a new row with that key into the target table. |
| [PrepareArrayForIn](PrepareArrayForIn.md) | Prepares an array for SQL IN clause helpers by mutating it in place. |
| [RetrieveLong](RetrieveLong.md) | Retrieves a value from one database column and writes it to a file when the selected value is returned as binary data. |
| [ReturnLastSQLError](ReturnLastSQLError.md) | Returns the currently stored SQL error as an SSLSQLError object, or NIL when no SQL error is recorded. |
| [ShowSqlErrors](ShowSqlErrors.md) | Sets the SQL error display flag, which decides whether a failing RunSQL raises, and returns the previous setting. |
| [SQLRemoveComments](SQLRemoveComments.md) | Removes SQL comments from a string and returns the cleaned SQL text. |
| [UpdLong](UpdLong.md) | Updates a large field value in a database table from the contents of a file, using search criteria for row selection. |
| [XmlExportSql](XmlExportSql.md) | Runs a SQL query, writes the result set to an XML file, and returns an empty string on success or an error message on failure. |

### Dataset Builders

| Function | Description |
|----------|-------------|
| [GetDataSetFromArray](GetDataSetFromArray.md) | Builds a dataset XML string from an array of values and an optional array of field names. |
| [GetDataSetFromArrayEx](GetDataSetFromArrayEx.md) | Generates a dataset XML string from array values, with control over field definitions, table name, header output, and schema output. |
| [GetDataSetWithSchemaFromSelect](GetDataSetWithSchemaFromSelect.md) | Executes a SQL query and returns the result as XML dataset text with schema always included. |
| [GetDataSetXMLFromArray](GetDataSetXMLFromArray.md) | Generates dataset XML from in-memory values, field definitions, and output flags. |
| [GetDataSetXMLFromSelect](GetDataSetXMLFromSelect.md) | Executes a SQL query and returns the result as XML dataset text. |

## Date & Time

| Function | Description |
|----------|-------------|
| [ClientEndOfDay](ClientEndOfDay.md) | Returns the end of the client's calendar day for a date value. |
| [ClientStartOfDay](ClientStartOfDay.md) | Returns the timestamp for the start of the client's calendar day. |
| [CMonth](CMonth.md) | Returns the full month name for a date value. |
| [CToD](CToD.md) | Converts a string in the current SSL date format to a date value. |
| [DateAdd](DateAdd.md) | Adds a time interval to a date and returns the resulting date. |
| [DateDiff](DateDiff.md) | Returns the whole-number difference between two date values in a requested unit. |
| [DateDiffEx](DateDiffEx.md) | Returns the elapsed interval between two date values as an object. |
| [DateFormat](DateFormat.md) | Sets the current SSL date format string. |
| [DateFromNumbers](DateFromNumbers.md) | Creates a date value from individual numeric components. |
| [DateFromString](DateFromString.md) | Parses a string into a date value with optional format and culture controls. |
| [DateToString](DateToString.md) | Converts a date value to a string using a specified or default format. |
| [Day](Day.md) | Extracts the day-of-month number from a date value. |
| [DOW](DOW.md) | Returns the numeric day of week for a date. |
| [DOY](DOY.md) | Calculates the ordinal day number of a date within its year. |
| [DToC](DToC.md) | Converts a date value to a string using the current SSL date format. |
| [DToS](DToS.md) | Converts a date value to an 8-character string in yyyyMMdd format. |
| [Hour](Hour.md) | Extracts the hour component from a date value. |
| [IsInvariantDate](IsInvariantDate.md) | Checks whether a date value has an unspecified (invariant) kind. |
| [JDay](JDay.md) | Returns the day-of-year number for a date, or for today's date when no argument is supplied. |
| [LIMSDate](LIMSDate.md) | Returns a date value as a formatted string. |
| [LimsGetDateFormat](LimsGetDateFormat.md) | Returns the current session date format string used for date parsing and formatting. |
| [LimsTime](LimsTime.md) | Returns the current time as a formatted string. |
| [MakeDateInvariant](MakeDateInvariant.md) | Marks a date, or selected date columns in an array, as invariant. |
| [MakeDateLocal](MakeDateLocal.md) | Sets a date value, or selected date columns in an array, to local date kind in place. |
| [Minute](Minute.md) | Extracts the minute component from a date value. |
| [Month](Month.md) | Extracts the numeric month from a date value. |
| [NoOfDays](NoOfDays.md) | Returns the number of days in the month for a date value. |
| [Now](Now.md) | Returns the current system date and time as an SSL date value. |
| [Second](Second.md) | Extracts the seconds component from a date value. |
| [Seconds](Seconds.md) | Returns the current time of day as the number of whole seconds since midnight. |
| [ServerEndOfDay](ServerEndOfDay.md) | Returns a date value set to the end of its day. |
| [ServerStartOfDay](ServerStartOfDay.md) | Returns a date value set to the start of its day. |
| [ServerTimeZone](ServerTimeZone.md) | Returns the current server's UTC offset in minutes as a number. |
| [StringToDate](StringToDate.md) | Converts a formatted date string into a date value using a specified pattern. |
| [Time](Time.md) | Returns the current time as a formatted string. |
| [Today](Today.md) | Returns the current date as a date object. |
| [UserTimeZone](UserTimeZone.md) | Returns the current user's UTC offset in minutes. If a user-specific offset is not available as a numeric value, the function returns the server's UTC offset instead. |
| [ValidateDate](ValidateDate.md) | Checks whether a string can be interpreted as a valid date. |
| [Year](Year.md) | Extracts the numeric year from a date value. |

## Documentum

### Auth

| Function | Description |
|----------|-------------|
| [DocEndDocumentumInterface](DocEndDocumentumInterface.md) | Ends the current Documentum interface context. |
| [DocInitDocumentumInterface](DocInitDocumentumInterface.md) | Creates a fresh Documentum interface context for the current execution. |
| [DocLoginToDocumentum](DocLoginToDocumentum.md) | Authenticates to a Documentum repository for the current initialized Documentum context. |

### Documents

| Function | Description |
|----------|-------------|
| [DocCancelCheckout](DocCancelCheckout.md) | Cancels checkout for a Documentum document and returns a boolean result. |
| [DocCheckinDocument](DocCheckinDocument.md) | Checks a local file into an existing Documentum document. |
| [DocCheckoutDocument](DocCheckoutDocument.md) | Checks out an existing Documentum document and returns the local checkout file path. |
| [DocDelete](DocDelete.md) | Deletes a Documentum document by object ID. |
| [DocExists](DocExists.md) | Checks whether a Documentum document exists for a given object ID. |
| [DocExportDocument](DocExportDocument.md) | Exports a specified document to a chosen format and returns the result as a string. |
| [DocGetDocuments](DocGetDocuments.md) | Retrieves documents from a Documentum repository folder as a two-dimensional array. |
| [DocGetMetadata](DocGetMetadata.md) | Retrieves metadata rows for a Documentum object. |
| [DocGetTypeAttributes](DocGetTypeAttributes.md) | Retrieves the attribute definitions for a Documentum type as a two-dimensional array. |
| [DocGetTypeAttributesAsDataset](DocGetTypeAttributesAsDataset.md) | Returns the attributes for a Documentum type as a dataset-formatted string. |
| [DocImportDocument](DocImportDocument.md) | Imports a document into Documentum and returns the underlying import result as a string. |
| [DocSetMetadata](DocSetMetadata.md) | Updates one or more metadata attributes on a Documentum object. |

### Folders & Cabinets

| Function | Description |
|----------|-------------|
| [DocCreateCabinet](DocCreateCabinet.md) | Creates a Documentum cabinet and returns the string result from the create operation. |
| [DocCreateFolder](DocCreateFolder.md) | Creates a Documentum folder under a parent path and returns the string result from the create operation. |
| [DocDeleteCabinet](DocDeleteCabinet.md) | Deletes a Documentum cabinet by cabinet identifier. |
| [DocDeleteFolder](DocDeleteFolder.md) | Deletes a Documentum folder and optionally allows the delete only when the folder is empty. |
| [DocGetCabinets](DocGetCabinets.md) | Returns the cabinet names available from the current Documentum connection. |
| [DocGetFolders](DocGetFolders.md) | Retrieves the immediate child folders of a Documentum folder as a sorted two-dimensional array. |

### Users & Groups

| Function | Description |
|----------|-------------|
| [DocAddUsersToGroup](DocAddUsersToGroup.md) | Adds one or more users to an existing Documentum group. |
| [DocCreateACL](DocCreateACL.md) | Creates a Documentum ACL and returns a result string. |
| [DocCreateGroup](DocCreateGroup.md) | Creates a Documentum group and returns its identifier. |
| [DocCreateUser](DocCreateUser.md) | Creates a Documentum user and returns its identifier. |
| [DocDeleteUser](DocDeleteUser.md) | Deletes a Documentum user by login name. |
| [DocExistsUser](DocExistsUser.md) | Determines whether a Documentum user exists for a supplied login context. |
| [DocRemoveAllUsersFromGroup](DocRemoveAllUsersFromGroup.md) | Removes every user from a Documentum group. |
| [DocRemoveUsersFromGroup](DocRemoveUsersFromGroup.md) | Removes one or more users from an existing Documentum group. |
| [DocUpdateUser](DocUpdateUser.md) | Updates a Documentum user and returns the Documentum result message. |

### Workflows

| Function | Description |
|----------|-------------|
| [DocAcquireWorkitem](DocAcquireWorkitem.md) | Acquires a Documentum work item and returns whether the acquisition succeeded. |
| [DocCompleteWorkitem](DocCompleteWorkitem.md) | Completes a Documentum workflow work item and returns whether the operation succeeded. |
| [DocDelegateWorkitem](DocDelegateWorkitem.md) | Delegates a Documentum workflow work item to another user and returns whether the delegation succeeded. |
| [DocGetTasks](DocGetTasks.md) | Retrieves Documentum workflow tasks as a two-dimensional array. |
| [DocGetTasksCount](DocGetTasksCount.md) | Returns the number of workflow tasks in the Documentum inbox for the active session. |
| [DocGetWorkflowStatus](DocGetWorkflowStatus.md) | Returns the current runtime status for a Documentum workflow. |
| [DocGetWorkitemProperties](DocGetWorkitemProperties.md) | Retrieves workflow flags and linked document IDs for a Documentum work item. |
| [DocPauseWorkflow](DocPauseWorkflow.md) | Pauses a Documentum workflow and returns whether the pause succeeded. |
| [DocRepeatWorkitem](DocRepeatWorkitem.md) | Repeats a Documentum workitem and can reassign it to a new user list. |
| [DocResumeWorkflow](DocResumeWorkflow.md) | Resumes a Documentum workflow identified by sWorkflowId. |
| [DocStartWorkflow](DocStartWorkflow.md) | Starts a Documentum workflow and returns the created workflow ID together with the start-activity performers. |
| [DocStopWorkflow](DocStopWorkflow.md) | Stops a Documentum workflow by its workflow ID. |

### Search

| Function | Description |
|----------|-------------|
| [DocSearchAsDataset](DocSearchAsDataset.md) | Searches Documentum and returns the matches as dataset XML. |
| [DocSearchFullText](DocSearchFullText.md) | Performs a Documentum full-text search and returns matching documents as an array. |
| [DocSearchUsingDql](DocSearchUsingDql.md) | Executes a Documentum DQL query and returns the result set as a two-dimensional array. |

### Documentum Errors

| Function | Description |
|----------|-------------|
| [DocCommandFailed](DocCommandFailed.md) | Checks whether the most recent Documentum command in the current session failed. |
| [DocGetErrorMessage](DocGetErrorMessage.md) | Returns the message text from the current Documentum error state. |

## Email

| Function | Description |
|----------|-------------|
| [SendFromOutbox](SendFromOutbox.md) | Sends every email currently queued in the outbox. |
| [SendLimsEmail](SendLimsEmail.md) | Sends an email through SMTP and returns whether the send succeeded. |
| [SendOutlookReminder](SendOutlookReminder.md) | Sends an Outlook-style meeting invitation email and returns whether delivery succeeded. |
| [SendToOutbox](SendToOutbox.md) | Queues an email request in LIMSEMAILOUTBOX for later delivery instead of sending it immediately. |

## Execution & Dynamic Dispatch

| Function | Description |
|----------|-------------|
| [Branch](Branch.md) | Transfers control to a label in the current procedure. |
| [DoProc](DoProc.md) | Calls a local or scripted procedure by name with an optional argument array. |
| [ExecFunction](ExecFunction.md) | Invokes a function by name at runtime and returns the result. |
| [ExecInternal](ExecInternal.md) | Calls a method on an object by name and returns that method's result. |
| [ExecUdf](ExecUdf.md) | Executes SSL source supplied as a string and returns the result. |
| [IIf](IIf.md) | Selects one of two values based on a boolean condition. |
| [LCase](LCase.md) | Conditionally evaluates one of two SSL expressions supplied as strings. |
| [LimsExec](LimsExec.md) | Launches an external application without waiting for it to finish. |
| [PrmCount](PrmCount.md) | Returns how many arguments the caller passed to the current server script; only valid in script-level code. |
| [RunApp](RunApp.md) | Launches an external application and waits for it to exit. |

## FTP

| Function | Description |
|----------|-------------|
| [CheckOnFtp](CheckOnFtp.md) | Checks whether a remote file exists on an FTP server, or on an SFTP server when bIsSFTP is .T.. |
| [CopyToFtp](CopyToFtp.md) | Appends the same text content to one or more files on an FTP or SFTP server. |
| [DeleteDirOnFtp](DeleteDirOnFtp.md) | Deletes a remote directory over FTP or SFTP. |
| [DeleteFromFtp](DeleteFromFtp.md) | Deletes a remote file through FTP, or through SFTP when bIsSFTP is .T.. |
| [GetDirFromFtp](GetDirFromFtp.md) | Lists directory entries from an FTP server, or from an SFTP server when bIsSFTP is .T.. |
| [GetFromFtp](GetFromFtp.md) | Downloads a file from an FTP or SFTP server to a local file. |
| [MakeDirOnFtp](MakeDirOnFtp.md) | Creates a remote directory by using FTP, or by using SFTP when bIsSFTP is .T.. |
| [MoveInFtp](MoveInFtp.md) | Moves a remote file on an FTP server, or on an SFTP server when bIsSFTP is .T.. |
| [ReadFromFtp](ReadFromFtp.md) | Retrieves a remote file as a string by using FTP, or SFTP when bIsSFTP is .T.. |
| [RenameOnFtp](RenameOnFtp.md) | Renames a remote file on an FTP server, or on an SFTP server when bIsSFTP is .T.. |
| [SendToFtp](SendToFtp.md) | Uploads one local file to an FTP or SFTP server. |
| [WriteToFtp](WriteToFtp.md) | Appends text to a remote file over FTP or SFTP. |

## File System

| Function | Description |
|----------|-------------|
| [CombineFiles](CombineFiles.md) | Concatenates multiple files into one output file on disk. |
| [Compress](Compress.md) | Compresses a non-empty string and returns the compressed result as either a base64 string or a generated file path. |
| [ConvertReport](ConvertReport.md) | Converts a report file identified by a file path and returns .T. when the conversion completes. |
| [CreateZip](CreateZip.md) | Creates a ZIP archive from a source directory. |
| [Decompress](Decompress.md) | Decompresses compressed text and returns the restored string. |
| [Directory](Directory.md) | Retrieves filesystem entries that match a path or wildcard pattern, with optional filtering for directories, hidden entries, and system entries. |
| [DosSupport](DosSupport.md) | Executes operating system-level file and directory commands. |
| [ExtractZip](ExtractZip.md) | Extracts a ZIP archive into a target directory. |
| [FileSupport](FileSupport.md) | Performs multiple file operations through a single request-driven interface. |
| [GetAppBaseFolder](GetAppBaseFolder.md) | Returns the application's base folder path as a string for use in file and configuration operations. |
| [GetAppWorkPathFolder](GetAppWorkPathFolder.md) | Returns the path to the application's working directory as a string. |
| [GetFileVersion](GetFileVersion.md) | Retrieves the file version string for a specified file path. |
| [GetLogsFolder](GetLogsFolder.md) | Returns the configured user log folder path with a trailing backslash. |
| [GetWebFolder](GetWebFolder.md) | Returns the current web folder path as a string. |
| [LDir](LDir.md) | Retrieves an array of file and directory names matching a specified pattern and optional attribute filter. |
| [ReadBytesBase64](ReadBytesBase64.md) | Reads a file from disk and returns its contents as a base64-encoded string. |
| [ReadText](ReadText.md) | Reads a text file and returns its contents, or the first n characters, as a string, with an optional encoding. |
| [WriteBytesBase64](WriteBytesBase64.md) | Writes a base64-encoded value to disk as binary file content. |
| [WriteText](WriteText.md) | Writes or appends string content to a text file with optional encoding. |

## Inline Code

Manage *inline code* — SSL snippets stored in the dictionary between [`:BEGININLINECODE`](../keywords/BEGININLINECODE.md) and [`:ENDINLINECODE`](../keywords/ENDINLINECODE.md) markers and executed by name.

| Function | Description |
|----------|-------------|
| [DeleteInlineCode](DeleteInlineCode.md) | Removes a named inline code entry using a case-insensitive name lookup. |
| [Eval](Eval.md) | Invokes a code block with the supplied arguments and returns the block's result. |
| [GetInlineCode](GetInlineCode.md) | Retrieves a named inline code block as a string. |
| [GetRegion](GetRegion.md) | Retrieves a named region string from the current region scope and can optionally apply sequential text replacements. |
| [GetRegionEx](GetRegionEx.md) | Retrieves a named region string, optionally using a caller-supplied local region map before falling back to the current region scope. |

## Messaging & Errors

| Function | Description |
|----------|-------------|
| [ClearLastSSLError](ClearLastSSLError.md) | Clears the stored SSL error so later error checks start clean. |
| [ErrorMes](ErrorMes.md) | Writes an error message to the server log, even when user-message logging is disabled, and returns the formatted log entry. |
| [FormatErrorMessage](FormatErrorMessage.md) | Returns a formatted string description for an error value. |
| [FormatSqlErrorMessage](FormatSqlErrorMessage.md) | Returns a human-readable error message from a SQL error value. |
| [GetLastSSLError](GetLastSSLError.md) | Retrieves the most recent SSL error encountered during the current process. |
| [InfoMes](InfoMes.md) | Logs an informational user message and returns the same formatted string as UsrMes. |
| [RaiseError](RaiseError.md) | Raises an SSL runtime error using the supplied message and optional location, error code, and inner error. |
| [UsrMes](UsrMes.md) | Writes a user message to the user log and returns the formatted log text. |

## Numeric & Math

| Function | Description |
|----------|-------------|
| [_AND](_AND.md) | Performs a bitwise AND operation between two integer numbers and returns the result. |
| [_NOT](_NOT.md) | Returns the bitwise complement of a whole-number operand. |
| [_OR](_OR.md) | Returns the bitwise inclusive OR of two whole-number operands. |
| [_XOR](_XOR.md) | Returns the bitwise exclusive OR of two whole-number operands. |
| [Abs](Abs.md) | Calculates the absolute value of a number. |
| [GetDecimalSep](GetDecimalSep.md) | Returns the current decimal separator as a numeric character code. |
| [GetDecimalSeparator](GetDecimalSeparator.md) | Returns the current decimal separator as a string. |
| [GetGroupSeparator](GetGroupSeparator.md) | Returns the current group separator as a string. |
| [IsNumeric](IsNumeric.md) | Determines whether a string is a valid numeric value, with optional support for hexadecimal input. |
| [LimsXOr](LimsXOr.md) | Calculates the bitwise exclusive OR of two integer-valued numbers. |
| [MatFunc](MatFunc.md) | Calculates a mathematical operation on a given number based on the specified function name. |
| [Max](Max.md) | Returns whichever of two values compares greater when both arguments are the same supported type. |
| [Min](Min.md) | Returns whichever of two values compares lower when both arguments are the same supported type. |
| [Rand](Rand.md) | Generates a pseudo-random number between 0 (inclusive) and 1 (exclusive). |
| [Round](Round.md) | Rounds a numeric value to a specific number of decimal places using a configurable midpoint handling strategy. |
| [RoundPoint5](RoundPoint5.md) | Rounds a numeric value to a half-point increment. |
| [Scient](Scient.md) | Converts a number to its scientific notation string representation. |
| [SetDecimalSeparator](SetDecimalSeparator.md) | Sets the current decimal separator and returns the previous setting. |
| [SetGroupSeparator](SetGroupSeparator.md) | Changes the group (thousands) separator character used when numbers are formatted as strings across the application. |
| [SigFig](SigFig.md) | Returns a string produced by applying a named rounding standard to a numeric value. |
| [Sqrt](Sqrt.md) | Calculates the non-negative square root of a numeric value. |
| [StdRound](StdRound.md) | Returns a string produced by applying a named rounding standard to a numeric value. |
| [ToScientific](ToScientific.md) | Converts a numeric value to a scientific-notation string. |
| [ValidateNumeric](ValidateNumeric.md) | Determines whether a string is a valid numeric value under the current STARLIMS numeric settings. |

## Object & Interop

| Function | Description |
|----------|-------------|
| [AddProperty](AddProperty.md) | Adds one or more properties to an object. |
| [CreateUdObject](CreateUdObject.md) | Creates a dynamic object or instantiates a user-defined class. |
| [EndLimsOleConnect](EndLimsOleConnect.md) | Disposes an object previously created for OLE automation use. |
| [GetInternal](GetInternal.md) | Retrieves the current value of a named property from a value that supports property access. |
| [GetInternalC](GetInternalC.md) | Retrieves a value by applying a chained series of index operations to a root value. |
| [HasProperty](HasProperty.md) | Checks whether a value exposes a named property. |
| [LimsNETConnect](LimsNETConnect.md) | Loads a .NET assembly, resolves a type, and either returns a type handle or creates an instance for SSL interop. |
| [LimsOleConnect](LimsOleConnect.md) | Creates an object from a ProgID so SSL code can work with an OLE or COM automation server. |
| [MakeNETObject](MakeNETObject.md) | Converts an SSL value to a .NET interop object. |
| [SetInternal](SetInternal.md) | Assigns a value to a named property on a target value and returns NIL. |
| [SetInternalC](SetInternalC.md) | Assigns a value through a chained index path on a target value and returns NIL. |
| [XmlDomToUdObject](XmlDomToUdObject.md) | Converts an XML string into a dynamic object tree. |

## Security

| Function | Description |
|----------|-------------|
| [ChkNewPassword](ChkNewPassword.md) | Validates that a proposed password is not already present in stored password history. |
| [ChkPassword](ChkPassword.md) | Checks whether a user name and password combination is accepted. |
| [DecryptData](DecryptData.md) | Decrypts an encrypted string with a password and returns the plaintext string. |
| [EncryptData](EncryptData.md) | Encrypts a string with a password by using the legacy built-in RC2, DES, or 3DES algorithms. |
| [GetUserData](GetUserData.md) | Returns the current session user name as a string. |
| [HashData](HashData.md) | Computes a one-way hash string from input text. |
| [LDAPAuth](LDAPAuth.md) | Authenticates a user by binding directly to an LDAP server. |
| [LDAPAuthEX](LDAPAuthEX.md) | Authenticates an LDAP user by searching for exactly one directory entry and then binding as that user. |
| [SearchLDAPUser](SearchLDAPUser.md) | Searches LDAP for exactly one user and returns that entry's distinguished name. |
| [SetUserData](SetUserData.md) | Sets the current user name for the active execution context. |
| [SetUserPassword](SetUserPassword.md) | Updates a user's password and returns the stored password hash. |
| [VerifySignature](VerifySignature.md) | Verifies a base64-encoded digital signature against a string by using the public key from a supplied X.509 certificate. |

## String

| Function | Description |
|----------|-------------|
| [AllTrim](AllTrim.md) | Removes leading and trailing space characters from a string. |
| [Asc](Asc.md) | Returns the character code of the first character in a string. |
| [At](At.md) | Finds the first occurrence of a substring in a string and returns its one-based position. |
| [BuildString](BuildString.md) | Builds one string from array elements using a delimiter. |
| [BuildString2](BuildString2.md) | Builds one string from a two-dimensional array using separate row and column delimiters. |
| [Chr](Chr.md) | Converts a numeric character code to a single-character string. |
| [CreateGUID](CreateGUID.md) | Generates a new GUID string in uppercase. |
| [HtmlDecode](HtmlDecode.md) | Converts selected HTML/XML entity sequences in a string back to literal characters. |
| [HtmlEncode](HtmlEncode.md) | Converts selected characters in a string to entity sequences for HTML or XML text output. |
| [IsGuid](IsGuid.md) | Validates whether a string matches the GUID format and returns a boolean result. |
| [IsHex](IsHex.md) | Validates whether a string contains only uppercase hexadecimal characters. |
| [Left](Left.md) | Extracts the leftmost characters from a string. |
| [Len](Len.md) | Returns the number of characters in a string or the element count of an array. |
| [LimsAt](LimsAt.md) | Finds the first occurrence of a substring in a string at or after a 1-based starting position. |
| [LimsString](LimsString.md) | Converts a value to a string, returning "NIL" when the input is NIL. |
| [LLower](LLower.md) | Converts all characters in a string to their lowercase equivalents. |
| [Lower](Lower.md) | Converts all characters in a string to lowercase. |
| [LStr](LStr.md) | Converts a value to its trimmed string representation, returning "NIL" when the input is NIL. |
| [LToHex](LToHex.md) | Converts a string or integer to hexadecimal text. |
| [LTrim](LTrim.md) | Removes leading whitespace from a string. |
| [MimeDecode](MimeDecode.md) | Decodes MIME-encoded data to its plain string representation. |
| [MimeEncode](MimeEncode.md) | Encodes a string so it can be round-tripped later with MimeDecode. |
| [Rat](Rat.md) | Finds the last occurrence of a substring in a string and returns its one-based position. |
| [Replace](Replace.md) | Replaces all occurrences of a specified substring within a string with another substring and returns the resulting string. |
| [Replicate](Replicate.md) | Creates a string by repeating the source string a specified number of times. |
| [Right](Right.md) | Extracts a specified number of characters from the end of a string. |
| [Str](Str.md) | Converts a numeric value to a formatted string. |
| [StrSrch](StrSrch.md) | Finds a substring by occurrence number or from a specific 1-based starting position. |
| [StrTran](StrTran.md) | Replaces all occurrences of a specified substring with another substring in a source string. |
| [StrZero](StrZero.md) | Formats a number as a zero-padded string, with optional total width and decimal precision. |
| [SubStr](SubStr.md) | Extracts part of a string starting at a position you specify. |
| [Trim](Trim.md) | Removes trailing whitespace from a string. |
| [Upper](Upper.md) | Converts all characters in a string to uppercase. |
| [UrlDecode](UrlDecode.md) | Decodes percent-encoded URL text back into its readable string form. |
| [UrlEncode](UrlEncode.md) | Converts a string into a format safe for inclusion in a URL by encoding unsafe characters. |

## System & Batch

| Function | Description |
|----------|-------------|
| [GetPrinters](GetPrinters.md) | Returns a list of printer names installed on the STARLIMS application server. |
| [InBatchProcess](InBatchProcess.md) | Returns whether the current SSL execution context is running in a batch process. |
| [IsProductionModeOn](IsProductionModeOn.md) | Returns .T. when the application's production mode flag is enabled and .F. otherwise. |
| [LWait](LWait.md) | Blocks further script execution for a specified number of seconds and returns an empty string. |
| [SubmitToBatch](SubmitToBatch.md) | Submits SSL code to a batch worker and returns the submitted job identifier. |
| [SubmitToBatchEx](SubmitToBatchEx.md) | Submits SSL code to batch execution and returns the submitted job identifier. |

## Type Conversion

| Function | Description |
|----------|-------------|
| [Empty](Empty.md) | Returns .T. when a value is considered empty by SSL; otherwise returns .F. |
| [FromJson](FromJson.md) | Parses a JSON string into the closest SSL-native value or returns the input unchanged if it is not a string. JSON arrays become arrays, objects become SSLExpando instances, numbers become numbers, booleans become booleans, and strings become strings or dates when the value starts with SSLDate\|. Null input, empty strings, and JSON null values return NIL. Invalid JSON tokens raise an error. |
| [FromXml](FromXml.md) | Parses a type-tagged XML string and converts it to the corresponding SSL value. |
| [Integer](Integer.md) | Returns the whole-number portion of a numeric value by truncating the fractional part toward zero. |
| [LFromHex](LFromHex.md) | Converts a hexadecimal string to a string by reading the input in two-character chunks and decoding each chunk as a byte. |
| [LHex2Dec](LHex2Dec.md) | Converts a hexadecimal string to its decimal string representation. |
| [LimsNETCast](LimsNETCast.md) | Prepares a value for a requested interop type such as an enum, by-reference value, numeric type, or typed array. |
| [LimsNETTypeOf](LimsNETTypeOf.md) | Resolves a .NET type name string to a .NET Type object. |
| [LimsType](LimsType.md) | Returns the SSL type code for a variable name or expression. |
| [LimsTypeEx](LimsTypeEx.md) | Returns the public SSL type name for a value. |
| [LTransform](LTransform.md) | Formats a numeric expression as a string by applying a picture string. |
| [Nothing](Nothing.md) | Returns .T. when vValue is NIL, empty by SSL rules, or stringifies to the exact value "0"; otherwise returns .F.. |
| [ToJson](ToJson.md) | Serializes an SSL value, array, or object to a JSON string. |
| [ToNumeric](ToNumeric.md) | Converts a string to a number, with optional hexadecimal support. |
| [ToXml](ToXml.md) | Serializes a value, array, or dynamic object to an XML string. |
| [Val](Val.md) | Converts numeric text at the start of a string to a number. |

## Variable & Session Management

| Function | Description |
|----------|-------------|
| [AddToSession](AddToSession.md) | Stores a non-object, non-array value in the current session under a string key. |
| [ClearSession](ClearSession.md) | Clears all values from the current session. |
| [CreateLocal](CreateLocal.md) | Creates or overwrites a local variable in the current scope by name. |
| [CreatePublic](CreatePublic.md) | Creates or overwrites a public variable by name. |
| [GetByName](GetByName.md) | Retrieves the value of a variable by name from the current scope, a caller scope, or public storage. |
| [GetFromApplication](GetFromApplication.md) | Returns a comma-separated string of connected usernames when called with the special key "STARLIMSUSERS" in a CUSTOM session context. |
| [GetFromSession](GetFromSession.md) | Retrieves the value associated with a specified key from the current user session. |
| [GetSetting](GetSetting.md) | Retrieves the stored value of a named configuration setting. |
| [GetSettings](GetSettings.md) | Retrieves multiple named settings in one call. |
| [IsDefined](IsDefined.md) | Determines whether a variable name is currently defined. |
| [LKill](LKill.md) | Deletes a public variable from the current SSL session by name and returns an empty string. |
| [SetByName](SetByName.md) | Assigns a value to a variable whose name is supplied at runtime. |
