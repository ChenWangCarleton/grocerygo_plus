import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "readwrite_0",
    passwd = "readwrite",
)

my_cursor = mydb.cursor()
my_cursor.execute("show databases")
for db in my_cursor:
    print(db)