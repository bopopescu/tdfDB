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
	teams = ''' SELECT DISTINCT Team FROM tdf.cyclist '''
	nation = ''' select distinct Nationality from tdf.cyclist'''
	manf = ''' SELECT DISTINCT BikeManf FROM tdf.cyclist  '''
	
	cur.execute(fastest_stage)
	ftl = cur.fetchall()	
	
	cur.execute(teams)
	teams = cur.fetchall()

	cur.execute(nation)
	nation = cur.fetchall()
	    


	return render_template('blog-simple.html', ftl=ftl, teams=teams, nation=nation, manf=manf)


@app.route('/name_update/', methods=["GET", "POST"])
def name_update():

	oldName = request.form.get("oldName")
	newName = request.form.get("newName")
	#print newName
	cur = db.cursor()
	

	
	
	oldCyclist = ''' SELECT * FROM tdf.cyclist c1 WHERE c1.Name = '{0}' '''.format(oldName)
	oldCompetes = ''' SELECT * FROM tdf.competes c1 WHERE c1.Name = '{0}' '''.format(oldName)
		
	cur.execute(oldCyclist)
	t1 = cur.fetchall()	
	c1 = [desc[0] for desc in cur.description]
	
	cur.execute(oldCompetes)
	t2 = cur.fetchall()
	c2 = [desc[0] for desc in cur.description]


	query = '''  UPDATE tdf.cyclist c1
	SET c1.Name = '{1}'
	WHERE c1.Name = '{0}' '''.format(oldName, newName)

	cur.execute(query)

	#################################################################################
 	
	newCyclist = ''' SELECT * FROM tdf.cyclist c1 WHERE c1.Name = '{0}' '''.format(newName)
	newCompetes = ''' SELECT * FROM tdf.competes c1 WHERE c1.Name = '{0}' '''.format(newName)
		
	cur.execute(newCyclist)
	t3 = cur.fetchall()	
	c3 = [desc[0] for desc in cur.description]
	
	cur.execute(newCompetes)
	t4 = cur.fetchall()
	c4 = [desc[0] for desc in cur.description]
	
	


	return render_template('multipleTable.html', t1=t1, c1=c1, t2=t2, c2=c2, t3=t3, c3=c3, t4=t4, c4=c4 )

	


@app.route('/updates/')
def updates():

	cur = db.cursor()

	names = ''' SELECT c1.Name 
		FROM tdf.cyclist c1 
		LIMIT 10; '''
			
	cur.execute(names)
	cyclist_name = cur.fetchall()


	return render_template('updates.html', cyclist_name=cyclist_name)


@app.route('/patterns/')
def patterns():

	return render_template('patterns.html')


@app.route('/patterns_bmc/', methods=["GET", "POST"])
def patterns_bmc():


	country = request.form.get("three_countries")
	print country
	cur = db.cursor()

	query = """ SELECT *
	from tdf.cyclist c1
	where not exists
		(select *
		from tdf.cyclist c1 
		where c1.team = 'BMC Racing' and c1.nationality = '{0}') """.format(country)
	cur.execute(query)

	
	tableDat = cur.fetchall()
	columns = [desc[0] for desc in cur.description]


	return render_template('results_fastest.html', tableDat=tableDat, columns=columns)




@app.route('/patterns_time_trial/', methods=["GET", "POST"])
def patterns_time_trial():

	cur = db.cursor()
	
	query = """ SELECT c1.Name, c1.stageNum, b1.manufacturer, b1.modelNum
FROM tdf.competes c1
left join tdf.bikes b1 on c1.modelNum = b1.modelNum
left join tdf.stages s1 on c1.stageNum = s1.stageNum
where not exists(
	select b2.manufacturer, modelNum
    from tdf.bikes b2, tdf.stages s2
    where b2.bikeType = 'Time Trial' and s2.type = 'Time Trial') """
	cur.execute(query)

	
	tableDat = cur.fetchall()
	columns = [desc[0] for desc in cur.description]


	return render_template('results_fastest.html', tableDat=tableDat, columns=columns)



@app.route("/fastest_time/", methods=["GET", "POST"])
def get_fastest_time():

	x = ""
	if request.method == 'POST':
		print "POST METHOD"
		x = request.form.get("stage_option")
		
	elif request.method == "GET":
		print "GET METHOD"
	
	
	stageString = x

	cur = db.cursor()
	
	query = """ SELECT s1.stageNum, s1.Type, s1.Distance, c1.Name, c2.stageTime as time_stage
	from tdf.cyclist c1
	left join tdf.competes c2 on c1.Name = c2.Name
	left join tdf.stages s1 on c2.stageNum = s1.stageNum
	where s1.stageNum = {0}
	order by time_stage asc
	limit 1 """.format(stageString)
	cur.execute(query)

	tableDat = cur.fetchall()
	columns = [desc[0] for desc in cur.description]

	


	return render_template('results_fastest.html', tableDat=tableDat, columns=columns)





