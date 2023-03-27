# In case if you need to generate a script to remove duplicates from an arbitrary table
# Step 1: Generate a dictionary from that table
"""
DECLARE @TableName VARCHAR(100) = 'dbo.MyTable'
DECLARE @ResultString NVARCHAR(MAX) = '{';

SELECT @ResultString = @ResultString + '"' + COLUMN_NAME + '":"' + CASE 
		WHEN DATA_TYPE IN (
				'varchar'
				,'char'
				,'nvarchar'
				,'nchar'
				,'text'
				,'ntext'
				)
			THEN ''
		WHEN DATA_TYPE IN (
				'tinyint'
				,'smallint'
				,'int'
				,'bigint'
				,'float'
				,'real'
				,'decimal'
				,'numeric'
				)
			THEN '0'
		WHEN DATA_TYPE IN (
				'date'
				,'time'
				,'datetime'
				,'datetime2'
				,'smalldatetime'
				)
			THEN '1900-01-01'
		END + '",'
FROM INFORMATION_SCHEMA.COLUMNS
WHERE CONCAT_WS('.', TABLE_SCHEMA, TABLE_NAME) = @TableName

-- Remove the trailing comma
SET @ResultString = LEFT(@ResultString, LEN(@ResultString) - 1) + '}'

SELECT @ResultString AS Result
"""
# Step 2: use that dictionary as a parameter

defaults = {"columnName1":"defaultValue1","columnName2":"defaultValue2","columnNameN":"defaultValueN"}
table = 'dbo.MyTable'
columns = [f"[{str(val)}]" for val in list(defaults.keys())]
values = [f"'{str(val)}'" for val in list(defaults.values())]

# Generate the SQL script
sql_script = f"""WITH IncomingRecords
AS (
    SELECT id, {', '.join(columns)}
    FROM {table}
    WHERE ProcessedDate IS NULL
),
ProcessedRecords
AS (
    SELECT id, {', '.join(columns)}
    FROM {table}
)
DELETE i
FROM IncomingRecords i
JOIN ProcessedRecords p ON {' AND '.join([f'ISNULL(i.{col},{val}) = ISNULL(p.{col},{val})' for col, val in zip(columns, values)])}
    AND i.id != p.id"""

print(sql_script)
