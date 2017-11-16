from flask import Flask, render_template
import MySQLdb


app = Flask(__name__)



hostname = "tdf-analytics.c9sxquz8eaf3.us-east-1.rds.amazonaws.com"
username = "vshenoy"
password = "tdf-analytics"
dbname = "tdf"
	
db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname)        # name of the data base





@app.route('/')
def hello_world():

	cur = db.cursor()

	# Use all the SQL you like
	cur.execute("SELECT * FROM tdf.cyclist LIMIT 10")

	# print all the first cell of all the rows
	#for row in cur.fetchall():
	 #   print row[0]

	#x = cur.fetchall()

	option_list = cur.fetchall()    


	return render_template('index.html', option_list= option_list)
