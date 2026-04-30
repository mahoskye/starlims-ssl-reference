---
title: "Functions"
summary: "330 built-in functions organized by category."
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Functions

**330 built-in functions** organized by category.

## Categories

- [Array](#array) (15)
- [Database](#database) (54)
  - [SQL Queries](#sql-queries)
  - [Transactions](#transactions)
  - [Connections](#connections)
  - [Schema](#schema)
  - [SQL Utilities](#sql-utilities)
  - [Dataset Builders](#dataset-builders)
- [Date & Time](#date-time) (39)
- [Documentum](#documentum) (47)
  - [Auth](#auth)
  - [Documents](#documents)
  - [Folders & Cabinets](#folders-cabinets)
  - [Users & Groups](#users-groups)
  - [Workflows](#workflows)
  - [Search](#search)
  - [Errors](#documentum-errors)
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
| [AAdd](AAdd.md) | Appends an element to the end of an array and returns that element. |
| [AEval](AEval.md) | Iterates an array, evaluating a code block against each element for its side effects and returning the array unchanged. |
| [AEvalA](AEvalA.md) | Applies a code block to each element of an array, replacing elements in place with the result. |
| [AFill](AFill.md) | Fills a specified range of elements in an array with a given value, modifying the original array in place. |
| [ALen](ALen.md) | Calculates the number of elements in a given array. |
| [AScan](AScan.md) | Finds the index of the first array element matching a given value or condition. |
| [AScanExact](AScanExact.md) | Searches an array for the first element that exactly matches a specified value or meets a condition. |
| [ArrayCalc](ArrayCalc.md) | Performs a wide range of operations—such as copying, merging, filling, sorting, and calculating statistics—on an array in a single flexible call. |
| [ArrayNew](ArrayNew.md) | Creates a new array with up to three specified dimensions, each with an explicit length. |
| [BuildArray](BuildArray.md) | Splits a string into an array using a specified delimiter, optionally trimming spaces from each element. |
| [BuildArray2](BuildArray2.md) | Parses a string into a two-dimensional array using customizable line and column delimiters. |
| [CompArray](CompArray.md) | Determines whether two arrays are structurally and value-wise equal. |
| [DelArray](DelArray.md) | Removes an element from an array at the specified index and returns the resulting array. |
| [ExtractCol](ExtractCol.md) | Extracts all values from a specified column in a two-dimensional array and returns them in a new array. |
| [SortArray](SortArray.md) | Sorts an array in-place using numeric or custom comparison logic. |

## Database

### SQL Queries

| Function | Description |
|----------|-------------|
| [GetDataSet](GetDataSet.md) | Executes a database query and returns the results as an XML string representing the dataset. |
| [GetDataSetEx](GetDataSetEx.md) | Executes a database query and returns its result as an XML string with flexible output options. |
| [GetNETDataSet](GetNETDataSet.md) | Retrieves a dataset from a database using a command string and optional filters, returning XML or object output as specified. |
| [GetSSLDataset](GetSSLDataset.md) | Executes a SQL query against a database or data source and returns the results as an SSLDataset. |
| [LSearch](LSearch.md) | Executes a SQL search and returns a single value or a specified default if the query finds no result. |
| [LSelect](LSelect.md) | Executes a SQL query and returns the result set as an array. |
| [LSelect1](LSelect1.md) | Executes a parameterized SQL SELECT command and returns the result as an array of rows. |
| [LSelectC](LSelectC.md) | Executes a parameterized SQL select query and returns result rows as an array of arrays. |
| [RunDS](RunDS.md) | Retrieves data from a specified data source using parameters and returns it in the chosen format. |
| [RunSQL](RunSQL.md) | Executes a provided SQL command against the database and returns whether the operation succeeded. |
| [SQLExecute](SQLExecute.md) | Executes a SQL command against a database and returns query results or execution status. |

### Transactions

| Function | Description |
|----------|-------------|
| [BeginLimsTransaction](BeginLimsTransaction.md) | Starts a database transaction on a specified or default LIMS connection with optional isolation level control. |
| [EndLimsTransaction](EndLimsTransaction.md) | Closes an active LIMS transaction, saving or discarding changes based on a flag, and reports the outcome. |
| [GetTransactionsCount](GetTransactionsCount.md) | Returns the number of open database transactions for a specified or default connection. |
| [IsInTransaction](IsInTransaction.md) | Returns true if the specified database connection currently has an open transaction; otherwise, false. |

### Connections

| Function | Description |
|----------|-------------|
| [GetConnectionByName](GetConnectionByName.md) | Retrieves a database connection object using a specified connection name. |
| [GetConnectionStrings](GetConnectionStrings.md) | Retrieves all available database connection strings configured in the system as a two-dimensional array. |
| [GetDBMSName](GetDBMSName.md) | Identifies the database management system (DBMS) platform for a specified or default database connection. |
| [GetDBMSProviderName](GetDBMSProviderName.md) | Returns the uppercase DBMS provider identifier for a named logical database, or raises a DAL error if the name is unknown. |
| [GetDefaultConnection](GetDefaultConnection.md) | Returns the current default database connection string used for executing database operations. |
| [IsDBConnected](IsDBConnected.md) | Checks if a named database connection is currently established and available for use. |
| [LimsSqlConnect](LimsSqlConnect.md) | Establishes a database connection using a registered identifier and updates the connection registry. |
| [LimsSqlDisconnect](LimsSqlDisconnect.md) | Closes an active database connection identified by its connection name and removes it from the internal registry. |
| [SetDefaultConnection](SetDefaultConnection.md) | Changes the active default database connection for the current session and returns the previous default connection name. |
| [SetSqlTimeout](SetSqlTimeout.md) | Adjusts the SQL command timeout for a specified database connection and returns the previous timeout value. |

### Schema

| Function | Description |
|----------|-------------|
| [GetDSParameters](GetDSParameters.md) | Retrieves all parameter keys associated with a given data source. |
| [GetTables](GetTables.md) | Extracts a list of table names referenced in a given SQL SELECT statement or fragment. |
| [IsTable](IsTable.md) | Checks whether a specified table exists in the database using the provided context. |
| [IsTableFld](IsTableFld.md) | Checks whether a specific field exists within a table in the database, returning a boolean result. |
| [TableFldLst](TableFldLst.md) | Returns an array of field names for a specified table, using a given or default database connection. |

### SQL Utilities

| Function | Description |
|----------|-------------|
| [AddColDelimiters](AddColDelimiters.md) | Adds database-appropriate delimiters and table-qualifies each column name in an array. |
| [AddNameDelimiters](AddNameDelimiters.md) | Wraps a string name in database-appropriate delimiters for safe SQL usage. |
| [ArrayToTVP](ArrayToTVP.md) | Converts a one-dimensional array into a table-valued parameter (TVP) object for use in supported database operations. |
| [BuildStringForIn](BuildStringForIn.md) | Concatenates array values into a single, parenthesized, and properly delimited string suitable for SQL IN clauses. |
| [CreateORMSession](CreateORMSession.md) | Establishes and returns a shared ORM session object for coordinated database operations. |
| [DetectSqlInjections](DetectSqlInjections.md) | Enables or disables SQL injection detection for a specified database connection and returns its prior setting. |
| [GetLastSQLError](GetLastSQLError.md) | Returns details of the most recent SQL database error or `NIL` if no error has occurred. |
| [GetNoLock](GetNoLock.md) | Returns the appropriate SQL no-lock query hint string for the specified database connection or platform. |
| [GetRdbmsDelimiter](GetRdbmsDelimiter.md) | Returns the correct identifier delimiter character for a specified RDBMS and context. |
| [IgnoreSqlErrors](IgnoreSqlErrors.md) | Enables or disables suppression of SQL error handling within the current session. |
| [LimsRecordsAffected](LimsRecordsAffected.md) | Returns the number of records affected by the most recent database operation. |
| [LimsSetCounter](LimsSetCounter.md) | Updates a numeric counter in a database table and inserts a new row with the result. |
| [PrepareArrayForIn](PrepareArrayForIn.md) | Fills an array's missing or empty entries with type-appropriate default values in place. |
| [ReturnLastSQLError](ReturnLastSQLError.md) | Retrieves the most recent SQL error that occurred during a database operation. |
| [RetrieveLong](RetrieveLong.md) | Retrieves large binary or text data from a database column and writes it to a file. |
| [SQLRemoveComments](SQLRemoveComments.md) | Removes all comments from an SQL statement, returning the cleaned result. |
| [ShowSqlErrors](ShowSqlErrors.md) | Alters the application-wide setting that determines whether SQL errors are visibly displayed to users. |
| [UpdLong](UpdLong.md) | Updates a large field value in a database table from the contents of a file, using search criteria for row selection. |
| [XmlExportSql](XmlExportSql.md) | Exports SQL query results to an XML file on disk, returning an empty string on success or an error message if failed. |

### Dataset Builders

| Function | Description |
|----------|-------------|
| [GetDataSetFromArray](GetDataSetFromArray.md) | Converts an array of values and optional field descriptors into a string-encoded tabular dataset. |
| [GetDataSetFromArrayEx](GetDataSetFromArrayEx.md) | Converts a two-dimensional array of values and optional field definitions into an XML dataset string, throwing an error if required arrays are `NIL`. |
| [GetDataSetWithSchemaFromSelect](GetDataSetWithSchemaFromSelect.md) | Returns an XML dataset with schema information generated from a SQL SELECT statement, using an optional connection name and constraint arrays. |
| [GetDataSetXMLFromArray](GetDataSetXMLFromArray.md) | Generates an XML string representing tabular data using provided values and field definitions. |
| [GetDataSetXMLFromSelect](GetDataSetXMLFromSelect.md) | Generates an XML string from the results of a database query with customizable headers, schema, and null handling. |

## Date & Time

| Function | Description |
|----------|-------------|
| [CMonth](CMonth.md) | Returns the full month name for a given date value. |
| [CToD](CToD.md) | Converts a date string to a date value, raising an exception if the input is `NIL` or returning an empty date if parsing fails. |
| [ClientEndOfDay](ClientEndOfDay.md) | Calculates the end-of-day timestamp for a given date, adjusted to the client's local timezone. |
| [ClientStartOfDay](ClientStartOfDay.md) | Calculates the local start of day for a given date, adjusting for timezone differences. |
| [DOW](DOW.md) | Calculates the day of the week for a given date and returns it as a numeric value. |
| [DOY](DOY.md) | Calculates the numeric day of the year for a given date value. |
| [DToC](DToC.md) | Converts a date value to a formatted string using the current date format settings. |
| [DToS](DToS.md) | Converts a date value to a string in the yyyymmdd format. |
| [DateAdd](DateAdd.md) | Adds a specified time interval to a date and returns the resulting date. |
| [DateDiff](DateDiff.md) | Calculates the difference between two dates and returns the result in a specified unit of time. |
| [DateDiffEx](DateDiffEx.md) | Calculates the difference between two dates and returns the result as a time interval object. |
| [DateFormat](DateFormat.md) | Sets the application-wide date format to a new string pattern. |
| [DateFromNumbers](DateFromNumbers.md) | Creates a date value from individual numeric components, applying defaults where values are omitted. |
| [DateFromString](DateFromString.md) | Converts a date represented as a string into a date value using optional format and culture settings. |
| [DateToString](DateToString.md) | Converts a date value to a string using a specified or default format. |
| [Day](Day.md) | Extracts the day of the month as a number from a date value. |
| [Hour](Hour.md) | Extracts the hour component (0–23) from a date value; raises an error if the date is `NIL`. |
| [IsInvariantDate](IsInvariantDate.md) | Checks if a date value is in an invariant (unspecified) state and returns a boolean result. |
| [JDay](JDay.md) | Returns the numeric day of the year (1–366) for a given date value. |
| [LIMSDate](LIMSDate.md) | Returns a date as a formatted string, using a provided pattern or a default format. |
| [LimsGetDateFormat](LimsGetDateFormat.md) | Returns the current global date format string used for date parsing and formatting. |
| [LimsTime](LimsTime.md) | Returns the current system time as a string in the default time format. |
| [MakeDateInvariant](MakeDateInvariant.md) | Converts a supplied date or array of dates to an invariant date format, detaching it from any local context. |
| [MakeDateLocal](MakeDateLocal.md) | Converts a date or specific date columns within an array to local time, modifying them in place. |
| [Minute](Minute.md) | Extracts the minute value (0–59) from a given date. |
| [Month](Month.md) | Extracts the month number (1–12) from a date value, returning 0 if the date is empty. |
| [NoOfDays](NoOfDays.md) | Calculates the number of days in the month of a specified date. |
| [Now](Now.md) | Returns the current date and time as a date value. |
| [Second](Second.md) | Extracts the seconds value (0–59) from a given date. |
| [Seconds](Seconds.md) | Calculates the number of seconds elapsed since midnight based on the current time. |
| [ServerEndOfDay](ServerEndOfDay.md) | Sets a date value to the final millisecond of its day using server-side time boundary rules. |
| [ServerStartOfDay](ServerStartOfDay.md) | Returns the date set to midnight at the start of its day according to server rules. |
| [ServerTimeZone](ServerTimeZone.md) | Returns the current server's UTC offset in minutes as a number. |
| [StringToDate](StringToDate.md) | Converts a formatted date string into a date value using a specified pattern. |
| [Time](Time.md) | Returns the current system time as a formatted string based on application settings. |
| [Today](Today.md) | Returns the current date as a date object. |
| [UserTimeZone](UserTimeZone.md) | Returns the user's timezone offset in minutes from UTC, falling back to the server offset when unavailable. |
| [ValidateDate](ValidateDate.md) | Validates whether a given string represents a valid date in expected formats. |
| [Year](Year.md) | Returns the year component from a date value. |

## Documentum

### Auth

| Function | Description |
|----------|-------------|
| [DocEndDocumentumInterface](DocEndDocumentumInterface.md) | Ends the active Documentum interface session and clears the associated context. |
| [DocInitDocumentumInterface](DocInitDocumentumInterface.md) | Establishes a new session context required for Documentum operations. |
| [DocLoginToDocumentum](DocLoginToDocumentum.md) | Authenticates a user to a specific Documentum repository and establishes a session context for further interactions. |

### Documents

| Function | Description |
|----------|-------------|
| [DocCancelCheckout](DocCancelCheckout.md) | Cancels the checked-out status of a specified document in Documentum and returns the result. |
| [DocCheckinDocument](DocCheckinDocument.md) | Check in a document file to the Documentum system, updating version and content as specified. |
| [DocCheckoutDocument](DocCheckoutDocument.md) | Checks out a document from the Documentum management system and returns its local reference. |
| [DocDelete](DocDelete.md) | Permanently removes one or all versions of a document using its "objId" parameter. |
| [DocExists](DocExists.md) | Checks if a document exists in the document management system by object ID. |
| [DocExportDocument](DocExportDocument.md) | Exports a specified document to a chosen format and returns the result as a string. |
| [DocGetDocuments](DocGetDocuments.md) | Retrieves an array of documents from a specified repository folder, optionally filtering by document type. |
| [DocGetMetadata](DocGetMetadata.md) | Retrieves metadata attributes for a specified object from a Documentum repository. |
| [DocGetTypeAttributes](DocGetTypeAttributes.md) | Retrieves metadata about all attributes for a specified document type as an array. |
| [DocGetTypeAttributesAsDataset](DocGetTypeAttributesAsDataset.md) | Retrieves the attributes of a specified type from Documentum as a structured dataset string. |
| [DocImportDocument](DocImportDocument.md) | Imports a document file to a specified destination with metadata and access control configuration. |
| [DocSetMetadata](DocSetMetadata.md) | Updates metadata attributes for a specified Documentum object by applying a set of attribute name/value pairs. |

### Folders & Cabinets

| Function | Description |
|----------|-------------|
| [DocCreateCabinet](DocCreateCabinet.md) | Creates a new cabinet in the document management system with optional type and access control settings. |
| [DocCreateFolder](DocCreateFolder.md) | Creates a folder in Documentum at the specified path, returning its identifier on success and an empty string on failure. |
| [DocDeleteCabinet](DocDeleteCabinet.md) | Deletes a specified cabinet from the repository, optionally including all nested documents and folders. |
| [DocDeleteFolder](DocDeleteFolder.md) | Deletes a folder from the Documentum repository, optionally removing all contents recursively. |
| [DocGetCabinets](DocGetCabinets.md) | Retrieves the names of all cabinets available on the connected Documentum server as an array. |
| [DocGetFolders](DocGetFolders.md) | Retrieves immediate subfolders of a specified parent folder and returns their metadata as an array. |

### Users & Groups

| Function | Description |
|----------|-------------|
| [DocAddUsersToGroup](DocAddUsersToGroup.md) | Grants a set of users membership in a specified group for security and document management purposes. |
| [DocCreateACL](DocCreateACL.md) | Creates an Access Control List (ACL) entry in the Documentum repository for a set of groups. |
| [DocCreateGroup](DocCreateGroup.md) | Creates a new group in the enterprise document repository and returns its unique identifier. |
| [DocCreateUser](DocCreateUser.md) | Creates a new user account with specified credentials and attributes and returns the user account identifier. |
| [DocDeleteUser](DocDeleteUser.md) | Deletes a user from the Documentum system by username. |
| [DocExistsUser](DocExistsUser.md) | Determines whether a specific user exists in the configured Documentum system for the given login. |
| [DocRemoveAllUsersFromGroup](DocRemoveAllUsersFromGroup.md) | Removes all users from a specified Documentum group. |
| [DocRemoveUsersFromGroup](DocRemoveUsersFromGroup.md) | Removes one or more specified users from a given group in the Documentum system. |
| [DocUpdateUser](DocUpdateUser.md) | Updates a user's account details, credentials, and access configuration in the Documentum repository. |

### Workflows

| Function | Description |
|----------|-------------|
| [DocAcquireWorkitem](DocAcquireWorkitem.md) | Acquires a specific work item from the Documentum backend and indicates success or failure. |
| [DocCompleteWorkitem](DocCompleteWorkitem.md) | Completes a workflow work item, optionally recording approval and reason, and indicates success or failure. |
| [DocDelegateWorkitem](DocDelegateWorkitem.md) | Delegates a specified workflow work item to another user and returns whether the operation succeeded. |
| [DocGetTasks](DocGetTasks.md) | Retrieves the list of workflow tasks from a Documentum system for a specified workflow identifier. |
| [DocGetTasksCount](DocGetTasksCount.md) | Returns the number of workflow tasks in the Documentum inbox for the active session. |
| [DocGetWorkflowStatus](DocGetWorkflowStatus.md) | Retrieves the current status of a workflow from the Documentum repository using its identifier. |
| [DocGetWorkitemProperties](DocGetWorkitemProperties.md) | Retrieves delegation, repeatability, sign-off requirements, and related document references for a specified work item. |
| [DocPauseWorkflow](DocPauseWorkflow.md) | Temporarily halts workflow processing to prevent further steps until manual intervention or review. |
| [DocRepeatWorkitem](DocRepeatWorkitem.md) | Executes a repeat operation on a workflow workitem, optionally reassigning it to specified users. |
| [DocResumeWorkflow](DocResumeWorkflow.md) | Resumes a paused or interrupted Documentum workflow identified by a string ID and returns whether the operation succeeded. |
| [DocStartWorkflow](DocStartWorkflow.md) | Initiates a new Documentum workflow process with provided workflow and document information, returning workflow context. |
| [DocStopWorkflow](DocStopWorkflow.md) | Stops an active Documentum workflow given its unique identifier. |

### Search

| Function | Description |
|----------|-------------|
| [DocSearchAsDataset](DocSearchAsDataset.md) | Performs a targeted search within a Documentum repository and returns the matching items as serialized dataset results. |
| [DocSearchFullText](DocSearchFullText.md) | Performs a full-text search on documents and returns matching results as an array. |
| [DocSearchUsingDql](DocSearchUsingDql.md) | Performs a document search using a DQL query and returns matching documents as an array. |

### Documentum Errors

| Function | Description |
|----------|-------------|
| [DocCommandFailed](DocCommandFailed.md) | Checks if the most recent Documentum command resulted in a failure. |
| [DocGetErrorMessage](DocGetErrorMessage.md) | Returns the error message from the most recent Documentum operation exception if one occurred. |

## Email

| Function | Description |
|----------|-------------|
| [SendFromOutbox](SendFromOutbox.md) | Executes all pending email records from the outbox and removes successfully sent entries from the database. |
| [SendLimsEmail](SendLimsEmail.md) | Sends an email via SMTP with support for custom recipients, attachments, HTML content, and optional security. |
| [SendOutlookReminder](SendOutlookReminder.md) | Sends a calendar meeting request as an Outlook-compatible reminder email using the specified SMTP server. |
| [SendToOutbox](SendToOutbox.md) | Logs an email instruction to the outbox database table for later sending via SMTP. |

## Execution & Dynamic Dispatch

| Function | Description |
|----------|-------------|
| [Branch](Branch.md) | Redirects process flow to a specified label during execution. |
| [DoProc](DoProc.md) | Executes a specified procedure by dynamically invoking a named method with provided arguments. |
| [ExecFunction](ExecFunction.md) | Invokes a function by name at runtime with a specified array of arguments, returning the result. |
| [ExecInternal](ExecInternal.md) | Calls a method by name on a specified stored object, passing up to twenty-one arguments, and returns the method's result. |
| [ExecUdf](ExecUdf.md) | Executes a string of SSL code dynamically with optional arguments and result caching. |
| [IIf](IIf.md) | Selects one of two values based on a boolean condition. |
| [LCase](LCase.md) | Returns one of two string values based on a boolean condition. |
| [LimsExec](LimsExec.md) | Executes an external application with optional arguments and user interface visibility. |
| [PrmCount](PrmCount.md) | Returns the number of parameters passed to the currently running procedure. |
| [RunApp](RunApp.md) | Launches an external application with optional arguments and indicates if execution succeeded (or throws on invalid parameters). |

## FTP

| Function | Description |
|----------|-------------|
| [CheckOnFtp](CheckOnFtp.md) | Checks if a specific file exists on an FTP or SFTP server. |
| [CopyToFtp](CopyToFtp.md) | Transfers files to a remote FTP or SFTP server directory with authentication. |
| [DeleteDirOnFtp](DeleteDirOnFtp.md) | Deletes a specified directory from a remote FTP or SFTP server. |
| [DeleteFromFtp](DeleteFromFtp.md) | Deletes a specified file from a remote FTP or SFTP server using supplied credentials. |
| [GetDirFromFtp](GetDirFromFtp.md) | Retrieves directory and file entries from an FTP or SFTP server as an array, matching specific criteria. |
| [GetFromFtp](GetFromFtp.md) | Transfers a file from a remote FTP or SFTP server to a specified local path with authentication. |
| [MakeDirOnFtp](MakeDirOnFtp.md) | Creates a remote directory on an FTP or SFTP server using connection parameters and credentials. |
| [MoveInFtp](MoveInFtp.md) | Moves a file from one location to another on an FTP or SFTP server, supporting optional file renaming and directory changes. |
| [ReadFromFtp](ReadFromFtp.md) | Retrieves the contents of a file from an FTP or SFTP server as a string. |
| [RenameOnFtp](RenameOnFtp.md) | Renames a specified file on a remote FTP or SFTP server and indicates success or failure. |
| [SendToFtp](SendToFtp.md) | Uploads a local file to a specified directory and filename on an FTP or SFTP server. |
| [WriteToFtp](WriteToFtp.md) | Appends text data to a specified file on an FTP or SFTP server. |

## File System

| Function | Description |
|----------|-------------|
| [CombineFiles](CombineFiles.md) | Concatenates the contents of multiple files into a single output file on disk. |
| [Compress](Compress.md) | Applies GZip compression to a string and optionally writes the result to a file. |
| [ConvertReport](ConvertReport.md) | Converts a report file at the given path, returning true on success and raising an error on any failure. |
| [CreateZip](CreateZip.md) | Creates a zip archive from the contents of a specified directory, with optional recursion, file filtering, and password protection. |
| [Decompress](Decompress.md) | Decompresses a compressed string or file and returns its uncompressed string content. |
| [Directory](Directory.md) | Retrieves a filtered array of files and directories matching a specified pattern and attribute flags. |
| [DosSupport](DosSupport.md) | Executes operating system-level file and directory commands, returning results as structured SSL data types. |
| [ExtractZip](ExtractZip.md) | Extracts files and directory structures from a zip archive into a specified target directory, supporting filtering, password protection, and empty directory creation. |
| [FileSupport](FileSupport.md) | Executes file and attribute operations—such as reading, writing, creating, moving, or managing files—based on a flexible request model. |
| [GetAppBaseFolder](GetAppBaseFolder.md) | Returns the application's base folder path as a string for use in file and configuration operations. |
| [GetAppWorkPathFolder](GetAppWorkPathFolder.md) | Returns the path to the application's working directory as a string. |
| [GetFileVersion](GetFileVersion.md) | Retrieves the version information string from a specified file. |
| [GetLogsFolder](GetLogsFolder.md) | Returns the absolute path to the user's log folder as a string, including a trailing directory separator for safe file operations. |
| [GetWebFolder](GetWebFolder.md) | Retrieves the path to the web resources folder for the running application context. |
| [LDir](LDir.md) | Retrieves an array of file and directory names matching a specified pattern and optional attribute filter. |
| [ReadBytesBase64](ReadBytesBase64.md) | Reads the contents of a specified file and returns a base64-encoded string representation. |
| [ReadText](ReadText.md) | Retrieves text content from a file in memory, allowing partial reads and encoding selection. |
| [WriteBytesBase64](WriteBytesBase64.md) | Writes binary data, decoded from a base64 string, to a specified file path. |
| [WriteText](WriteText.md) | Writes text content to a file, either creating, overwriting, or appending as specified. |

## Inline Code

| Function | Description |
|----------|-------------|
| [DeleteInlineCode](DeleteInlineCode.md) | Removes a named inline code entry from the current execution context if it exists. |
| [Eval](Eval.md) | Invokes a code block value with the supplied arguments and returns whatever the block evaluates to. |
| [GetInlineCode](GetInlineCode.md) | Retrieves an inline code block as a string with specified variables replaced by their current values. |
| [GetRegion](GetRegion.md) | Retrieves a named string constant ("region") from a shared dictionary and optionally substitutes substrings using mapping arrays. |
| [GetRegionEx](GetRegionEx.md) | Performs a region lookup by name, applying optional string replacements and supporting local region overrides using parameters s, src, dst, and localRegions. |

## Messaging & Errors

| Function | Description |
|----------|-------------|
| [ClearLastSSLError](ClearLastSSLError.md) | Clears the system-wide SSL error state and confirms completion with a boolean value. |
| [ErrorMes](ErrorMes.md) | Logs an error message with contextual information and returns the combined result as a string. |
| [FormatErrorMessage](FormatErrorMessage.md) | Returns a formatted string description for an error value. |
| [FormatSqlErrorMessage](FormatSqlErrorMessage.md) | Returns a human-readable error message from a SQL error value. |
| [GetLastSSLError](GetLastSSLError.md) | Retrieves the most recent SSL error encountered during the current process. |
| [InfoMes](InfoMes.md) | Writes an informational message to the user log; behaviorally identical to UsrMes. |
| [RaiseError](RaiseError.md) | Raises a runtime error with a specified message, halting normal code execution and recording error details for handling. |
| [UsrMes](UsrMes.md) | Logs a user message with contextual metadata and returns the formatted string. |

## Numeric & Math

| Function | Description |
|----------|-------------|
| [Abs](Abs.md) | Calculates the non-negative value of a number, removing any sign. |
| [GetDecimalSep](GetDecimalSep.md) | Returns the current decimal separator character as its byte value. |
| [GetDecimalSeparator](GetDecimalSeparator.md) | Returns the current decimal separator character defined in the system or application configuration. |
| [GetGroupSeparator](GetGroupSeparator.md) | Returns the current group separator character used for formatting numbers as a string. |
| [IsNumeric](IsNumeric.md) | Determines if a value represents a valid numeric string, optionally allowing hexadecimal format. |
| [LimsXOr](LimsXOr.md) | Performs a bitwise exclusive OR operation on two integer numbers and returns the result. |
| [MatFunc](MatFunc.md) | Calculates a mathematical operation on a given number based on the specified function name. |
| [Max](Max.md) | Calculates the greater of two values, supporting numbers, strings, and dates. |
| [Min](Min.md) | Returns the lesser of two strings, numbers, or dates as defined by their type-specific comparison rules. |
| [Rand](Rand.md) | Generates a random number, optionally using the provided seed to produce a repeatable sequence. |
| [Round](Round.md) | Rounds a numeric value to a specific number of decimal places using a configurable midpoint handling strategy. |
| [RoundPoint5](RoundPoint5.md) | Rounds a number to the nearest half-point value. |
| [Scient](Scient.md) | Converts a number to its scientific notation string representation. |
| [SetDecimalSeparator](SetDecimalSeparator.md) | Sets the character used as the decimal separator for all numeric formatting and parsing operations. |
| [SetGroupSeparator](SetGroupSeparator.md) | Changes the group (thousands) separator character used when numbers are formatted as strings across the application. |
| [SigFig](SigFig.md) | Produces a string by rounding a number to a specified count of significant digits according to a selected rounding standard. |
| [Sqrt](Sqrt.md) | Calculates the positive square root of a given number. |
| [StdRound](StdRound.md) | Returns a string representation of a number rounded to a specified number of digits using a named industry or regulatory rounding standard. |
| [ToScientific](ToScientific.md) | Converts a numeric value to its scientific notation string representation with customizable decimal places. |
| [ValidateNumeric](ValidateNumeric.md) | Validates whether a string accurately represents a numeric value based on SSL conventions. |
| [_AND](_AND.md) | Performs a bitwise AND operation between two integer numbers and returns the result. |
| [_NOT](_NOT.md) | Performs bitwise complement on an integer number (fractional values are rejected, not truncated). |
| [_OR](_OR.md) | Performs a bitwise OR operation on two integer values and returns the result as a number. |
| [_XOR](_XOR.md) | Calculates the bitwise exclusive OR of two integer-valued numbers and returns the result. |

## Object & Interop

| Function | Description |
|----------|-------------|
| [AddProperty](AddProperty.md) | Adds one or more properties with empty string values to an object. |
| [CreateUdObject](CreateUdObject.md) | Creates a dynamic object with properties defined at runtime based on the input arguments. |
| [EndLimsOleConnect](EndLimsOleConnect.md) | Releases a LIMS OLE connection by disposing it and confirming disconnection. |
| [GetInternal](GetInternal.md) | Retrieves the value of a specified property from an object without modifying it. |
| [GetInternalC](GetInternalC.md) | Retrieves a nested value from an object or collection using a specified path of indexes. |
| [HasProperty](HasProperty.md) | Checks whether a given object contains a specified property. |
| [LimsNETConnect](LimsNETConnect.md) | Instantiates a new .NET object or accesses a .NET type for use within SSL, with optional parameterization and support for static access. |
| [LimsOleConnect](LimsOleConnect.md) | Creates and returns an active instance of a native OLE or COM object by ProgID for use in SSL. |
| [MakeNETObject](MakeNETObject.md) | Converts an SSL value to a .NET-compatible object, enabling interaction with .NET APIs from SSL. |
| [SetInternal](SetInternal.md) | Assigns a new value to a named property on an object and returns `NIL`. |
| [SetInternalC](SetInternalC.md) | Updates a value within an object's internal collection at specified indices. |
| [XmlDomToUdObject](XmlDomToUdObject.md) | Converts an XML string into a dynamic object structure representing the XML document. |

## Security

| Function | Description |
|----------|-------------|
| [ChkNewPassword](ChkNewPassword.md) | Validates that a proposed password has not been used previously. |
| [ChkPassword](ChkPassword.md) | Validates a user's credentials against the password store and authentication logic. |
| [DecryptData](DecryptData.md) | Decrypts an encrypted string using a provided password and returns the decrypted value as a string. |
| [EncryptData](EncryptData.md) | Encrypts a string with a password using one of the legacy built-in algorithms (RC2, DES, 3DES) and returns the result as a hex or base64 string. |
| [GetUserData](GetUserData.md) | Returns the username of the currently authenticated user as a string. |
| [HashData](HashData.md) | Computes a cryptographic hash string from the input string using a selected algorithm. |
| [LDAPAuth](LDAPAuth.md) | Performs user credential authentication against an LDAP directory server and returns the authentication result. |
| [LDAPAuthEX](LDAPAuthEX.md) | Authenticates a user against an LDAP server with advanced search and attribute retrieval options. |
| [SearchLDAPUser](SearchLDAPUser.md) | Searches a directory server for a specific user and returns their distinguished name. |
| [SetUserData](SetUserData.md) | Updates the current user name in the session context for the application. |
| [SetUserPassword](SetUserPassword.md) | Updates a user's password and returns the resulting password hash. |
| [VerifySignature](VerifySignature.md) | Validates that a data string has been signed by the private key corresponding to a provided X.509 certificate. |

## String

| Function | Description |
|----------|-------------|
| [AllTrim](AllTrim.md) | Removes all leading and trailing spaces from a string. |
| [Asc](Asc.md) | Returns the ASCII code of the first character in a string. |
| [At](At.md) | Finds the first occurrence of a specified substring within a source string and returns its one-based position. |
| [BuildString](BuildString.md) | Concatenates trimmed string representations of array elements into a single string with a specified delimiter. |
| [BuildString2](BuildString2.md) | Concatenates a two-dimensional array into a delimited string with customizable line and column separators. |
| [Chr](Chr.md) | Converts a numeric ASCII code to its corresponding single-character string. |
| [CreateGUID](CreateGUID.md) | Generates a new globally unique identifier as an uppercase string. |
| [HtmlDecode](HtmlDecode.md) | Converts HTML-encoded text into its plain, readable string representation. |
| [HtmlEncode](HtmlEncode.md) | Encodes special characters in a string as HTML entities for safe use in HTML content. |
| [IsGuid](IsGuid.md) | Validates whether a string conforms to the GUID format and indicates validity as a boolean. |
| [IsHex](IsHex.md) | Validates whether a string contains only uppercase hexadecimal characters (0-9 and A-F). |
| [LLower](LLower.md) | Converts all characters in a string to their lowercase equivalents. |
| [LStr](LStr.md) | Converts a numeric value to a trimmed string, or returns "NIL" for `NIL` input. |
| [LToHex](LToHex.md) | Converts a string or integer to its hexadecimal string representation. |
| [LTrim](LTrim.md) | Removes leading whitespace from a string, returning NIL if the input is empty or contains only whitespace. |
| [Left](Left.md) | Extracts a substring from the start of a string up to a specified length, or returns `NIL` if the length is zero or negative. |
| [Len](Len.md) | Calculates the length of a string or the number of elements in an array. |
| [LimsAt](LimsAt.md) | Returns the 1-based position of a substring within a string, starting from a specified 1-based offset, or 0 if not found. |
| [LimsString](LimsString.md) | Converts any value to a LIMS-formatted string, returning "NIL" for `NIL` inputs. |
| [Lower](Lower.md) | Converts all characters in a string to lowercase. |
| [MimeDecode](MimeDecode.md) | Decodes MIME-encoded data to its plain string representation. |
| [MimeEncode](MimeEncode.md) | Converts a string into its MIME-encoded form for safe transmission and storage in contexts that require text to be encoded. |
| [Rat](Rat.md) | Returns the one-based position of the last occurrence of a substring within a source string. |
| [Replace](Replace.md) | Replaces all occurrences of a specified substring within a string with another substring and returns the resulting string. |
| [Replicate](Replicate.md) | Creates a string by repeating the source string a specified number of times. |
| [Right](Right.md) | Extracts a specified number of characters from the end of a string. |
| [Str](Str.md) | Converts a number to a string with optional total length and decimal formatting. |
| [StrSrch](StrSrch.md) | Identifies the 1-based position of a substring within another string, allowing for flexible search modes. |
| [StrTran](StrTran.md) | Replaces all occurrences of a specified substring with another substring in a source string. |
| [StrZero](StrZero.md) | Formats a number as a string with leading zeros, optional length, and decimal precision. |
| [SubStr](SubStr.md) | Extracts a substring from a string starting at a 1-based position and for a specified number of characters. |
| [Trim](Trim.md) | Removes trailing whitespace characters from a string. |
| [Upper](Upper.md) | Converts all characters in a string to uppercase. |
| [UrlDecode](UrlDecode.md) | Converts a URL-encoded string into its decoded, human-readable form. |
| [UrlEncode](UrlEncode.md) | Converts a string into a format safe for inclusion in a URL by encoding unsafe characters. |

## System & Batch

| Function | Description |
|----------|-------------|
| [GetPrinters](GetPrinters.md) | Returns a list of printer names currently installed on the system. |
| [InBatchProcess](InBatchProcess.md) | Checks whether the current execution context is operating in batch process mode. |
| [IsProductionModeOn](IsProductionModeOn.md) | Identifies whether the current application environment is configured as production. |
| [LWait](LWait.md) | Blocks further script execution for a specified number of seconds and returns an empty string. |
| [SubmitToBatch](SubmitToBatch.md) | Submits source code for batched processing and returns an identifier or batch result. |
| [SubmitToBatchEx](SubmitToBatchEx.md) | Submits code to a batch job processor and returns a batch job identifier as a string. |

## Type Conversion

| Function | Description |
|----------|-------------|
| [Empty](Empty.md) | Determines whether a value is considered empty, returning a boolean result. |
| [FromJson](FromJson.md) | Parses a JSON string into equivalent SSL-native values or returns the input unchanged if not a string. |
| [FromXml](FromXml.md) | Parses an XML string and converts it to the corresponding SSL value, inferring type and structure from XML content. |
| [Integer](Integer.md) | Truncates the fractional part of a number and returns the nearest integer value toward zero. |
| [LFromHex](LFromHex.md) | Converts a hexadecimal-encoded string into its ASCII string representation. |
| [LHex2Dec](LHex2Dec.md) | Converts a hexadecimal number string to its decimal string representation. |
| [LTransform](LTransform.md) | Converts an expression to a string using a custom numeric formatting pattern. |
| [LimsNETCast](LimsNETCast.md) | Converts a given value to a specified target type, such as enum, reference, number, or array, according to the instructions in the type string. |
| [LimsNETTypeOf](LimsNETTypeOf.md) | Resolves a type name to its corresponding .NET type object for dynamic operations. |
| [LimsType](LimsType.md) | Identifies the SSL type code for a value referenced by a string parameter. |
| [LimsTypeEx](LimsTypeEx.md) | Returns the SSL type name of a given value as a string. |
| [Nothing](Nothing.md) | Returns true when val is `NIL`, empty, or stringifies to "0"; otherwise returns false. |
| [ToJson](ToJson.md) | Serializes a value to its JSON string representation. |
| [ToNumeric](ToNumeric.md) | Converts a string to a numeric value, with optional hexadecimal support. |
| [ToXml](ToXml.md) | Converts an input value to its XML string representation for serialization and data exchange. |
| [Val](Val.md) | Converts a string containing numeric characters into a number. |

## Variable & Session Management

| Function | Description |
|----------|-------------|
| [AddToSession](AddToSession.md) | Stores a specified value under a named key in the session for later retrieval within the same user context. |
| [ClearSession](ClearSession.md) | Removes all values and resets state in the current session context. |
| [CreateLocal](CreateLocal.md) | Assigns a value to a local variable identified by any input, with scope limited to the current runtime session. |
| [CreatePublic](CreatePublic.md) | Creates or updates a public variable that can be accessed by name across different program modules. |
| [GetByName](GetByName.md) | Retrieves the value of a variable by name from local or public storage. |
| [GetFromApplication](GetFromApplication.md) | Returns a comma-separated list of connected usernames when given the key 'STARLIMSUSERS' in CUSTOM session mode, or `NIL`/empty for other conditions. |
| [GetFromSession](GetFromSession.md) | Retrieves the value associated with a specified key from the current user session. |
| [GetSetting](GetSetting.md) | Retrieves the value of a named application or environment setting. |
| [GetSettings](GetSettings.md) | Retrieves multiple configuration setting values for provided setting names. |
| [IsDefined](IsDefined.md) | Determines if a variable with the given name exists in the current scope, returning true or false. |
| [LKill](LKill.md) | Deletes a public variable from the runtime session by name and returns an empty string. |
| [SetByName](SetByName.md) | Assigns a value to a local or public variable by its name at runtime, creating it if permitted. |
