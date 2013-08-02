#!/usr/bin/python
# Generate an ARFF nominal list for use in ARFF header


#Enter database info here
host = "localhost"
user = "root"
password = "coolio"
db = "datamining"
table = "cand2008"
attribute = "party"

#tha code
import MySQLdb as mdb

con = None

con = mdb.connect(host, user, password, db)

cur = con.cursor(mdb.cursors.DictCursor)

q = "SELECT "+attribute+" FROM "+table+" GROUP BY "+attribute+";"
cur.execute(q)
rows = cur.fetchall()

first = 0
s = ''
for row in rows:
  if first:
    s = row[attribute]
  else:
    s = s +","+row[attribute]

nomstr = "{%s}" % s

print nomstr
