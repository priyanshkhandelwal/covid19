from flask import Flask,render_template,request,redirect,url_for
import json
import requests
import pymysql as sql
app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/aftersignup/",methods=["POST","GET"])
def aftersignup():
    if request.method == "POST":
        firstname = request.form.get("fname")
        lastname = request.form.get("lname")
        email=request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        if password == cpassword:
            try:
                db=sql.connect(host="localhost", port=3306, user="root", password="", database="flask")
            except:
                return "\n Connectivity Issue....."
            else:
                cur =db.cursor()
                cmd = f"select email from user where email='{email}'"
                cur.execute(cmd)
                data = cur.fetchone()
                if data:
                    error = "Email already registered"
                    return render_template("signup.html")
                else:
                    cmd = f"insert into user value('{firstname}','{lastname}','{email}','{password}')"
                    cur.execute(cmd)
                    db.commit()
                    return render_template("login.html")
        else:
            error = "Password does not match please try again"
            return render_template("signup.html", error=error)

    else:
        return render_template("signup.html")


@app.route("/afterlogin/",methods=["POST","GET"])
def afterlogin():
    if request.method == "POST":
        email=request.form.get("email")
        password = request.form.get("password")
        try:
            db = sql.connect(host="localhost", port=3306, user="root", password="", database="flask")
        except Exception as e:
            return e
        else:
            cmd = f"select * from user where email='{email}'"
            cur = db.cursor()
            cur.execute(cmd)
            data = cur.fetchone()
            if data:
                if password == data[3]:
                    print(password)
                    return render_template("afterloginindex.html")
                else:
                    error="Invalid Password...."
                    return render_template("login.html",error=error)
            else:
                error="Invalid Email...."
                return render_template("login.html",error=error)
    else:
        error="Invalid Request...."
        return render_template('login.html',error=error)  

@app.route("/signout/")
def signout():
    return render_template("index.html") 

@app.route("/knowlivestats/")
def livestats():
    return render_template("livestats.html")

@app.route("/getdata/", methods=["POST","GET"])
def getdata():
    if request.method=="POST":
        state=request.form.get("state")
        url='https://corona.lmao.ninja/v2/gov/India'
        response=requests.get(url)
        if response.status_code==200:
            data=json.loads(response.text)
            st=data['states']
            d={}
            for i in range(len(st)):
                if st[i]['state']==state:
                    d['cases']=st[i]['cases']
                    d['recovered']=st[i]['recovered']
                    d['deaths']=st[i]['deaths']
                    d['active']=st[i]['active']
                    return render_template("showdata.html", data=d, state=state)
            else:
                return render_template("livestats.html", error="Invalid state")
        else:
            return render_template("livestats.html", error="Invalid status")
    else:
        return redirect(url_for('login'))

app.run(host="localhost", port=80, debug=True)