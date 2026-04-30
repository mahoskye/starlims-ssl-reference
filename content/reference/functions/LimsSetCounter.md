---
title: "LimsSetCounter"
summary: "Generates the next counter value and, when given matching field and value arrays, inserts a new row with that key."
id: ssl.function.limssetcounter
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsSetCounter

Generates the next counter value and, when given matching field and value arrays, inserts a new row with that key.

`LimsSetCounter` gets the next value for a counter identified by `sTableName`, `sFieldName`, and an optional `sPrefix`. It always returns the numeric counter value. When `aFields` and `aValues` are both supplied and have the same length, the function also inserts a new row into `sTableName`, using the generated key for `sFieldName` plus the additional columns from `aFields`.

If `sPrefix` is supplied, the inserted value for `sFieldName` is the prefix concatenated with the generated number, while the function still returns the numeric part. If `sTableName` or `sFieldName` is [`NIL`](../literals/nil.md), the function returns `0` immediately.

## When to use

- When you need the next numeric counter value for a table field.
- When you want to insert a row immediately after generating that value.
- When you need separate counter streams for the same table and field by using different prefixes.

## Syntax

```ssl
LimsSetCounter(sTableName, sFieldName, [sPrefix], [aFields], [aValues], [nIncrementWith])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sTableName` | [string](../types/string.md) | yes | — | Target table name. The generated key is inserted into this table when the field and value arrays match. |
| `sFieldName` | [string](../types/string.md) | yes | — | Column that receives the generated key value. |
| `sPrefix` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Optional counter qualifier. When supplied, the inserted key becomes `sPrefix + nextNumber`. |
| `aFields` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Additional column names to include in the insert. Do not repeat `sFieldName` here. |
| `aValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Values for `aFields`, in the same order. |
| `nIncrementWith` | [number](../types/number.md) | no | `1` | Optional whole-number increment. Non-integer values do not change the default behavior. |

## Returns

**[number](../types/number.md)** — The generated numeric counter value.

## Best practices

!!! success "Do"
    - Pass only additional insert columns in `aFields`; `sFieldName` is inserted automatically.
    - Keep `aFields` and `aValues` aligned by position and length.
    - Check for a `0` return when the counter cannot be generated.
    - Wrap calls in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the inputs or database state may be unreliable.

!!! failure "Don't"
    - Put `sFieldName` in `aFields`; that produces a duplicate insert column.
    - Assume empty strings are treated the same as [`NIL`](../literals/nil.md); only [`NIL`](../literals/nil.md) table or field arguments short-circuit to `0` before work starts.
    - Assume mismatched arrays will still insert a partial row; the function skips the insert when the array lengths differ.
    - Assume an insert failure always means the generated number can be reused; some environments may still consume the next counter value.

## Caveats

- If `aFields` and `aValues` have different lengths, the counter value is still generated, but the row insert is skipped.
- `nIncrementWith` affects how far the stored counter advances, but the returned numeric value is still the first value from that reserved range.
- Insert-failure handling is not identical in every deployment. Do not assume the generated number was rolled back unless you have verified that behavior in your environment.

## Examples

### Insert a new row with an auto-generated key

Call `LimsSetCounter` with a table, field name, and an additional field/value pair to insert a new row and retrieve the generated key in one step.

```ssl
:PROCEDURE InsertSampleWithAutoID;
	:DECLARE nNewSampleID, aFields, aValues;

	aFields := {"sample_name", "status_id"};
	aValues := {"QC-Batch-047", "A"};

	nNewSampleID := LimsSetCounter("SAMPLES", "sample_id",, aFields, aValues);

	UsrMes("Created sample ID: " + LimsString(nNewSampleID));

	:RETURN nNewSampleID;
:ENDPROC;

/* Usage;
DoProc("InsertSampleWithAutoID");
```

[`UsrMes`](UsrMes.md) displays:

```text
Created sample ID: <n>
```

### Use a prefix to maintain separate counter streams

Pass different `sPrefix` values to maintain independent counter streams for the same table and field. Each prefix increments its own counter sequence.

```ssl
:PROCEDURE GenerateProjectSamples;
	:DECLARE sTableName, sFieldName, aFields;
	:DECLARE sProjectAlpha, sProjectBeta, aValuesAlpha, aValuesBeta;
	:DECLARE nNextAlpha, nNextBeta;

	sTableName := "WORKLIST";
	sFieldName := "WORK_ID";
	aFields := {"PROJECT_CODE"};

	sProjectAlpha := "ALPHA";
	sProjectBeta := "BETA";

	aValuesAlpha := {sProjectAlpha};
	aValuesBeta := {sProjectBeta};

	nNextAlpha := LimsSetCounter(sTableName, sFieldName, sProjectAlpha, aFields,
		aValuesAlpha);
	nNextBeta := LimsSetCounter(sTableName, sFieldName, sProjectBeta, aFields, aValuesBeta);

	UsrMes("Generated: " + sProjectAlpha + LimsString(nNextAlpha));
	/* Displays generated ALPHA key;
	UsrMes("Generated: " + sProjectBeta + LimsString(nNextBeta));
	/* Displays generated BETA key;
:ENDPROC;

/* Usage;
DoProc("GenerateProjectSamples");
```

### Insert a full row with error handling

Wrap `LimsSetCounter` in a [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) block and check for a `0` return to handle both counter failure and database errors.

```ssl
:PROCEDURE InsertComplexSubmission;
	:DECLARE sTableName, sFieldName, sPrefix, sSubmissionID;
	:DECLARE aFields, aValues, nCounter, oErr, dSubmitDate;

	sTableName := "SUBMISSIONS";
	sFieldName := "SUBMISSION_ID";
	sPrefix := "SUB";
	dSubmitDate := Today();

	aFields := {"SUBMITTER", "LAB_CODE", "STATUS", "SUBMIT_DATE"};
	aValues := {"JSmith", "LAB-A", "P", dSubmitDate};

	:TRY;
		nCounter := LimsSetCounter(sTableName, sFieldName, sPrefix, aFields, aValues, 1);

		:IF nCounter == 0;
			ErrorMes("Submission was not created");
			:RETURN .F.;
		:ENDIF;

		sSubmissionID := sPrefix + LimsString(nCounter);
		UsrMes("Submission created: " + sSubmissionID);
		/* Displays created submission ID;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("Failed to create submission: " + oErr:Description);
		/* Displays on failure: submission creation failed;
		:RETURN .F.;
	:ENDTRY;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("InsertComplexSubmission");
```

## Related

- [`RunSQL`](RunSQL.md)
- [`SQLExecute`](SQLExecute.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
- [`array`](../types/array.md)
