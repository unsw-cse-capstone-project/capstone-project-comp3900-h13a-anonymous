import sqlite3

conn = sqlite3.connect('hermes.db')
print ("Opened database successfully")

conn.execute('''CREATE TABLE STOCK
         (CODE TEXT PRIMARY KEY NOT NULL,
         PRICE             REAL NOT NULL,
         TIMESTAMP      INTEGER NOT NULL,
         VLOUMN           REAL);''')
print ("Table created successfully")

conn.commit()
conn.close()