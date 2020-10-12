import sqlite3

conn = sqlite3.connect('hermes.db')
print ("Opened database successfully")

conn.execute('''DROP TABLE STOCK''')
conn.execute('''DROP TABLE USER''')

conn.execute('''CREATE TABLE STOCK
         (CODE TEXT PRIMARY KEY NOT NULL,
         PRICE             REAL NOT NULL,
         TIMESTAMP      INTEGER NOT NULL,
         VLOUMN           REAL);''')
print ("Stock table created successfully")

conn.execute('''CREATE TABLE USER
         (ID INTEGER PRIMARY KEY autoincrement,
         EMAIL              TEXT NOT NULL,
         PASSWORD           TEXT NOT NULL,
         PHONE           INTEGER NOT NULL,
         BALANCE            REAL NOT NULL,
         NAME               TEXT NOT NULL,
         LOGIN              TEXT NOT NULL,
         LOGOUT             TEXT NOT NULL);''')
print ("User table created successfully")
conn.commit()
conn.close()