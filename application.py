from flask import Flask,render_template,request, session, url_for, escape, redirect, abort, make_response
import json
import string
import random
from werkzeug.utils import secure_filename
import os
import db
import genpass

pyBot = db.Database()

app=Flask(__name__)
app.secret_key = "pollsapp"

@app.route('/')
def index():
	if 'login' in session:
		pollsCountPrivate = pyBot.getPrivatePolls('username')
		pollsCountPublic = pyBot.getPublicPolls('username')
		return render_template('index.html', pollsCountPrivate=pollsCountPrivate, pollsCountPublic=pollsCountPublic)
	else:
		pollsCountPublic= pyBot.getPublicPolls('username')
		return render_template('index.html', pollsCountPublic=pollsCountPublic)

@app.route('/login')
def log_in():
	if 'username' in session:
		session['login'] = "signed_in"
		return redirect(url_for('dashboard'))
	return render_template("login.html")

@app.route('/register')
def register():
	if 'login' in session:
		return redirect(url_for('dashboard'))
	return render_template('register.html')

@app.route('/registrationconfirm', methods=["POST"])
def otpconfirm():
	username = request.form["username"]
	password = request.form["user_pass"]
	checkUser = pyBot.checkUser(username)
	if checkUser == None:
		try:
			pyBot.register_user(username, password)
			return render_template("success.html")
		except:
			return render_template("userExists.html")
	else:
		return render_template("userExists.html")

@app.route('/validate', methods=["POST"])
def validate():
	uid = request.form["userid"]
	upass = request.form["user_pass"]
	check_user = pyBot.con_auth(uid, upass)
	if check_user == None:
		return render_template("nouser.html")
	else:
		session['username'] = uid
		session['login'] = "signed_in"
		return redirect(url_for('dashboard'))

@app.route('/addpassword', methods=["GET"])
def addpassword():
	if 'login' in session:
		return render_template('addpassword.html')
	else:
		abort(404)

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('login', None)
	return redirect(url_for('index'))
		
@app.route('/dashboard', methods=["GET"])
def dashboard():
	if 'login' in session:
		return render_template('dashboard.html')
	else:
		return redirect(url_for('log_in'))

@app.route('/addpoll', methods=["POST"])
def create():
	if 'login' in session:
		question = request.form["question"]
		option1 = request.form["option1"]
		option2 = request.form["option2"]
		typePoll = request.form["typePoll"]
		pyBot.addpoll(question, option1, option2, session["username"], typePoll)
		return render_template('polladded.html')

@app.route('/poll/<pollid>', methods=["POST"])
def getTeam(pollid):
	check = pyBot.getPollbyID(pollid)
	return render_template('showPoll.html', check=check)

@app.route('/vote', methods=["POST"])
def vote():
	pollid = request.form["pollid"]
	option = request.form["option"]
	check = pyBot.getPollbyID(pollid)
	if option == check["op1"]:
		increaseCount = str(int(check["op1count"])+1)
		pyBot.giveVote(pollid, "op1", increaseCount)
		return render_template("voted.html")
	else:
		increaseCount = str(int(check["op2count"])+1)
		pyBot.giveVote(pollid, "op2", increaseCount)
		return render_template("voted.html")

if __name__ == '__main__':
	app.run()
