import pyodbc

# Define parameters to connect to server
server = "untitledtravel.database.windows.net"
database = 'VenueDB'
username = "untitled"
password = "Unt1tled.final"
driver= '{ODBC Driver 17 for SQL Server}'

# Establish a connection
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()

# Execute a query
f = open("testQuery.sql", "r")
cursor.execute(f.read())#    <--- COMMAND GOES HERE ###
f.close()
print("Cursor object:", cursor)
row = cursor.fetchone()
print("Fetch:")
print(row)
print("Fetch again:")
print(cursor.fetchone())
print("Fetch again:")
print(cursor.fetchone())
