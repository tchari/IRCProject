import sqlite3

sqldb = 'db.sqlite3'
conn = sqlite3.connect(sqldb)
c = conn.cursor()



#query = "SELECT name FROM sqlite_master WHERE type='table';"
#query = "PRAGMA table_info("+tablename+");"
#query = "SELECT * FROM "+tablename

TYPEtablename = 'IRC_assessmenttype'
type_vals = " VALUES (1,'Fire');"
query = "INSERT INTO " + TYPEtablename + type_vals;
c.execute(query)
conn.commit()

COPtablename = 'IRC_costofprotection'
cop_vals = " VALUES (1,'Sprinkler', 30, 0.13, 70000, 1, 0, 1000, 0, 1), (2,'Fire Truck', 30, 0.13, 1300000, 20, 10000, 350, 0, 1);"
query = "INSERT INTO " + COPtablename + cop_vals;
c.execute(query)
conn.commit()

UNITtablename = 'IRC_unit'
unit_vals = " VALUES (1,'Maintenance Building', 'none', 'Buildings', 0.0025, 2500000);"
query = "INSERT INTO " + UNITtablename + unit_vals;
c.execute(query)
conn.commit()

#vals = c.fetchall()
#for i in vals:
#        print(i)

conn.close()
