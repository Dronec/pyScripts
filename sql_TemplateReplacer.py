fields = ['AssetNo'
      ,'WorkOrder'
      ,'DateCompleted'
      ]
output = "@template"
for field in fields:
    output = f"REPLACE({output},'%{field}%',{field})"
print(output)
