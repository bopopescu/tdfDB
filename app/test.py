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

	fastest_stage = ''' SELECT stageNum, start, end, Distance, type FROM tdf.stages  '''

	cur.execute(fastest_stage)
	
	option_list = cur.fetchall()    


	return render_template('blog-simple.html', option_list=option_list)



@app.route("/forward/", methods=["GET", "POST"])
def move_forward():

	x = ""
	if request.method == 'POST':
		print "POST METHOD"
		x = request.form.get("teamdata")
		x = "*"
	elif request.method == "GET":
		print "GET METHOD"
	


	cur = db.cursor()
	query = "SELECT DISTINCT {0} FROM tdf.cyclist LIMIT 10".format(x)
	print query
	

	query = """ SELECT stageNum as stageNumber, Team, sec_to_time(avg(time_to_sec(stageTime))) as time
	from tdf.cyclist c1
	left join tdf.competes c2 on c1.Name = c2.Name
	group by stageNum, Team
	order by stageNumber asc, time asc """
	cur.execute(query)

	tableDat = cur.fetchall()
	columns = [desc[0] for desc in cur.description]
	


	return render_template('results.html', tableDat=tableDat, columns=columns)

