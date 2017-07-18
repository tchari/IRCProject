import sqlite3

sqldb = 'db.sqlite3'
conn = sqlite3.connect(sqldb)
c = conn.cursor()

query = "SELECT name FROM sqlite_master WHERE type='table';"
#query = "PRAGMA table_info("+tablename+");"
#query = "SELECT * FROM "+tablename
c.execute(query)
vals = c.fetchall()
for i in vals:
        print(i)

conn.close()