@app.route("/fastest_time_country/", methods=["GET", "POST"])
def get_fastest_time_country():

	x = ""
	if request.method == 'POST':
		print "POST METHOD"
		x = request.form.get("stage_option")
		
	elif request.method == "GET":
		print "GET METHOD"
	
	
	stageString = x
	countries = request.form.get("countries")
	cur = db.cursor()
	
	query = """ SELECT s1.stageNum, s1.Type, s1.Distance, c1.Name, c2.stageTime as time_stage
	from tdf.cyclist c1
	left join tdf.competes c2 on c1.Name = c2.Name
	left join tdf.stages s1 on c2.stageNum = s1.stageNum
	where s1.stageNum = {0} and c1.Nationality = '{1}'
	order by time_stage asc
	limit 5 """.format(stageString, countries)
	cur.execute(query)

	tableDat = cur.fetchall()
	columns = [desc[0] for desc in cur.description]

	print columns


	return render_template('results_fastest.html', tableDat=tableDat, columns=columns)


@app.route("/avghw/", methods=["GET", "POST"])
def averagehw():

	
	
	teamString = request.form.get("teams")
	

	cur = db.cursor()
	
	query = """ SELECT c1.Nationality, round(avg(c1.height), 2) as avgHeight, round(avg(c1.weight), 2) as avgWeight
	from tdf.cyclist c1
	group by c1.Nationality
	having c1.Nationality = "{0}"
	order by avgHeight asc""".format(teamString)
	cur.execute(query)

	tableDat = cur.fetchall()
	columns = [desc[0] for desc in cur.description]

	print columns


	return render_template('results_fastest.html', tableDat=tableDat, columns=columns)



@app.route("/avgmanf/", methods=["GET", "POST"])
def averageManf():

	
	
	stageOption = request.form.get("stage_option")
	calcData = request.form.get("calcData")

	cur = db.cursor()
	
	query = """ SELECT distinct c1.BikeManf, sec_to_time(round({1}(time_to_sec(stageTime)), 0)) as calcTime
	from (
		select *
	    from tdf.competes c2
	    where c2.stageNum = {0}) as c1
	group by c1.bikeManf""".format(stageOption, calcData)
	cur.execute(query)

	tableDat = cur.fetchall()
	columns = [desc[0] for desc in cur.description]

	print columns


	return render_template('results_fastest.html', tableDat=tableDat, columns=columns)




@app.route("/avgmax_time_team/", methods=["GET", "POST"])
def average_time_team():

	
	
	teamString = request.form.get("teams")
	calcString = request.form.get("calcData")

	cur = db.cursor()
	
	query = """ SELECT c2.stageNum as stageNums, s1.Type, s1.Distance, sec_to_time(round({1}(time_to_sec(stageTime)), 0)) as time
	from tdf.cyclist c1
	left join tdf.competes c2 on c1.Name = c2.Name
	left join tdf.stages s1 on s1.stageNum = c2.stageNum
	group by c2.stageNum, Team
	having Team = '{0}'
	order by stageNums asc, time asc """.format(teamString, calcString)
	cur.execute(query)

	tableDat = cur.fetchall()
	columns = [desc[0] for desc in cur.description]

	print columns


	return render_template('results_fastest.html', tableDat=tableDat, columns=columns)


@app.route("/calories_consumed/", methods=["GET", "POST"])
def calories_consumed():

	
	
	x = ""
	if request.method == 'POST':
		print "POST METHOD"
		x = request.form.get("stage_option")
		
	elif request.method == "GET":
		print "GET METHOD"
	
	
	stageString = x

	cur = db.cursor()
	
	query = """ SELECT s1.stageNum, c1.Name, c1.Team, c2.stageTime as stageTime, f2.Calories, f2.Carbohydrates, f2.Proteins, f2.Fats
	from tdf.cyclist c1
		left join tdf.competes c2 on c1.Name = c2.Name
		left join tdf.stages s1 on c2.stageNum = s1.stageNum
	    left join tdf.consumes f1 on s1.stageNum = f1.stageNum
	    left join tdf.foods f2 on f1.Name = f1.Name
	where c2.stageNum = {0}
	order by stageTime asc
	limit 1 """.format(stageString)
	cur.execute(query)

	tableDat = cur.fetchall()
	columns = [desc[0] for desc in cur.description]

	print columns


	return render_template('results_fastest.html', tableDat=tableDat, columns=columns)








'''


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

'''