
# To connect to a SQL Server database and execute a stored procedure in Python using the pyodbc library, you can modify the previous example. Here's an example of how to execute a stored procedure:
import pyodbc
# private const string SqlConnectionString = "Server=database-1.ctok6v46po4w.us-east-1.rds.amazonaws.com,1433;Database=ADETAB_DB;User Id=Admin;Password=MoAdeTab987!;Integrated Security=false;Connect Timeout=3600;";
# Replace these values with your SQL Server credentials and connection details
server = 'database-1.ctok6v46po4w.us-east-1.rds.amazonaws.com'
database = 'ADETAB_DB'
username = 'Admin'
password = 'MoAdeTab987!'
table_name = 'malik'



connection_string2 = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection2 = pyodbc.connect(connection_string2)
cursor2 = connection2.cursor()
#READ AND RETURN THE DATA FROM TABLE CREATED BY PROC
query2 = f'SELECT * FROM adetab_db.adetab_schema.avgs'
# query = f'EXEC ADETAB_DB.ADETAB_SCHEMA.find_players 1'
cursor2.execute(query2)
# Fetch all the rows from the result set
rows = cursor2.fetchall()
# Display the column names
columns = [column[0] for column in cursor2.description]
print(columns)
# Display the data
for row in rows:
    print(row)
cursor2.close()
connection2.close()