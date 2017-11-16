#!/usr/bin/python
import MySQLdb

hostname = "tdf-analytics.c9sxquz8eaf3.us-east-1.rds.amazonaws.com"
username = "vshenoy"
password = "tdf-analytics"
dbname = "tdf"
	
db = MySQLdb.connect(host=hostname,    # your host, usually localhost
                     user=username,         # your username
                     passwd=password,  # your password
                     db=dbname)        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM tdf.cyclist")

# print all the first cell of all the rows
for row in cur.fetchall():
    print row[0]

db.close()