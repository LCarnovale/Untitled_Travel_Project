import pyodbc
server = "untitledtravel.database.windows.net"
database = 'VenueDB'
username = "untitled"
password = "Unt1tled.final"
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM dbo.dbTable")# XXX: COMMAND GOES HERE
row = cursor.fetchone()
print(row)