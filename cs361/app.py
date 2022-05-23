from flask import Flask
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import urllib
import requests
import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs361_zhanzh'
app.config['MYSQL_PASSWORD'] = '4548'
app.config['MYSQL_DB'] = 'cs361_zhanzh'

mysql = MySQL(app)

def get_time():
    response_API = requests.get('http://127.0.0.1:7777/')
    #response_API = requests.get('http://1986-2603-9001-5504-e427-8dfa-bc47-4f6c-ad09.ngrok.io/')

    data = response_API.text
    parse_json = json.loads(data)
    results = parse_json['Timestamp']
    return results

def check_status():
    now_time = get_time()
    now_time = datetime.datetime.strptime(now_time,'%Y-%m-%d %H:%M')
    query = "SELECT * FROM EVENTS;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    events = cur.fetchall()
    for i in events:
        start_time = i[4]
        end_time = i[5]
        start_diff = now_time - start_time
        end_diff = now_time - end_time
        if(start_diff.days < 0):
            query = "UPDATE EVENTS SET status = %s where eventid = %s;"
            cur.execute(query,('Feture', i[0]))
        if(start_diff.days > 0 and end_diff.days < 0):
            query = "UPDATE EVENTS SET status = %s where eventid = %s;"
            cur.execute(query,('Working', i[0]))
        if(end_diff.days > 0):
            query = "UPDATE EVENTS SET status = %s where eventid = %s;"
            cur.execute(query,('Old', i[0]))

@app.route('/', methods=["POST","GET"])
def sign():
    query = "SELECT * FROM USERS;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    users = cur.fetchall()

    if request.method == "POST":
        name = request.form["user"]
        password = request.form["password"]
        if request.form.get("sign"):
            for i in users:
                if (name == i[1] and password == i[2]):
                    get_event = "SELECT * FROM EVENTS WHERE userid = %s;"
                    cur.execute(get_event,(str(i[0])))
                    events = cur.fetchall()
                    return render_template("home.html", events = events)
            return render_template("sign.html")
    
    else:
        return render_template("sign.html")

@app.route("/home", methods=['GET','POST'])
def event():
    check_status()
    get_event = "SELECT * FROM EVENTS WHERE userid = %s;"
    cur = mysql.connection.cursor()
    cur.execute(get_event,(str(i[0])))
    events = cur.fetchall()
    return render_template("home.html", events = events)

@app.route('/NewEvent')
def newevent():
    cur = mysql.connection.cursor()

    if request.method == "POST":
        name = request.form["user"]
        status = request.form["status"]
        start = request.form["start"]
        end = request.form["end"]

        if request.form.get("newevent"):
            query = "INSERT EVENTS (`name`, `status`, `start`, `end`) VALUES (%s, %s, %s, %s);"
            data = (name, status, start, end)
            cur.execute(query, data)
            return render_template("home.html")
    
    else:
        return render_template("NewEvent.html")

@app.route('/NewUser',methods=['POST','GET'])
def newuser():
    cur = mysql.connection.cursor()

    if request.method == "POST":
        name = request.form["user"]
        password = request.form["password"]
        data = (name, password)

        if request.form.get("newuser"):
            query = "INSERT USERS (`name`, `password`) VALUES (%s, %s);"
            cur.execute(query, data)
            return render_template("sign.html")
    
    else:
        return render_template("NewUser.html")

@app.route('/Update')
def upevent():
    
    cur = mysql.connection.cursor()
    name = request.form["user"]
    status = request.form["status"]
    start = request.form["start"]
    end = request.form["end"]

    if request.method == "POST":
        data = (name, status, start, end)
        if request.form.get("newevent"):
            query = "UPDATE EVENTS SET name = %s, status = %s, start = %s, end = %s) WHERE id = %d;"
            cur.execute(query, data)
            return render_template("home.html")
    
    else:
        return render_template("update.html")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 17710)) 
    app.run(port=port, debug=True) 