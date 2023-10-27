import json
'''
Feed the output of this to the python script
SELECT TABLE_SCHEMA
	,TABLE_NAME
	,COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'wotaapi'
FOR JSON AUTO
'''

json_input = ""

  # Parse JSON
  data = json.loads(json_data)

  # Create a dictionary with tables and their columns
  tables = {}
  for item in data:
      table_name = item['TABLE_NAME']
      column_name = item['COLUMN_NAME']
      if table_name not in tables:
          tables[table_name] = []
      tables[table_name].append(column_name)

  # Identify relationships based on column names
  relationships = []
  table_names = list(tables.keys())
  for i in range(len(table_names)):
      for j in range(i+1, len(table_names)):
          common_columns = set(tables[table_names[i]]) & set(tables[table_names[j]])
          for col in common_columns:
              relationships.append((table_names[i], table_names[j], col))

  # Construct MERMAID syntax
  mermaid_syntax = "classDiagram\n"
  for table, columns in tables.items():
      mermaid_syntax += f"  class {table} {{\n"
      for col in columns:
          if any(rel for rel in relationships if col == rel[2]):
              mermaid_syntax += f"    <b>{col}</b>\n"
          else:
              mermaid_syntax += f"    {col}\n"
      mermaid_syntax += "  }\n"

  for rel in relationships:
      mermaid_syntax += f"  {rel[0]} -- {rel[1]} : <b>{rel[2]}</b>\n"
