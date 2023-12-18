
# To connect to a SQL Server database and execute a stored procedure in Python using the pyodbc library, you can modify the previous example. Here's an example of how to execute a stored procedure:
import pyodbc
import json
# private const string SqlConnectionString = "Server=database-1.ctok6v46po4w.us-east-1.rds.amazonaws.com,1433;Database=ADETAB_DB;User Id=Admin;Password=MoAdeTab987!;Integrated Security=false;Connect Timeout=3600;";
# Replace these values with your SQL Server credentials and connection details
server = 'database-1.ctok6v46po4w.us-east-1.rds.amazonaws.com'
database = 'ADETAB_DB'
username = 'Admin'
password = 'MoAdeTab987!'
table_name = 'malik'

connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

#EXECUTE THE PROC
cmd_prod_executesp = """exec ADETAB_DB.ADETAB_SCHEMA.find_players 1 """
connection.autocommit = True
cursor.execute(cmd_prod_executesp)
cursor.close()
connection.close()

connection_string2 = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection2 = pyodbc.connect(connection_string2)
cursor2 = connection2.cursor()

#READ AND RETURN THE DATA FROM TABLE CREATED BY PROC
query2 = f'SELECT * FROM ADETAB_DB.ADETAB_SCHEMA.json_final'

# query = f'EXEC ADETAB_DB.ADETAB_SCHEMA.find_players 1'
cursor2.execute(query2)

# Fetch all the rows from the result set
rows = cursor2.fetchall()

edited_row = ''

for row in rows:
    row = str(row)
    len = len(row)
    edited_row = row[3:(len-4)]
cursor2.close()
connection2.close()

edited_row = "[" + edited_row + "]"

data_list = json.loads(edited_row)
