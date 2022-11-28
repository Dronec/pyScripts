# This simple script generates a single MS SQL query for managing SCD2 dimension. Just update the setup section and you're good to go
# setup
sourceTable = 'stg.users'
dimTable = 'DW.dim_Users'
businessKey = 'RIW'
updateSource = "'Active Directory'" # contents for UpdateBy column
maxDate = "'9999-12-31'"
emptyString = "''"
attributes = ['UserName','Employer','Title','Phone']
granularity = 'MINUTE' #The EffectiveTo timestamp equals NOW - 1 * granularity. Set it to DAY if you expect daily updates only
# output
output = f'INSERT INTO {dimTable}\n({businessKey},{",".join(attributes)},EffectiveFrom,EffectiveTo,IsCurrent,UpdateDate,UpdateBy)\n'
output = output + \
    f'SELECT {businessKey},{",".join(attributes)},EffectiveFrom,EffectiveTo,1,GETDATE(),{updateSource}\nFROM (\n'
output = output + f'MERGE INTO {dimTable} AS target USING (\n'
output = output + \
    f'SELECT {businessKey},{",".join(attributes)}\nFROM {sourceTable})\nAS source({businessKey},{",".join(attributes)})\n'
output = output + f'ON (target.{businessKey} = source.{businessKey})\n'
output = output + \
    f'WHEN MATCHED and target.IsCurrent = 1 and ({" OR ".join([f"ISNULL(target.{x},{emptyString}) != ISNULL(source.{x},{emptyString})" for x in attributes])})\n'
output = output + \
    f'THEN UPDATE	SET EffectiveTo = DATEADD({granularity},-1,getdate()), IsCurrent = 0, UpdateDate = getdate(),UpdateBy = {updateSource}\n'
output = output + \
    f'WHEN NOT MATCHED THEN INSERT \n({businessKey},{",".join(attributes)},EffectiveFrom,EffectiveTo,IsCurrent,UpdateDate,UpdateBy)\nVALUES(source.{businessKey},{",".join([f"source.{x}" for x in attributes])},GETDATE(),{maxDate},1,GETDATE(),{updateSource})'
output = output + \
    f"OUTPUT $ACTION action,source.{businessKey},{','.join([f'source.{x}' for x in attributes])},GETDATE() EffectiveFrom,{maxDate} EffectiveTo) n\nWHERE n.action = 'UPDATE';"

print(output)
