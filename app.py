from datetime import datetime, timedelta
import os

from flask import *
from flask import Flask, render_template, request ,session
from pymongo import MongoClient
from csv import writer


app = Flask(__name__)


client = MongoClient("mongodb+srv://HLI:hli123@cluster0.m3oowl9.mongodb.net/?retryWrites=true&w=majority")

db = client['STUDENT']

studentdetails = db.DETAILS

policies = db.POLICY

lpolicy=db.LPOLICY

app.secret_key = os.urandom(24)

app.secret_key = "login"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
@app.route("/success", methods=['GET', 'POST'])
def onsubmit():
    email = request.form.get('em')
    password = request.form.get('pwd')
    confirmPass = request.form.get('cpwd')
    date=datetime.now()
    date_time = date.strftime("%d/%m/%Y, %H:%M:%S")
    c = {"Email": email, "Password": password,"Date":date_time}
    f = open("static/users.csv", "a")
    d = email
    e = password
    dt = writer(f)
    dt.writerow([d, e])
    f.close()


    if confirmPass == password:
        studentdetails.insert_one(c)
        return redirect(url_for('login'))

    else:

        return render_template("register.html")



@app.route("/addprofile", methods=['GET', 'POST'])
def addprofile():
    FN=request.form.get('pfn')
    LN=request.form.get('pln')

    EM=request.form.get('pem')
    DOB=request.form.get('pdob')
    ADD=request.form.get('padd')
    CITY=request.form.get('pct')
    MOB=request.form.get('pmob')
    ADHAAR=request.form.get('padhaar')


    dt={"Details":{"First_Name":FN,"Last_Name":LN,"Email":EM,"Data_of_Birth":DOB,"Address":ADD,"City":CITY,"Mobile_Number":MOB,"Adhaar_Number":ADHAAR}}


    data=studentdetails.find({'Email':session['user']})

    if data:
        studentdetails.update_one(
            {"Email":session['user']},

                {"$set": dt}

        )


    return redirect(url_for('home1'))





@app.route("/add", methods=['GET', 'POST'])
def onadd():
    Type = request.form.get('type')
    Premium = request.form.get('prm')
    Discription = request.form.get('dis')

    p = {"Type": Type, "Premium": Premium, "Discription": Discription}

    if Type=="Health":
        policies.insert_one(p)
    elif Type=="Life":
        lpolicy.insert_one(p)
    return redirect(url_for('admin'))


@app.route('/download')
def Download_File():
    PATH = 'static/users.csv'
    return send_file(PATH, as_attachment=True)


@app.route("/login1", methods=['GET', 'POST'])
def onlogin():
    email = request.form.get('lem')
    password = request.form.get('lpwd')

    c = {"Email": email, "Password": password}

    d = {"Email": "chinnu@gmail.com", "Password": "chinnu123"}
    b = studentdetails.find_one(c)

    if request.method == "POST":
        session['user']=email
    if c == d:
        return redirect(url_for('admin'))

    elif b:
        return redirect(url_for('home1'))
    else:
        return redirect(url_for('login'))


@app.route("/users", methods=['GET', 'POST'])
def ViewUsers():
    email = request.form.get('lem')
    password = request.form.get('lpwd')

    c = {"Email": email, "Password": password}

    b = studentdetails.find()

    count = studentdetails.count_documents({})

    return render_template("usersAdmin.html", b=b, count=count)


@app.route("/policies", methods=['GET', 'POST'])
def ViewPolicies():
    x = policies.find()

    t = lpolicy.find()



    return render_template("policies.html", x=x ,t=t)


@app.route("/delete_policies/<name>", methods=['GET', 'POST', 'DELETE'])
def delete(name):
    y = {'Premium': name}

    policies.delete_one(y)

    return redirect(url_for('ViewPolicies'))

@app.route("/delete_lpolicies/<policy>", methods=['GET', 'POST', 'DELETE'])
def ldelete(policy):
    a = {'Premium': policy}

    lpolicy.delete_one(a)

    return redirect(url_for('ViewPolicies'))


@app.route("/remove_user/<a>", methods=['GET', 'POST', 'DELETE'])
def removeUser(a):
    z = {'Email': a}

    studentdetails.delete_one(z)

    return redirect(url_for('ViewUsers'))


@app.route("/")
def home():
    return render_template("nav.html")


@app.route("/admin")
def admin():
    if not session.get("user"):
        return redirect("/login")
    return render_template("admin.html")

@app.route("/logout")
def logout():

    session.pop('user',None)
    return render_template("login.html")

@app.route("/logout1")
def logout1():

    session.pop('user',None)
    return render_template("login.html")


@app.route("/addpolicy")
def addPolicy():
    return render_template("AddPolicy.html")


@app.route("/home1")
def home1():
    if not session.get("user"):
        return redirect("/login")
    return render_template("userHome.html",user=session['user'])


@app.route("/home")
def home2():
    return render_template("nav.html")


@app.route("/aboutUs")
def aboutus():

    return render_template("aboutUs.html")


@app.route("/lpolicies")
def lpolicies():

    return render_template("viewProfile.html")


@app.route("/profile")
def profile():

    k=studentdetails.find_one({"Email":session['user']})
    l=k['Details']
    return render_template("userProfile.html",l=l)


@app.route("/register")
def registration():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/contactus")
def contactus():
    return render_template("contactus.html")


@app.route("/healthInsurance", methods=['GET', 'POST'])
def hinsurance():
    x = policies.find()

    return render_template("health.html", x=x , em=session['user'])

@app.route("/lifeInsurance", methods=['GET', 'POST'])
def linsurance():
    c = lpolicy.find()

    return render_template("lifeInsurance.html", c=c)


@app.route("/customerHealth", methods=['GET', 'POST'])
def Cinsurance():
    x = policies.find()

    return render_template("customerHealth.html", x=x)


@app.route("/customerLife", methods=['GET', 'POST'])
def Lifeinsurance():
    c = lpolicy.find()

    return render_template("customerLife.html", c=c)




if __name__ == "__main__":
    app.run()
