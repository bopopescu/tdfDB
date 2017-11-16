from flask import Flask, render_template, Response, request, redirect, url_for
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

	cur.execute("SELECT * FROM tdf.cyclist LIMIT 10")
	
	option_list = cur.fetchall()    


	return render_template('index.html', option_list= option_list)




@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    forward_message = "Moving Forward..."
    return render_template('blog.html');
