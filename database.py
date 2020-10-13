import sqlite3

conn = sqlite3.connect('hermes.db')
print("Opened database successfully")

conn.execute('''DROP TABLE STOCK''')
conn.execute('''DROP TABLE USER''')
conn.execute('''DROP TABLE WATCHLIST''')
conn.execute('''DROP TABLE PURCHASE''')

conn.execute('''CREATE TABLE STOCK
         (CODE TEXT PRIMARY KEY NOT NULL,
         PRICE             REAL NOT NULL,
         TIMESTAMP      INTEGER NOT NULL,
         VLOUMN           REAL);''')
print("Stock table created successfully")

conn.execute('''CREATE TABLE USER
         (ID INTEGER PRIMARY KEY autoincrement,
         EMAIL              TEXT NOT NULL UNIQUE,
         PASSWORD           TEXT NOT NULL,
         PHONE           INTEGER NOT NULL UNIQUE,
         BALANCE            REAL NOT NULL,
         NAME               TEXT NOT NULL,
         LOGIN              TEXT NOT NULL,
         LOGOUT             TEXT NOT NULL);''')
print("User table created successfully")

conn.execute('''CREATE TABLE WATCHLIST
         (ID                 INTEGER NOT NULL,
         CODE                TEXT NOT NULL,
         DATEADD             TEXT,
         FOREIGN KEY (ID) REFERENCES USER (ID),
         FOREIGN KEY (CODE) REFERENCES STOCK (CODE));''')
print("Watchlist table created successfully")

conn.execute('''CREATE TABLE PURCHASE
         (ID                 INTEGER NOT NULL UNIQUE,
         CODE                TEXT NOT NULL,
         DATEBUY             DATE,
         DATESELL            DATE,
         UNITBUY             REAL,
         UNITSELL            REAL,
         FOREIGN KEY (ID) REFERENCES USER (ID),
         FOREIGN KEY (CODE) REFERENCES STOCK (CODE));''')
print("Purchase table created successfully")

conn.commit()
conn.close()
