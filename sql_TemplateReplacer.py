fields = ['AssetNo'
      ,'WorkOrder'
      ,'DateCompleted'
      ,'FromPoint'
      ,'ToPoint'
      ,'Note']
output = "@template"
outputxml = ""
c = 1
for field in fields:
    output = f"REPLACE({output},'%{field}%',{field})"
    outputxml = outputxml+f'<PromptData sequence="{c}">%{field}%</PromptData>\n'
    c=c+1
print(output)
print(outputxml)
